import { execSync } from 'child_process'
import {
  writeFileSync,
  unlinkSync,
  symlinkSync,
  existsSync,
  statSync,
} from 'fs'
import { join } from 'path'
import chalk from 'chalk'
import { generateTimestamp, getFileSize, countLines } from './utils.js'
import {
  loadProfiles,
  createProfileConfig,
  loadBaseConfig,
  type Profile,
  type BaseConfig,
} from './config-manager.js'

interface GenerationOptions {
  isVerbose?: boolean
  isDryRun?: boolean
  profile?: string
  isEstimateOnly?: boolean
}

interface SingleProfileResult {
  profile: string
  timestamp: string
  outputFile: string
  latestLink: string
  isDryRun?: boolean
  config?: BaseConfig
  fileSize?: string
  lineCount?: number
  fileSizeBytes?: number
  isSuccess?: boolean
  error?: string
}

interface GenerationResult {
  results?: SingleProfileResult[]
  successful?: number
  failed?: number
  total?: number
  isEstimateOnly?: boolean
  profiles?: string[]
}

interface GenerateSingleProfileOptions {
  profileName: string
  profileConfig: Profile
  baseConfig: BaseConfig
  generatedDir: string
  projectRoot: string
  options?: GenerationOptions
}

interface GenerateRepoXMLOptions {
  profilesPath: string
  configPath: string
  generatedDir: string
  projectRoot: string
  options?: GenerationOptions
}

/**
 * Generate repository XML for a single profile
 */
export async function generateSingleProfile({
  profileName,
  profileConfig,
  baseConfig,
  generatedDir,
  projectRoot,
  options = {}
}: GenerateSingleProfileOptions): Promise<SingleProfileResult> {
  const { isVerbose = false, isDryRun = false } = options

  const config = createProfileConfig({ profile: profileConfig, baseConfig })
  const timestamp = generateTimestamp()
  const profileSuffix = `_${profileName}`
  const outputFile = join(
    generatedDir,
    `repo_${timestamp}${profileSuffix}.xml`
  )
  const latestLink = join(generatedDir, `repo_latest${profileSuffix}.xml`)

  // Guard clause: Handle dry run early
  if (isDryRun) {
    console.log(
      chalk.yellow(
        `🔍 [${profileName}] Dry run - would generate: ${outputFile}`
      )
    )
    return {
      profile: profileName,
      timestamp,
      outputFile,
      latestLink,
      isDryRun: true,
      config,
    }
  }

  try {
    // Create temporary config file
    const tempConfigPath = join(
      generatedDir,
      `temp_config_${timestamp}_${profileName}.json`
    )
    writeFileSync(tempConfigPath, JSON.stringify(config, null, 2))

    // Run repomix with configuration
    const command = `repomix --config "${tempConfigPath}" --output "${outputFile}"`

    if (isVerbose) {
      console.log(chalk.gray(`🔧 [${profileName}] Command: ${command}`))
    }

    execSync(command, {
      cwd: projectRoot,
      stdio: isVerbose ? 'inherit' : 'pipe',
    })

    // Clean up temporary config
    if (existsSync(tempConfigPath)) {
      unlinkSync(tempConfigPath)
    }

    // Check if file was created
    if (!existsSync(outputFile)) {
      throw new Error('Output file was not created')
    }

    const fileSize = getFileSize({ filePath: outputFile })
    const lineCount = countLines({ filePath: outputFile })
    const fileSizeBytes = statSync(outputFile).size

    // Update latest symlink
    if (existsSync(latestLink)) {
      unlinkSync(latestLink)
    }
    const relativePath = `repo_${timestamp}${profileSuffix}.xml`
    symlinkSync(relativePath, latestLink)

    return {
      profile: profileName,
      timestamp,
      outputFile,
      latestLink,
      fileSize,
      lineCount,
      fileSizeBytes,
      isSuccess: true,
    }
  } catch (error) {
    return {
      profile: profileName,
      timestamp,
      outputFile,
      latestLink,
      isSuccess: false,
      error: (error as Error).message,
    }
  }
}

/**
 * Generate repository XML using repomix
 */
export async function generateRepoXML({
  profilesPath,
  configPath,
  generatedDir,
  projectRoot,
  options = {}
}: GenerateRepoXMLOptions): Promise<GenerationResult> {
  const { isDryRun = false, profile = null, isEstimateOnly = false } = options

  console.log(chalk.blue('🚀 Generating repository XML with Repomix...'))

  // Load profiles and base configuration
  const profiles = loadProfiles({ profilesPath })
  const baseConfig = loadBaseConfig({ configPath })

  // Determine which profiles to generate
  let profilesToGenerate: Record<string, Profile>

  if (profile) {
    // Guard clause: Check if profile exists
    if (!profiles.profiles[profile]) {
      console.error(chalk.red(`❌ Profile '${profile}' not found`))
      console.log(chalk.yellow('Available profiles:'))
      Object.keys(profiles.profiles).forEach(p => {
        console.log(chalk.yellow(`  - ${p}`))
      })
      process.exit(1)
    }

    profilesToGenerate = { [profile]: profiles.profiles[profile] }
    console.log(chalk.blue(`📝 Generating single profile: ${profile}`))
  } else {
    profilesToGenerate = profiles.profiles
    console.log(
      chalk.blue(
        `📝 Generating all profiles: ${Object.keys(profilesToGenerate).join(', ')}`
      )
    )
  }

  // Estimate size if requested
  if (isEstimateOnly) {
    console.log(chalk.blue('📊 Estimating sizes for selected profiles...'))
    Object.entries(profilesToGenerate).forEach(([name, profileConfig]) => {
      console.log(
        chalk.cyan(
          `${name}: ${profileConfig.description} (${profileConfig.maxTotalSize || 'No limit'})`
        )
      )
    })
    return { isEstimateOnly: true, profiles: Object.keys(profilesToGenerate) }
  }

  if (isDryRun) {
    console.log(chalk.yellow('🔍 Dry run mode - no files will be generated'))
  }

  // Generate each profile
  const results: SingleProfileResult[] = [];
  const profileNames = Object.keys(profilesToGenerate);

  for (let i = 0; i < profileNames.length; i++) {
    const profileName = profileNames[i];
    const profileConfig = profilesToGenerate[profileName];

    console.log(
      chalk.yellow(
        `⚡ [${i + 1}/${profileNames.length}] Generating profile: ${profileName}`
      )
    );
    console.log(chalk.gray(`   📋 ${profileConfig.description}`));

    const result = await generateSingleProfile({
      profileName,
      profileConfig,
      baseConfig,
      generatedDir,
      projectRoot,
      options
    })
    results.push(result)

    if (result.isSuccess) {
      console.log(
        chalk.green(
          `   ✅ ${profileName}: ${result.fileSize} (${result.lineCount?.toLocaleString()} lines)`
        )
      )

      // Check if output is too large for context window
      const warningThreshold = 100 * 1024 // 100KB
      if (result.fileSizeBytes && result.fileSizeBytes > warningThreshold) {
        console.log(
          chalk.yellow(
            `   ⚠️  Warning: ${profileName} (${result.fileSize}) may be too large for context window`
          )
        )
      }
    } else if (result.error) {
      console.log(chalk.red(`   ❌ ${profileName}: ${result.error}`))
    } else if (result.isDryRun) {
      console.log(
        chalk.gray(`   🔍 ${profileName}: Would generate ${result.outputFile}`)
      )
    }
  }

  // Summary
  const successful = results.filter(r => r.isSuccess)
  const failed = results.filter(r => !r.isSuccess && !r.isDryRun)

  if (isDryRun) {
    console.log(
      chalk.blue(
        `\n📋 Dry run summary: ${results.length} profiles would be generated`
      )
    )
  } else {
    console.log(chalk.green(`\n✅ Generation completed!`))
    console.log(
      chalk.green(
        `📄 Successfully generated: ${successful.length}/${profileNames.length} profiles`
      )
    )

    if (successful.length > 0) {
      console.log(chalk.blue('\n📊 Generated files:'))
      successful.forEach(result => {
        console.log(
          chalk.blue(
            `  ${result.profile}: ${result.fileSize} (${result.lineCount?.toLocaleString()} lines)`
          )
        )
        console.log(chalk.gray(`    📁 ${result.outputFile}`))
        console.log(chalk.gray(`    🔗 ${result.latestLink}`))
      })
    }

    if (failed.length > 0) {
      console.log(
        chalk.red(
          `\n❌ Failed profiles: ${failed.map(r => r.profile).join(', ')}`
        )
      )
    }
  }

  return {
    results,
    successful: successful.length,
    failed: failed.length,
    total: profileNames.length,
  };
}
