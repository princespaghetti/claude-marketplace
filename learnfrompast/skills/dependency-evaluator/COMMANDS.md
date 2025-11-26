# Dependency Evaluation Commands Reference

This file contains all ecosystem-specific commands for gathering dependency information. Organize your investigation by the signals you're evaluating, then run the appropriate commands for your package's ecosystem.

## Table of Contents

### By Signal
- [1. Activity and Maintenance Patterns](#1-activity-and-maintenance-patterns)
- [2. Security Posture](#2-security-posture)
- [3. Community Health](#3-community-health)
- [4. Documentation Quality](#4-documentation-quality)
- [5. Dependency Footprint](#5-dependency-footprint)
- [6. Production Adoption](#6-production-adoption)
- [7. License Compatibility](#7-license-compatibility)
- [8-10. Other Signals](#8-10-other-signals)

### By Ecosystem
- [Node.js / npm Complete Checklist](#nodejs--npm-complete-checklist)
- [Python / PyPI Complete Checklist](#python--pypi-complete-checklist)
- [Rust / Cargo Complete Checklist](#rust--cargo-complete-checklist)
- [Go Complete Checklist](#go-complete-checklist)
- [Java / Maven Complete Checklist](#java--maven-complete-checklist)

### Tips
- [Command Usage Tips](#tips-for-effective-command-usage)

---

## Quick Command Lookup by Signal

### 1. Activity and Maintenance Patterns

#### Node.js / npm
```bash
# Check publish dates and version history
npm view <package> time

# List all published versions
npm view <package> versions --json
```

#### Python / PyPI
```bash
# Check available versions
pip index versions <package>
```

#### Rust / Cargo
```bash
# Search for crate information
cargo search <package> --limit 1
```

#### Go
```bash
# Check module versions
go list -m -versions <module>
```

#### GitHub (all ecosystems)
```bash
# Get repository activity (requires gh CLI)
gh api repos/{owner}/{repo} --jq '.pushed_at, .open_issues_count'

# Get latest commit date
gh api repos/{owner}/{repo}/commits --jq '.[0].commit.author.date'
```

### 2. Security Posture

#### Node.js / npm
```bash
# Run built-in security audit
npm audit --json
```

#### GitHub Security
```bash
# Check security advisories for a repository
gh api repos/{owner}/{repo}/security-advisories --jq '.[].summary'

# Check for CVEs via GitHub Advisory Database
gh api graphql -f query='{ securityVulnerabilities(first: 5, package: "<package>") { nodes { advisory { summary severity } } } }'
```

#### Manual Investigation
- Search for CVEs: `"<package-name>" CVE`
- Check OSV database: https://osv.dev
- Look for security badges in README (Snyk, Dependabot)
- Review GitHub Security tab

### 3. Community Health

#### GitHub Community Metrics
```bash
# Get community health score and files (returns health_percentage 0-100)
gh api repos/{owner}/{repo}/community/profile --jq '{health_percentage, description, files}'

# Check if security policy exists
gh api repos/{owner}/{repo}/contents/SECURITY.md --jq '.name' 2>/dev/null || echo "No SECURITY.md"

# Get contributor count
gh api repos/{owner}/{repo}/contributors --jq 'length'

# Get top contributors
gh api repos/{owner}/{repo}/stats/contributors --jq 'sort_by(.total) | reverse | .[0:5] | .[].author.login'

# Check recent issue activity (are maintainers responding?)
gh api repos/{owner}/{repo}/issues --jq '[.[] | select(.pull_request == null)] | .[0:5] | .[] | {title, created_at, comments}'

# Check PR merge velocity
gh api repos/{owner}/{repo}/pulls?state=closed --jq '.[0:10] | .[] | {title, created_at, merged_at}'
```

#### Interpreting Community Health Metrics
- `health_percentage` > 70 is good; < 50 suggests missing community files
- Multiple contributors (not just 1-2) indicates healthier bus factor
- Issues with comments show maintainer engagement; many 0-comment issues is a red flag
- PRs merged within days/weeks is healthy; months suggests slow maintenance

### 4. Documentation Quality

No specific commands - manually review:
- README comprehensiveness
- API documentation site
- Migration guides between versions
- Working examples and tutorials
- TypeScript type definitions (for JS/TS packages)

### 5. Dependency Footprint

#### Node.js / npm
```bash
# View full dependency tree
npm ls --all <package>

# Check package size (dry-run of pack)
npm pack <package> --dry-run
```

#### Python / PyPI
```bash
# Shows direct dependencies in Requires field
pip show <package>
```

#### Rust / Cargo
```bash
# Display dependency tree
cargo tree -p <package>
```

#### Go
```bash
# Show module dependency graph
go mod graph | grep <package>
```

#### Java / Maven
```bash
# Display dependency tree
mvn dependency:tree
```

#### Interpreting Dependency Trees
**What to look for:**
- **Total count**: Flag packages with >50 transitive dependencies for simple functionality
- **Duplicate versions**: Multiple versions of the same package (e.g., `lodash@4.17.21` and `lodash@4.17.15`) indicate potential conflicts
- **Deep nesting**: Dependencies 5+ levels deep are harder to audit and update
- **Abandoned dependencies**: Transitive deps that haven't been updated in years
- **Size vs. function**: A 500KB+ package for a simple utility is a smell

### 6. Production Adoption

#### Package Statistics
- **npm**: Check weekly downloads on npmjs.com or via `npm view <package>`
- **PyPI**: Check download stats on pypi.org package page
- **crates.io**: View download counts on crates.io
- **GitHub**: Check "Used by" count on repository page

#### Investigation Methods
```bash
# GitHub dependents (who uses this package)
# Visit: https://github.com/{owner}/{repo}/network/dependents

# Search for production usage mentions
# Web search: "<package> production" or "<package> case study"
```

### 7. License Compatibility

#### GitHub License
```bash
# Get license information
gh api repos/{owner}/{repo}/license --jq '.license.spdx_id'

# Check full dependency tree licenses via SBOM
gh api repos/{owner}/{repo}/dependency-graph/sbom --jq '.sbom.packages[].licenseConcluded'
```

#### Node.js / npm
```bash
# Check package.json license field
npm view <package> license
```

#### Python / PyPI
```bash
# Shows License field
pip show <package>
```

#### Rust / Cargo
```bash
# Check license from Cargo.toml
cargo metadata --format-version 1 | jq '.packages[] | {name, license}'
```

### 8. API Stability

No specific commands - manually review:
- CHANGELOG.md or GitHub releases
- Version history for breaking change patterns
- Adherence to semantic versioning
- Deprecation warnings before removal

### 9. Bus Factor and Funding

No specific commands - manually investigate:
- Check for sponsor badges in README
- Look for OpenCollective or GitHub Sponsors links
- Search "<package> funding" or "<package> sponsor"
- Check for organizational backing (CNCF, Apache, company sponsorship)
- Review contributor affiliations in GitHub profile

### 10. Ecosystem Momentum

No specific commands - research:
- Check if ecosystem is migrating to alternatives
- Verify framework/platform alignment
- Search for ecosystem trend discussions
- Review plugin/extension ecosystem activity

## Command Reference by Ecosystem

### Node.js / npm Complete Checklist

```bash
# Package metadata and history
npm view <package> time
npm view <package> versions --json
npm view <package> license

# Dependency analysis
npm ls --all <package>
npm pack <package> --dry-run

# Security
npm audit --json

# If GitHub repo is known
gh api repos/{owner}/{repo} --jq '.pushed_at, .open_issues_count'
gh api repos/{owner}/{repo}/community/profile
gh api repos/{owner}/{repo}/license --jq '.license.spdx_id'
```

### Python / PyPI Complete Checklist

```bash
# Package information
pip index versions <package>
pip show <package>

# If GitHub repo is known
gh api repos/{owner}/{repo} --jq '.pushed_at, .open_issues_count'
gh api repos/{owner}/{repo}/community/profile
gh api repos/{owner}/{repo}/security-advisories
```

### Rust / Cargo Complete Checklist

```bash
# Crate information
cargo search <package> --limit 1
cargo tree -p <package>
cargo metadata --format-version 1 | jq '.packages[] | select(.name=="<package>") | {name, license, version}'

# If GitHub repo is known
gh api repos/{owner}/{repo} --jq '.pushed_at, .open_issues_count'
gh api repos/{owner}/{repo}/community/profile
```

### Go Complete Checklist

```bash
# Module information
go list -m -versions <module>
go mod graph | grep <module>

# If GitHub repo is known (most Go modules are on GitHub)
gh api repos/{owner}/{repo} --jq '.pushed_at, .open_issues_count'
gh api repos/{owner}/{repo}/community/profile
gh api repos/{owner}/{repo}/security-advisories
```

### Java / Maven Complete Checklist

```bash
# Dependency tree
mvn dependency:tree

# If GitHub repo is known
gh api repos/{owner}/{repo} --jq '.pushed_at, .open_issues_count'
gh api repos/{owner}/{repo}/community/profile
gh api repos/{owner}/{repo}/license --jq '.license.spdx_id'
```

## Tips for Effective Command Usage

### Run Commands in Parallel
When gathering data for multiple signals, run independent commands simultaneously to save time:
```bash
# Example: Run these in parallel
gh api repos/{owner}/{repo} &
gh api repos/{owner}/{repo}/community/profile &
gh api repos/{owner}/{repo}/contributors &
wait
```

### Save Command Output
For complex evaluations, save output to files for reference:
```bash
npm view <package> time > /tmp/npm-history.json
gh api repos/{owner}/{repo}/issues > /tmp/github-issues.json
```

### Handle Errors Gracefully
Some commands may fail if data isn't available:
```bash
# Use || to provide fallback messages
gh api repos/{owner}/{repo}/contents/SECURITY.md 2>/dev/null || echo "No security policy found"
```

### Find GitHub Repository
If you only have a package name, find its repository:
```bash
# For npm packages
npm view <package> repository.url

# For PyPI packages
pip show <package> | grep "Home-page"

# For cargo crates
# Visit crates.io and check the repository link
```
