// Common types for the prompts project

export interface Profile {
  name: string;
  description: string;
  maxSize: string;
  include: string[];
  exclude?: string[];
}

export interface ProfileConfig {
  [profileName: string]: Profile;
}

export interface GenerationOptions {
  profile?: string;
  verbose?: boolean;
  dryRun?: boolean;
  outputDir?: string;
}

export interface FileInfo {
  path: string;
  size: number;
  created: Date;
  profile: string;
}

export interface CleanupOptions {
  keep?: number;
  maxAge?: number;
  maxSize?: number;
  dryRun?: boolean;
  verbose?: boolean;
}

export interface RepomixConfig {
  output: {
    filePath: string;
    style: string;
    headerText?: string;
    instructionFilePath?: string;
    removeComments: boolean;
    removeEmptyLines: boolean;
    topFilesLength: number;
    showLineNumbers: boolean;
    copyToClipboard: boolean;
  };
  include: string[];
  ignore: {
    useGitignore: boolean;
    useDefaultPatterns: boolean;
    customPatterns: string[];
  };
  security: {
    enableSecurityCheck: boolean;
  };
}

// Utility types
export type LogLevel = 'info' | 'warn' | 'error' | 'debug';

export interface Logger {
  info(_message: string, ..._args: any[]): void;
  warn(_message: string, ..._args: any[]): void;
  error(_message: string, ..._args: any[]): void;
  debug(_message: string, ..._args: any[]): void;
}

// Command line interface types
export interface CLICommand {
  name: string;
  description: string;
  options?: CLIOption[];
  action: (..._args: any[]) => Promise<void> | void;
}

export interface CLIOption {
  flags: string;
  description: string;
  defaultValue?: any;
}
