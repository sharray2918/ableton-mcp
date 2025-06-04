import { existsSync, readdirSync } from 'fs'
import { join } from 'path'
import chalk from 'chalk'
import { getFileSize } from './utils.js'
import { loadProfiles } from './config-manager.js'

interface ListOptions {
  profile?: string
}

interface ListProfilesOptions {
  profilesPath: string
}

interface ListGeneratedFilesOptions {
  generatedDir: string
  options?: ListOptions
}

interface GetLatestFilePathOptions {
  generatedDir: string
  profile?: string | null
}

/**
 * List available profiles
 */
export function listProfiles({ profilesPath }: ListProfilesOptions): void {
  console.log(chalk.blue('📋 Available profiles:'))

  try {
    const profiles = loadProfiles({ profilesPath })

    Object.entries(profiles.profiles).forEach(([name, profile]) => {
      const size = profile.maxTotalSize || 'No limit'
      console.log(
        chalk.green(`  ${name.padEnd(10)} - ${profile.description} (${size})`)
      )
    })

    console.log(chalk.gray('\nUsage: generate run --profile <profile-name>'))
  } catch (error) {
    console.error(chalk.red('Error loading profiles'))
    return
  }
}

/**
 * List generated files with metadata
 */
export function listGeneratedFiles({
  generatedDir,
  options = {}
}: ListGeneratedFilesOptions): void {
  const { profile = null } = options

  console.log(chalk.blue('📋 Generated XML files:'))

  if (!existsSync(generatedDir)) {
    console.log(chalk.yellow('📁 No generated directory found'))
    return
  }

  const profileFilter = profile ? `_${profile}` : ''
  const files = readdirSync(generatedDir)
    .filter((file: string) => {
      // Skip symlinks
      if (file.startsWith('repo_latest')) return false

      // Filter by profile if specified
      if (profile) {
        return file.includes(profileFilter) && file.endsWith('.xml')
      }

      // Show all repo files
      return file.startsWith('repo_') && file.endsWith('.xml')
    })
    .sort()
    .reverse() // Most recent first

  if (files.length === 0) {
    const message = profile
      ? `📄 No XML files found for profile '${profile}'`
      : '📄 No XML files found'
    console.log(chalk.yellow(message))
    return
  }

  // Group files by profile
  const filesByProfile: Record<string, string[]> = {}

  files.forEach((file: string) => {
    const parts = file.replace('.xml', '').split('_')
    const profileName = parts.length > 2 ? parts.slice(2).join('_') : 'default'

    if (!filesByProfile[profileName]) {
      filesByProfile[profileName] = []
    }

    filesByProfile[profileName].push(file)
  })

  // Display files grouped by profile
  Object.entries(filesByProfile).forEach(([profileName, profileFiles]) => {
    // Skip if filtering by profile and this isn't the target profile
    if (profile && profileName !== profile) return

    const displayName = profileName === 'default' ? 'Default' : profileName
    console.log(chalk.cyan(`\n📁 Profile: ${displayName}`))

    profileFiles.forEach((file, index) => {
      const filePath = join(generatedDir, file)
      const fileSize = getFileSize({ filePath })

      // Extract timestamp
      const timestampMatch = file.match(/repo_(\d{12})/)
      if (!timestampMatch) {
        console.log(`   ${file} - ${fileSize}`)
        return
      }

      const timestamp = timestampMatch[1]
      const year = timestamp.substring(0, 4)
      const month = timestamp.substring(4, 6)
      const day = timestamp.substring(6, 8)
      const hour = timestamp.substring(8, 10)
      const minute = timestamp.substring(10, 12)
      const formattedDate = `${year}/${month}/${day} ${hour}:${minute}`

      const isLatest = index === 0
      const prefix = isLatest ? chalk.green('🔗') : '  '
      const status = isLatest ? chalk.green(' (latest)') : ''

      console.log(
        `${prefix} ${file} - ${formattedDate} - ${fileSize}${status}`
      )
    })
  })

  // Show available profiles if not filtering
  if (!profile) {
    console.log(chalk.gray('\nTip: Use --profile <name> to filter by profile'));
    console.log(chalk.gray('Available profiles: minimal, core, full, docs'));
  }
}

/**
 * Get latest file path for a profile
 */
export function getLatestFilePath({
  generatedDir,
  profile = null
}: GetLatestFilePathOptions): string | null {
  const profileSuffix = profile ? `_${profile}` : ''
  const latestLink = join(generatedDir, `repo_latest${profileSuffix}.xml`)

  if (existsSync(latestLink)) {
    return latestLink
  }

  return null
}
