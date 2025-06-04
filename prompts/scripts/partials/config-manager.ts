import { readFileSync, existsSync } from 'fs'

export interface Profile {
  description: string
  maxTotalSize?: string
  include?: string[]
  exclude?: string[]
}

interface ProfilesData {
  profiles: Record<string, Profile>
}

export interface BaseConfig {
  include?: string[]
  ignore?: {
    customPatterns?: string[]
  }
  maxTotalSize?: string
  [key: string]: unknown
}

interface LoadProfilesOptions {
  profilesPath: string
}

interface CreateProfileConfigOptions {
  profile: Profile
  baseConfig: BaseConfig
}

interface LoadBaseConfigOptions {
  configPath: string
}

interface ValidationError extends Error {
  code: 'FILE_NOT_FOUND' | 'INVALID_JSON' | 'MISSING_PROFILES'
}

function createValidationError(message: string, code: ValidationError['code']): ValidationError {
  const error = new Error(message) as ValidationError
  error.code = code
  return error
}

function validateProfilesData(data: unknown): ProfilesData {
  if (!data || typeof data !== 'object' || !('profiles' in data)) {
    throw createValidationError('Invalid profiles.json: missing "profiles" key', 'MISSING_PROFILES')
  }
  return data as ProfilesData
}

/**
 * Load and validate profiles configuration
 */
export function loadProfiles({ profilesPath }: LoadProfilesOptions): ProfilesData {
  if (!existsSync(profilesPath)) {
    throw createValidationError(`Profiles configuration not found: ${profilesPath}`, 'FILE_NOT_FOUND')
  }

  try {
    const content = readFileSync(profilesPath, 'utf8')
    const data = JSON.parse(content) as unknown
    return validateProfilesData(data)
  } catch (error) {
    if (error instanceof SyntaxError) {
      throw createValidationError(`JSON syntax error in profiles.json: ${error.message}`, 'INVALID_JSON')
    }
    throw error
  }
}

/**
 * Create dynamic repomix configuration based on profile
 */
export function createProfileConfig({ profile, baseConfig }: CreateProfileConfigOptions): BaseConfig {
  const config = { ...baseConfig }

  // Apply profile-specific settings
  if (profile.maxTotalSize) {
    config.maxTotalSize = profile.maxTotalSize
  }

  if (profile.include && profile.include.length > 0) {
    config.include = profile.include
  }

  if (profile.exclude) {
    if (!config.ignore) config.ignore = {}
    if (!config.ignore.customPatterns) config.ignore.customPatterns = []
    config.ignore.customPatterns = [
      ...config.ignore.customPatterns,
      ...profile.exclude,
    ]
  }

  return config
}

/**
 * Load base configuration from config file
 */
export function loadBaseConfig({ configPath }: LoadBaseConfigOptions): BaseConfig {
  try {
    const content = readFileSync(configPath, 'utf8')
    return JSON.parse(content) as BaseConfig
  } catch (error) {
    throw new Error(`Failed to load base config from ${configPath}: ${error instanceof Error ? error.message : 'Unknown error'}`)
  }
}
