# AI Prompt Generation Workflow

Enhanced workflow for converting repository contents into XML files using [Repomix](https://repomix.com) for AI prompt creation. Now with **profile-based size control** to fit AI context windows, improved tooling, better organization, and pnpm support.

## ✨ New Features

### 🎯 Profile-based Generation
- **minimal** (< 20KB): Core application files only - perfect for context windows
- **core** (< 50KB): Essential application structure including tests
- **docs** (< 30KB): Documentation and configuration only
- **full** (< 100KB): Complete codebase excluding assets

### 📊 Size Control & Warnings
- Automatic size estimation
- Context window compatibility warnings
- Pre-generation size checks

## 🏗️ Directory Structure

```
prompts/
├── package.json              # Node.js dependencies (pnpm)
├── pnpm-lock.yaml           # pnpm lockfile
├── setup.sh                 # Setup script
├── config/                   # Configuration files
│   └── repomix.config.json  # Repomix configuration
├── scripts/                  # Generation and management scripts
│   ├── generate.js          # Main generation script
│   └── cleanup.js           # File cleanup management
├── generated/                # Generated XML files
│   ├── repo_202506021625.xml # Timestamped XML files
│   └── repo_202506021705.xml # More timestamped files
└── README.md                # This file
```

## 🚀 Quick Start

### 1. Setup (One-time)
```bash
cd prompts/
pnpm install
# or use the setup script
./setup.sh
```

### 2. Generate Repository XML

```bash
# 🎯 NEW: Generate ALL profiles at once (recommended)
pnpm run generate
# or
node scripts/generate.js run

# This generates 4 optimized files:
# - minimal: 12KB - Core application files only
# - core: 43KB - Application structure + tests
# - docs: 14KB - Documentation and configuration
# - full: 189KB - Complete codebase (may be large)

# Generate specific profile only
pnpm run generate -- --profile minimal   # Just the minimal profile
pnpm run generate -- --profile core      # Just the core profile

# With verbose output for all profiles
pnpm run generate -- --verbose

# Dry run to see what would be generated
pnpm run generate -- --dry-run

# Estimate sizes before generation
pnpm run generate estimate               # All profiles
pnpm run generate estimate --profile minimal  # Specific profile
```

### 3. View Available Profiles

```bash
# List all available profiles
node scripts/generate.js profiles

# Output:
# minimal    - Core application files only (< 20KB) (20KB)
# core       - Essential application structure (< 50KB) (50KB)
# full       - Complete codebase excluding assets (< 100KB) (100KB)
# docs       - Documentation and configuration only (< 30KB) (30KB)
```

### 4. List Generated Files

```bash
# List all generated files (grouped by profile)
pnpm run generate list
# or
node scripts/generate.js list

# Filter by specific profile
node scripts/generate.js list --profile minimal

# Get path to latest file
node scripts/generate.js latest --profile minimal
```

### 4. Get Latest File Path
```bash
pnpm run generate latest
```

## 🧹 File Management

### Cleanup Old Files
```bash
# Basic cleanup (keeps 5 latest, deletes files older than 30 days)
pnpm run cleanup

# Custom settings
pnpm run cleanup -- --keep 10 --max-age 60 --max-size 200

# Dry run to see what would be deleted
pnpm run cleanup -- --dry-run

# Show statistics
pnpm run cleanup stats
```

### Cleanup Options
- `--keep <count>`: Number of latest files to keep (default: 5)
- `--max-age <days>`: Maximum age in days (default: 30)
- `--max-size <mb>`: Maximum total size in MB (default: 100)
- `--dry-run`: Preview deletions without executing
- `--verbose`: Show detailed output

## 📊 Enhanced Features

### Advanced Configuration
The [`repomix.config.json`](config/repomix.config.json:1) provides:
- Custom ignore patterns for better file filtering
- Security checks to prevent sensitive data exposure
- File size limits and optimization settings
- Enhanced XML output formatting

### Improved File Management
- **Automatic cleanup**: Prevents disk space issues
- **File statistics**: Size, age, and metadata tracking
- **Smart retention**: Keeps important files, removes old ones
- **Progress reporting**: Verbose output with file information

### AI Prompt Templates
Ready-to-use prompt patterns for:
- Code quality reviews
- Security audits
- Performance analysis
- Feature implementation guidance
- Bug investigation

## 💡 AI Prompt Usage

### 1. Generate XML
```bash
cd prompts/
pnpm run generate
```

### 2. Create Your Prompt
Use these common prompt patterns based on your needs:
- Code Quality Review
- Feature Implementation
- Bug Investigation
- Performance Analysis
- Security Audit

### 3. Copy Content
```bash
# Copy latest XML to clipboard (macOS)
cat generated/repo_202506021705.xml | pbcopy

# View file info
ls -la generated/
```

## 🔧 Configuration Details

### Repomix Configuration
Key settings in [`config/repomix.config.json`](config/repomix.config.json:1):
- **Output format**: XML with line numbers and headers
- **Security filtering**: Prevents credential exposure
- **File exclusions**: Ignores logs, dependencies, temporary files
- **Size limits**: Prevents oversized outputs

### Ignored Patterns
Automatically excludes:
- Dependencies (`node_modules/`, `vendor/bundle/`)
- Generated files (`*.lock`, `db/schema.rb`)
- Logs and temporary files (`log/`, `tmp/`)
- Environment files (`.env.*`, `config/master.key`)
- Build artifacts (`.terraform/`, `coverage/`)

## 📈 Migration Benefits

### From Bash to Node.js/pnpm
- ✅ **Faster execution**: pnpm package resolution
- ✅ **Better error handling**: Detailed error messages and stack traces
- ✅ **Enhanced features**: File statistics, cleanup automation
- ✅ **Cross-platform**: Works on Windows, macOS, Linux
- ✅ **Maintainable**: Modular, testable code structure

### Improved Organization
- ✅ **Separated concerns**: Config, scripts, templates, generated files
- ✅ **Template system**: Ready-to-use AI prompt examples
- ✅ **Automated cleanup**: Prevents disk space issues
- ✅ **Better documentation**: Clear usage examples and options

## 🔍 File Statistics

Generated XML files include:
- Complete repository structure and content
- File metadata and statistics
- Security scan results
- Token count estimates for AI models

## 📝 Best Practices

### Security
- ⚠️ **Review generated XML** before sharing
- ⚠️ **Check for sensitive data** (API keys, passwords)
- ✅ **Use security filtering** (enabled by default)
- ✅ **Keep .gitignore updated** for exclusions

### Performance
- 🔧 **Regular cleanup**: Run cleanup weekly
- 🔧 **Monitor file sizes**: Large repositories may need filtering
- 🔧 **Use dry-run first**: Test settings before generation
- 🔧 **Optimize ignore patterns**: Add project-specific exclusions

### AI Prompting
- 📝 **Use specific templates** for better results
- 📝 **Include context** about your goals
- 📝 **Split large files** if needed for AI model limits
- 📝 **Reference line numbers** when discussing specific code

## 🆘 Troubleshooting

### Common Issues
1. **"repomix not found"**: Run `pnpm install` in `prompts/` directory
2. **Permission errors**: Check file permissions on generated files
3. **Large file sizes**: Adjust ignore patterns in config
4. **Script execution errors**: Ensure Node.js scripts have proper permissions

### Getting Help
```bash
# Show command help
node scripts/generate.js --help
node scripts/cleanup.js --help

# Show file statistics
pnpm run cleanup stats

# Verbose output for debugging
pnpm run generate -- --verbose
```

## 🔗 References

- [Repomix Documentation](https://repomix.com/guide/configuration)
- [pnpm Documentation](https://pnpm.io/)
- [Node.js File System API](https://nodejs.org/api/fs.html)
