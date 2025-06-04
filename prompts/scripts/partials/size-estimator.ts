import { readFileSync } from 'fs'
import chalk from 'chalk'
import { parseSize } from './utils.js'
import {
  loadProfiles,
  createProfileConfig,
  type Profile,
  type BaseConfig,
} from './config-manager.js'

interface EstimateResult {
  maxSize: string
  sizeInBytes: number
}

interface EstimateSizeOptions {
  profile?: string | null
  profilesPath: string
  configPath: string
}

interface EstimateAllProfilesOptions {
  profilesPath: string
}

/**
 * Estimate file size before generation
 */
export function estimateSize({ profile = null, profilesPath, configPath }: EstimateSizeOptions): EstimateResult {
  console.log(chalk.blue('📊 Estimating output size...'))

  const baseConfig = JSON.parse(readFileSync(configPath, 'utf8')) as BaseConfig
  let config = baseConfig

  if (profile) {
    const profiles = loadProfiles({ profilesPath })
    if (!profiles.profiles[profile]) {
      throw new Error(`Profile '${profile}' not found`)
    }
    config = createProfileConfig({ profile: profiles.profiles[profile], baseConfig })
  }

  // This is a rough estimation - repomix would need to be run to get exact size
  // For now, we'll provide a warning if the maxTotalSize is large
  const maxSize = config.maxTotalSize || '50MB'
  const sizeInBytes = parseSize({ sizeString: maxSize })

  const warningThreshold = 100 * 1024 // 100KB

  if (sizeInBytes > warningThreshold) {
    console.log(
      chalk.yellow(
        `⚠️  Warning: Max size is ${maxSize} - may exceed context window`
      )
    )
    console.log(
      chalk.yellow(
        '   Consider using a smaller profile (minimal, core, or docs)'
      )
    )
    return { maxSize, sizeInBytes }
  }

  console.log(
    chalk.green(`✅ Max size ${maxSize} should fit in context window`)
  )

  return { maxSize, sizeInBytes }
}

/**
 * Estimate sizes for all profiles
 */
export function estimateAllProfiles({ profilesPath }: EstimateAllProfilesOptions): void {
  const profiles = loadProfiles({ profilesPath })
  console.log(chalk.blue('📊 Size estimates for all profiles:\n'))

  Object.entries(profiles.profiles).forEach(
    ([name, profile]: [string, Profile]) => {
      console.log(chalk.cyan(`${name.padEnd(8)} - ${profile.description}`))
      console.log(
        chalk.gray(
          `${' '.repeat(10)}Max size: ${profile.maxTotalSize || 'No limit'}\n`
        )
      )
    }
  )

  console.log(
    chalk.yellow('💡 Tip: Use --profile <name> to estimate a specific profile')
  )
  console.log(
    chalk.gray(
      'Available profiles: ' + Object.keys(profiles.profiles).join(', ')
    )
  )
}
