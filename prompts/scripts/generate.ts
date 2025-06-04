#!/usr/bin/env node

import { existsSync, mkdirSync } from 'fs'
import { join, dirname, resolve } from 'path'
import { fileURLToPath } from 'url'
import setupCLI from './partials/cli-setup.js'

const __filename = fileURLToPath(import.meta.url)
const __dirname = dirname(__filename)
const PROJECT_ROOT = resolve(__dirname, '../..')
const PROMPTS_ROOT = resolve(__dirname, '..')
const GENERATED_DIR = join(PROMPTS_ROOT, 'generated')
const CONFIG_PATH = join(PROMPTS_ROOT, 'config/repomix.config.json')
const PROFILES_PATH = join(PROMPTS_ROOT, 'config/profiles.json')

interface Paths {
  projectRoot: string
  promptsRoot: string
  generatedDir: string
  configPath: string
  profilesPath: string
}

interface EnsureDirectoryOptions {
  directoryPath: string
}

function ensureDirectoryExists({ directoryPath }: EnsureDirectoryOptions): void {
  if (!existsSync(directoryPath)) {
    mkdirSync(directoryPath, { recursive: true })
  }
}

// Ensure directories exist
ensureDirectoryExists({ directoryPath: GENERATED_DIR })

// Setup paths for CLI modules
const paths: Paths = {
  projectRoot: PROJECT_ROOT,
  promptsRoot: PROMPTS_ROOT,
  generatedDir: GENERATED_DIR,
  configPath: CONFIG_PATH,
  profilesPath: PROFILES_PATH,
}

// Setup and run CLI
const program = setupCLI(paths)

// Handle no arguments - default to run command
if (process.argv.length === 2) {
  program.parse(['node', 'generate.js', 'run'])
} else {
  program.parse()
}
