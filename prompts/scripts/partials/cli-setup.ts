import { Command } from 'commander'
import chalk from 'chalk'
import { generateRepoXML } from './file-generator.js'
import {
  listGeneratedFiles,
  listProfiles,
  getLatestFilePath,
} from './file-lister.js'
import { estimateSize, estimateAllProfiles } from './size-estimator.js'

interface Paths {
  profilesPath: string
  configPath: string
  generatedDir: string
  projectRoot: string
}

interface CLIOptions {
  isVerbose?: boolean
  isDryRun?: boolean
  profile?: string
  isEstimate?: boolean
  isEstimateOnly?: boolean
}

interface ListOptions {
  profile?: string
}

interface LatestOptions {
  profile?: string
}

interface EstimateOptions {
  profile?: string
}

/**
 * Setup CLI commands
 */
export default function setupCLI(paths: Paths): Command {
  const { profilesPath, configPath, generatedDir, projectRoot } = paths

  const program = new Command()

  program
    .name('generate')
    .description('Generate repository XML for AI prompts using Repomix')
    .version('1.0.0')

  program
    .command('run', { isDefault: true })
    .description(
      'Generate repository XML for all profiles (default) or specific profile'
    )
    .option('-v, --verbose', 'Enable verbose output')
    .option(
      '-d, --dry-run',
      'Show what would be generated without creating files'
    )
    .option(
      '-p, --profile <profile>',
      'Generate only specific profile (minimal, core, full, docs)'
    )
    .option('-e, --estimate', 'Only estimate output size without generating')
    .action(async (options: CLIOptions) => {
      if (options.isEstimate) {
        options.isEstimateOnly = true
      }
      await generateRepoXML({
        profilesPath,
        configPath,
        generatedDir,
        projectRoot,
        options
      })
    })

  program
    .command('list')
    .description('List generated XML files')
    .alias('ls')
    .option('-p, --profile <profile>', 'Filter by profile')
    .action((options: ListOptions) => {
      listGeneratedFiles({ generatedDir, options })
    })

  program
    .command('profiles')
    .description('List available profiles')
    .action(() => {
      listProfiles({ profilesPath })
    })

  program
    .command('latest')
    .description('Show path to latest generated file')
    .option('-p, --profile <profile>', 'Get latest file for specific profile')
    .action((options: LatestOptions) => {
      const latestFile = getLatestFilePath({
        generatedDir,
        profile: options.profile || null
      })

      if (latestFile) {
        console.log(latestFile)
      } else {
        const message = options.profile
          ? `No latest file found for profile '${options.profile}'`
          : 'No latest file found'
        console.log(chalk.yellow(message))
        process.exit(1)
      }
    })

  program
    .command('estimate')
    .description('Estimate output size for all profiles or specific profile')
    .option('-p, --profile <profile>', 'Estimate for specific profile only')
    .action((options: EstimateOptions) => {
      if (options.profile) {
        estimateSize({ profile: options.profile, profilesPath, configPath })
      } else {
        estimateAllProfiles({ profilesPath })
      }
    })

  return program
}
