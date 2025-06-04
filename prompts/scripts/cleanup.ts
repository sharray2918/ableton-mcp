#!/usr/bin/env node

import { readdirSync, unlinkSync, statSync } from 'fs'
import { join, dirname, resolve } from 'path'
import { fileURLToPath } from 'url'
import chalk from 'chalk'
import { Command } from 'commander'

const __filename = fileURLToPath(import.meta.url)
const __dirname = dirname(__filename)
const PROMPTS_ROOT = resolve(__dirname, '..')
const GENERATED_DIR = join(PROMPTS_ROOT, 'generated')

interface FileMetadata {
  filename: string
  path: string
  timestamp: Date | null
  age: number
  size: number
  formattedSize: string
}

interface FileToDelete extends FileMetadata {
  reason: string
}

interface CleanupOptions {
  keepCount?: number
  maxAgeDays?: number
  maxSizeMB?: number
  isDryRun?: boolean
  isVerbose?: boolean
}

interface CleanupCliOptions {
  keep?: string
  maxAge?: string
  maxSize?: string
  dryRun?: boolean
  verbose?: boolean
}

interface GetFileAgeOptions {
  filePath: string
}

interface GetFileSizeOptions {
  filePath: string
}

interface FormatFileSizeOptions {
  bytes: number
}

interface ParseTimestampOptions {
  filename: string
}

interface GetAgeIndicatorOptions {
  age: number
}

/**
 * Get age indicator based on file age
 */
function getAgeIndicator({ age }: GetAgeIndicatorOptions): string {
  if (age > 30) return chalk.red('🔴')
  if (age > 7) return chalk.yellow('⚠️')
  return chalk.green('🟢')
}

/**
 * Get file age in days
 */
function getFileAgeDays({ filePath }: GetFileAgeOptions): number {
  try {
    const stats = statSync(filePath)
    const now = new Date()
    const fileDate = new Date(stats.mtime)
    const diffTime = Math.abs(now.getTime() - fileDate.getTime())
    return Math.ceil(diffTime / (1000 * 60 * 60 * 24))
  } catch (error) {
    throw new Error(`Failed to get file age for ${filePath}: ${error instanceof Error ? error.message : 'Unknown error'}`)
  }
}

/**
 * Get file size in bytes
 */
function getFileSizeBytes({ filePath }: GetFileSizeOptions): number {
  try {
    const stats = statSync(filePath)
    return stats.size
  } catch (error) {
    throw new Error(`Failed to get file size for ${filePath}: ${error instanceof Error ? error.message : 'Unknown error'}`)
  }
}

/**
 * Format file size
 */
function formatFileSize({ bytes }: FormatFileSizeOptions): string {
  if (bytes === 0) return '0 B'

  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))

  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

/**
 * Parse timestamp from filename
 */
function parseTimestamp({ filename }: ParseTimestampOptions): Date | null {
  const match = filename.match(/repo_(\d{12})\.xml$/)
  if (!match) return null

  const timestamp = match[1]
  const year = timestamp.substring(0, 4)
  const month = timestamp.substring(4, 6)
  const day = timestamp.substring(6, 8)
  const hour = timestamp.substring(8, 10)
  const minute = timestamp.substring(10, 12)

  return new Date(`${year}-${month}-${day}T${hour}:${minute}:00`)
}

/**
 * Get generated XML files with metadata
 */
function getGeneratedFiles(): FileMetadata[] {
  try {
    const files = readdirSync(GENERATED_DIR)
      .filter(
        (file: string) =>
          file.startsWith('repo_') &&
          file.endsWith('.xml') &&
          file !== 'repo_latest.xml'
      )
      .map((file: string) => {
        const filePath = join(GENERATED_DIR, file)
        const timestamp = parseTimestamp({ filename: file })
        const fileSize = getFileSizeBytes({ filePath })
        return {
          filename: file,
          path: filePath,
          timestamp,
          age: getFileAgeDays({ filePath }),
          size: fileSize,
          formattedSize: formatFileSize({ bytes: fileSize }),
        }
      })
      .sort((a: FileMetadata, b: FileMetadata) => {
        if (!a.timestamp || !b.timestamp) return 0
        return b.timestamp.getTime() - a.timestamp.getTime()
      }) // Most recent first

    return files
  } catch (error) {
    console.log(chalk.yellow('📁 Generated directory not found'))
    return []
  }
}

/**
 * Clean up old files based on criteria
 */
function cleanupFiles(options: CleanupOptions = {}): void {
  const {
    keepCount = 5,
    maxAgeDays = 30,
    maxSizeMB = 100,
    isDryRun = false,
    isVerbose = false,
  } = options

  console.log(chalk.blue('🧹 Starting cleanup of generated XML files...'))

  const files = getGeneratedFiles()

  if (files.length === 0) {
    console.log(chalk.yellow('📄 No files to clean up'))
    return
  }

  const maxSizeBytes = maxSizeMB * 1024 * 1024
  const totalSize = files.reduce((sum, file) => sum + file.size, 0)
  let deletedCount = 0
  let deletedSize = 0

  console.log(
    chalk.blue(
      `📊 Found ${files.length} files (${formatFileSize({ bytes: totalSize })} total)`
    )
  )
  console.log(chalk.blue(`🔧 Cleanup criteria:`))
  console.log(chalk.blue(`   - Keep latest ${keepCount} files`))
  console.log(chalk.blue(`   - Delete files older than ${maxAgeDays} days`))
  console.log(chalk.blue(`   - Target total size: ${maxSizeMB} MB`))

  // Files to delete
  const filesToDelete: FileToDelete[] = [];

  // 1. Keep latest N files
  const filesToKeep = files.slice(0, keepCount);
  const candidatesForDeletion = files.slice(keepCount);

  // 2. Add files older than maxAgeDays to deletion list
  candidatesForDeletion.forEach(file => {
    if (file.age > maxAgeDays) {
      filesToDelete.push({
        ...file,
        reason: `older than ${maxAgeDays} days (${file.age} days)`,
      });
    }
  });

  // 3. If still over size limit, delete oldest files
  const remainingFiles = candidatesForDeletion.filter(
    file =>
      !filesToDelete.find(deleteFile => deleteFile.filename === file.filename)
  );
  let currentSize =
    filesToKeep.reduce((sum, file) => sum + file.size, 0) +
    remainingFiles.reduce((sum, file) => sum + file.size, 0);

  while (currentSize > maxSizeBytes && remainingFiles.length > 0) {
    const oldestFile = remainingFiles.pop(); // Remove oldest
    if (oldestFile) {
      filesToDelete.push({
        ...oldestFile,
        reason: `size limit exceeded (${formatFileSize({ bytes: currentSize })} > ${maxSizeMB} MB)`,
      });
      currentSize -= oldestFile.size;
    }
  }

  if (filesToDelete.length === 0) {
    console.log(chalk.green('✅ No files need to be deleted'));
    return;
  }

  console.log(chalk.yellow(`🗑️  Files to delete (${filesToDelete.length}):`));

  filesToDelete.forEach(file => {
    const date = file.timestamp?.toLocaleString() || 'Unknown date'
    console.log(
      chalk.yellow(
        `   ${file.filename} - ${date} - ${file.formattedSize} - ${file.reason}`
      )
    )

    if (!isDryRun) {
      try {
        unlinkSync(file.path)
        deletedCount++
        deletedSize += file.size
        if (isVerbose) {
          console.log(chalk.gray(`     ✅ Deleted`))
        }
      } catch (error) {
        console.log(
          chalk.red(`     ❌ Failed to delete: ${(error as Error).message}`)
        )
      }
    }
  })

  if (isDryRun) {
    console.log(
      chalk.blue(
        `🔍 Dry run complete - ${filesToDelete.length} files would be deleted`
      )
    )
    console.log(
      chalk.blue(
        `💾 ${formatFileSize({ bytes: filesToDelete.reduce((sum, f) => sum + f.size, 0) })} would be freed`
      )
    )
  } else {
    console.log(
      chalk.green(`✅ Cleanup complete - deleted ${deletedCount} files`)
    )
    console.log(
      chalk.green(`💾 Freed ${formatFileSize({ bytes: deletedSize })} of disk space`)
    )

    const remainingFiles = getGeneratedFiles()
    const remainingSize = remainingFiles.reduce(
      (sum, file) => sum + file.size,
      0
    )
    console.log(
      chalk.blue(
        `📊 Remaining: ${remainingFiles.length} files (${formatFileSize({ bytes: remainingSize })})`
      )
    )
  }
}

/**
 * Show statistics about generated files
 */
function showStats(): void {
  console.log(chalk.blue('📊 Generated files statistics:'))

  const files = getGeneratedFiles()

  if (files.length === 0) {
    console.log(chalk.yellow('📄 No files found'))
    return
  }

  const totalSize = files.reduce((sum, file) => sum + file.size, 0)
  const avgSize = totalSize / files.length
  const oldestFile = files[files.length - 1]
  const newestFile = files[0]

  console.log(chalk.blue(`📁 Total files: ${files.length}`))
  console.log(chalk.blue(`💾 Total size: ${formatFileSize({ bytes: totalSize })}`))
  console.log(chalk.blue(`📏 Average size: ${formatFileSize({ bytes: avgSize })}`))
  console.log(
    chalk.blue(`🕐 Oldest: ${oldestFile.filename} (${oldestFile.age} days ago)`)
  )
  console.log(
    chalk.blue(`🕑 Newest: ${newestFile.filename} (${newestFile.age} days ago)`)
  )

  // Size distribution
  console.log(chalk.blue('\n📊 Size distribution:'))
  files.forEach(file => {
    const date = file.timestamp?.toLocaleString() || 'Unknown date'
    const ageIndicator = getAgeIndicator({ age: file.age })
    console.log(
      `   ${ageIndicator} ${file.filename} - ${date} - ${file.formattedSize}`
    )
  })
}

// CLI setup
const program = new Command();

program
  .name('cleanup')
  .description('Clean up old generated XML files')
  .version('1.0.0');

program
  .command('run', { isDefault: true })
  .description('Clean up old files based on criteria')
  .option('-k, --keep <count>', 'Number of latest files to keep', '5')
  .option('-a, --max-age <days>', 'Maximum age in days', '30')
  .option('-s, --max-size <mb>', 'Maximum total size in MB', '100')
  .option(
    '-d, --dry-run',
    'Show what would be deleted without actually deleting'
  )
  .option('-v, --verbose', 'Show detailed output')
  .action((options: CleanupCliOptions) => {
    cleanupFiles({
      keepCount: parseInt(options.keep || '5'),
      maxAgeDays: parseInt(options.maxAge || '30'),
      maxSizeMB: parseInt(options.maxSize || '100'),
      isDryRun: Boolean(options.dryRun),
      isVerbose: Boolean(options.verbose),
    })
  })

program
  .command('stats')
  .description('Show statistics about generated files')
  .action(() => {
    showStats()
  })

program
  .command('list')
  .description('List all generated files with details')
  .alias('ls')
  .action(() => {
    const files = getGeneratedFiles()

    if (files.length === 0) {
      console.log(chalk.yellow('📄 No files found'))
      return
    }

    console.log(chalk.blue('📋 Generated XML files:'))
    files.forEach((file, index) => {
      const date = file.timestamp?.toLocaleString() || 'Unknown date'
      const isLatest = index === 0
      const prefix = isLatest ? chalk.green('🔗') : '  '
      const status = isLatest ? chalk.green(' (latest)') : ''
      const ageIndicator =
        file.age > 7
          ? chalk.yellow(' ⚠️')
          : file.age > 30
            ? chalk.red(' 🔴')
            : ''

      console.log(
        `${prefix} ${file.filename} - ${date} - ${file.formattedSize}${status}${ageIndicator}`
      )
    })
  })

program.parse()
