import { statSync, readFileSync } from 'fs'

interface TimestampOptions {
  date?: Date
}

interface FileSizeOptions {
  filePath: string
}

interface LineCountOptions {
  filePath: string
}

interface ParseSizeOptions {
  sizeString: string
}

/**
 * Generate timestamp in YYYYMMDDHHmm format
 */
export function generateTimestamp({ date = new Date() }: TimestampOptions = {}): string {
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  const hour = String(date.getHours()).padStart(2, '0')
  const minute = String(date.getMinutes()).padStart(2, '0')

  return `${year}${month}${day}${hour}${minute}`
}

/**
 * Get file size in human readable format
 */
export function getFileSize({ filePath }: FileSizeOptions): string {
  try {
    const stats = statSync(filePath)
    const bytes = stats.size

    if (bytes === 0) return '0 B'

    const k = 1024
    const sizes = ['B', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))

    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
  } catch (error) {
    throw new Error(`Failed to get file size for ${filePath}: ${error instanceof Error ? error.message : 'Unknown error'}`)
  }
}

/**
 * Count lines in a file
 */
export function countLines({ filePath }: LineCountOptions): number {
  try {
    const content = readFileSync(filePath, 'utf8')
    return content.split('\n').length
  } catch (error) {
    throw new Error(`Failed to count lines in ${filePath}: ${error instanceof Error ? error.message : 'Unknown error'}`)
  }
}

/**
 * Parse size string to bytes
 */
export function parseSize({ sizeString }: ParseSizeOptions): number {
  const units: Record<string, number> = {
    B: 1,
    KB: 1024,
    MB: 1024 * 1024,
    GB: 1024 * 1024 * 1024,
  }

  const match = sizeString.match(/^(\d+(?:\.\d+)?)\s*(B|KB|MB|GB)$/i)
  if (!match) {
    throw new Error(`Invalid size format: ${sizeString}`)
  }

  const value = parseFloat(match[1])
  const unit = match[2].toUpperCase()

  return value * units[unit]
}
