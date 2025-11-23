---
name: dependency-evaluator
description: Evaluates whether a programming language dependency should be used by analyzing maintenance activity, security posture, community health, documentation quality, dependency footprint, production adoption, license compatibility, API stability, and funding sustainability. Use when users are considering adding a new dependency, evaluating an existing dependency, or asking about package/library recommendations.
allowed-tools:
  - Read
  - Bash
  - Grep
  - Glob
  - WebFetch
  - WebSearch
---

# Dependency Evaluator Skill

This skill helps evaluate whether a programming language dependency should be added to a project by analyzing multiple quality signals and risk factors.

## Purpose

Making informed decisions about dependencies is critical for project health. A poorly chosen dependency can introduce security vulnerabilities, maintenance burden, and technical debt. This skill provides a systematic framework for evaluating dependencies before adoption.

## When to Use

Activate this skill when users:
- Ask about whether to use a specific package/library
- Want to evaluate a dependency before adding it
- Need to compare alternative packages
- Ask "should I use X library?"
- Want to assess the health of a dependency
- Mention adding a new npm/pip/cargo/gem/etc. package
- Ask about package recommendations for a use case

## Evaluation Framework

When evaluating a dependency, analyze these key signals:

### 1. Activity and Maintenance Patterns

**What to check:**
- Commit history and release cadence
- Time since last release
- How quickly critical bugs and security issues get addressed
- Issue triage responsiveness

**Commands to run:**
```bash
# Node.js - check publish dates and versions
npm view <package> time
npm view <package> versions --json

# Python - check package info
pip index versions <package>

# Rust - check crate info
cargo search <package> --limit 1

# Go - check module info
go list -m -versions <module>

# GitHub API - get repository activity (requires gh CLI)
gh api repos/{owner}/{repo} --jq '.pushed_at, .open_issues_count'
gh api repos/{owner}/{repo}/commits --jq '.[0].commit.author.date'
```

**Red flags:**
- No commits in 12+ months
- Sporadic bursts followed by long silences
- Large backlog of unaddressed issues
- No recent releases despite open issues

**Green flags:**
- Regular commits (even if small)
- Recent releases within last 6 months
- Responsive issue triage
- Active pull request merging

### 2. Security Posture

**What to check:**
- Security policy existence (SECURITY.md)
- Vulnerability disclosure process
- History of security advisories
- Response time to past CVEs
- Automated security scanning (Dependabot, Snyk badges)

**Commands to run:**
```bash
# Node.js - built-in audit
npm audit --json

# GitHub API - check security advisories
gh api repos/{owner}/{repo}/security-advisories --jq '.[].summary'

# Check for CVEs via GitHub Advisory Database
gh api graphql -f query='{ securityVulnerabilities(first: 5, package: "<package>") { nodes { advisory { summary severity } } } }'
```

**How to investigate:**
- Search for CVE history: `"<package-name>" CVE`
- Look for security badges in README (Snyk, Dependabot)
- Review GitHub Security tab
- Check OSV database: https://osv.dev

**Red flags:**
- No security policy
- Slow CVE response (30+ days)
- Multiple unpatched vulnerabilities
- No security scanning in CI

**Green flags:**
- Published security best practices
- Quick CVE patches (< 7 days)
- Security scanning enabled
- Bug bounty program

### 3. Community Health

**What to check:**
- Contributor diversity (single maintainer vs. team)
- PR merge rates and issue response times
- Stack Overflow activity
- Community forum engagement
- Bus factor

**Commands to run:**
```bash
# GitHub API - community health metrics
gh api repos/{owner}/{repo}/community/profile --jq '{health_percentage, files}'

# Get contributor stats
gh api repos/{owner}/{repo}/contributors --jq 'length'
gh api repos/{owner}/{repo}/stats/contributors --jq '.[].author.login'

# Check issue/PR response times
gh api repos/{owner}/{repo}/issues --jq '[.[] | select(.pull_request == null)] | .[0:5] | .[].created_at'
gh api repos/{owner}/{repo}/pulls --jq '.[0:5] | .[].created_at'
```

**Red flags:**
- Single maintainer with no backup
- PRs sitting for months unreviewed
- Hostile or dismissive responses to issues
- No community engagement

**Green flags:**
- Multiple active maintainers
- PRs reviewed within days
- Active Discord/Slack/forum community
- Good first issue labels for newcomers

### 4. Documentation Quality

**What to check:**
- Comprehensive API documentation
- Migration guides between versions
- Real-world usage examples
- Architectural decision records
- TypeScript types / type definitions

**Red flags:**
- Minimal or outdated README
- No API reference
- No migration guides for breaking changes
- Examples that don't work

**Green flags:**
- Comprehensive docs site
- Versioned documentation
- Clear upgrade guides
- Working examples and tutorials

### 5. Dependency Footprint

**What to check:**
- Number of transitive dependencies
- Size of dependency tree
- Quality of transitive dependencies

**Commands to run:**
```bash
# Node.js
npm ls --all <package>
npm pack <package> --dry-run  # Check package size

# Python
pip show <package>  # Shows direct dependencies in Requires field

# Rust
cargo tree -p <package>

# Go
go mod graph | grep <package>

# Java
mvn dependency:tree
```

**Red flags:**
- 50+ transitive dependencies
- Dependencies with known vulnerabilities
- Bloated bundle size for simple functionality
- Unmaintained transitive dependencies

**Green flags:**
- Minimal dependency tree
- Well-maintained dependencies
- Tree-shakeable / modular imports
- No native/binary dependencies (unless needed)

### 6. Production Adoption

**What to check:**
- Who's using this in production
- Download statistics and trends
- GitHub dependency graph (dependents)
- Mentions in tech blogs from reputable companies

**How to investigate:**
- Check npm weekly downloads / PyPI stats
- GitHub "Used by" section
- Search for "<package> production" in tech blogs

**Red flags:**
- High download counts but no visible production usage
- Only tutorial/example usage
- Declining download trends
- No notable adopters

**Green flags:**
- Used by large organizations (visible in GitHub dependents)
- Growing download trends
- Featured in production case studies
- Part of major frameworks' ecosystems

### 7. License Compatibility

**What to check:**
- License type (MIT, Apache-2.0, GPL, etc.)
- License compatibility with your project
- License stability (recent changes)
- Transitive license obligations

**Commands to run:**
```bash
# GitHub API - get license info
gh api repos/{owner}/{repo}/license --jq '.license.spdx_id'

# Check full dependency tree licenses via GitHub SBOM
gh api repos/{owner}/{repo}/dependency-graph/sbom --jq '.sbom.packages[].licenseConcluded'

# Node.js - check package.json license field
npm view <package> license

# Python - check PyPI metadata
pip show <package>  # Shows License field

# Rust - check Cargo.toml
cargo metadata --format-version 1 | jq '.packages[] | {name, license}'
```

**Red flags:**
- Copyleft licenses (GPL, AGPL) for proprietary projects
- No license specified
- Recent license changes
- Conflicting transitive licenses

**Green flags:**
- Permissive license (MIT, Apache-2.0, BSD)
- Clear license file
- Consistent licensing across dependencies

### 8. API Stability

**What to check:**
- Changelog for breaking changes
- Semantic versioning adherence
- Deprecation policy
- Breaking changes frequency in minor versions

**How to investigate:**
- Review CHANGELOG.md or GitHub releases
- Check version history for breaking change patterns

**Red flags:**
- Frequent breaking changes in minor versions
- No changelog or release notes
- No deprecation warnings before removal
- Unstable API (0.x version for years)

**Green flags:**
- Strict semver adherence
- Clear deprecation cycle
- Stable API (1.x+ with rare breaking changes)
- Migration codemods for major upgrades

### 9. Bus Factor and Funding

**What to check:**
- Organizational backing (CNCF, Apache, company sponsorship)
- OpenCollective or GitHub Sponsors presence
- Corporate contributor presence
- Full-time maintainers

**How to investigate:**
- Check for sponsor badges in README
- Look for corporate affiliations in contributor list
- Search for "<package> funding" or "<package> sponsor"

**Red flags:**
- Solo volunteer maintainer for critical package
- No funding mechanism
- Maintainer burnout signals
- Company backing withdrawn

**Green flags:**
- Foundation backing (Linux Foundation, Apache, etc.)
- Active sponsorship program
- Corporate maintainers
- Sustainable funding model

### 10. Ecosystem Momentum

**What to check:**
- Is the ecosystem migrating elsewhere?
- Framework/platform alignment
- Technology trend direction

**Red flags:**
- Ecosystem migrating to alternatives
- Deprecated by framework it supports
- Based on sunset technology

**Green flags:**
- Growing ecosystem adoption
- Aligned with platform direction
- Active plugin/extension ecosystem

## Output Format

Structure your evaluation report as:

```markdown
## Dependency Evaluation: <package-name>

### Summary
[2-3 sentence overall assessment with recommendation]

**Recommendation**: [ADOPT / EVALUATE FURTHER / AVOID]
**Risk Level**: [Low / Medium / High]
**Blockers Found**: [Yes/No]

### Blockers (if any)
[List any dealbreaker issues that should prevent adoption regardless of other scores]
- ⛔ [Blocker description]

### Evaluation Scores

| Signal | Score | Weight | Notes |
|--------|-------|--------|-------|
| Maintenance | X/5 | [H/M/L] | [brief note] |
| Security | X/5 | [H/M/L] | [brief note] |
| Community | X/5 | [H/M/L] | [brief note] |
| Documentation | X/5 | [H/M/L] | [brief note] |
| Dependency Footprint | X/5 | [H/M/L] | [brief note] |
| Production Adoption | X/5 | [H/M/L] | [brief note] |
| License | X/5 | [H/M/L] | [brief note] |
| API Stability | X/5 | [H/M/L] | [brief note] |
| Funding/Sustainability | X/5 | [H/M/L] | [brief note] |
| Ecosystem Momentum | X/5 | [H/M/L] | [brief note] |

**Weighted Score**: X/50 (adjusted for dependency criticality)

### Key Findings

#### Strengths
- [Strength 1]
- [Strength 2]

#### Concerns
- [Concern 1]
- [Concern 2]

### Alternatives Considered
[If applicable, mention alternatives worth evaluating]

### Recommendation Details
[Detailed reasoning for the recommendation]

### If You Proceed
[Specific advice if they decide to use the dependency]
- Version pinning strategy
- Monitoring recommendations
- Fallback plan
```

## Scoring Weights

Adjust signal weights based on dependency type:

| Signal | Critical Dep | Standard Dep | Dev Dep |
|--------|-------------|--------------|---------|
| Security | High | Medium | Low |
| Maintenance | High | Medium | Medium |
| Funding | High | Low | Low |
| License | High | High | Medium |
| API Stability | Medium | Medium | High |
| Documentation | Medium | Medium | Medium |
| Community | Medium | Medium | Low |
| Dependency Footprint | Medium | Low | Low |
| Production Adoption | Medium | Medium | Low |
| Ecosystem Momentum | Low | Medium | Low |

**Blocker Override**: Any blocker issue results in AVOID recommendation regardless of scores.

## Risk-Adjusted Evaluation

Weight signals based on dependency criticality:

**Critical Dependencies** (auth, security, data handling):
- Prioritize: Security, Maintenance, Funding
- Higher bar for all signals
- Consider cost of forking if maintenance stops

**Standard Dependencies** (utilities, formatting):
- Balance all signals equally
- Lower risk tolerance acceptable
- Easier to replace if needed

**Development Dependencies** (testing, linting):
- Prioritize: Maintenance, API Stability
- Lower security concerns (not in production)
- Focus on developer experience

## Ecosystem-Specific Considerations

Different language ecosystems have different norms and risks:

### Node.js / npm
- **left-pad risk**: Tiny single-function packages carry disproportionate supply chain risk
- **Prefer**: Packages with minimal dependencies, or well-established micro-utilities
- **Watch for**: Packages with hundreds of transitive dependencies for simple tasks
- **Tool**: Use `npm ls --all` to visualize the full tree before committing

### Go
- **Philosophy**: Stdlib-first, fewer dependencies is idiomatic
- **Prefer**: Standard library solutions when available
- **Watch for**: Packages that wrap stdlib with minimal added value
- **Strength**: Strong tooling (`go mod`, `go mod graph`) makes dependency management safer

### Rust / Cargo
- **Strength**: Cargo's built-in tooling (`cargo tree`, `cargo metadata`) provides excellent visibility
- **Prefer**: Crates with `#![forbid(unsafe_code)]` for non-performance-critical code
- **Watch for**: Crates pulling in many proc-macro dependencies (slow compile times)
- **Culture**: Strong emphasis on correctness, good documentation norms

### Python / PyPI
- **Risk**: PyPI has had notable supply chain attacks (typosquatting)
- **Prefer**: Packages from known maintainers, check for signed releases
- **Watch for**: Packages with names similar to popular packages
- **Tool**: Use `pip show` and check GitHub for vulnerability history

### Ruby / RubyGems
- **Culture**: Convention over configuration, gems often do a lot
- **Watch for**: Gems that monkey-patch core classes extensively
- **Prefer**: Well-documented gems with clear upgrade paths

### Java / Maven
- **Strength**: Mature ecosystem with established governance
- **Watch for**: Dependency hell from version conflicts
- **Tool**: Use `mvn dependency:tree` to understand the full graph

## Critical Red Flags (Dealbreakers)

These issues should trigger an automatic AVOID recommendation:

### Supply Chain Risks
- ⛔ **Typosquatting**: Package name suspiciously similar to a popular package
- ⛔ **Compiled binaries without source**: Binary blobs in repo without build instructions
- ⛔ **Sudden ownership transfer**: Recent transfer to unknown maintainer
- ⛔ **Install scripts with network calls**: postinstall scripts that download external code

### Maintainer Behavior
- ⛔ **Ransom behavior**: Maintainer demanding payment to fix security issues
- ⛔ **Protest-ware**: Code that performs actions based on political/geographic conditions
- ⛔ **Intentional sabotage history**: Any history of deliberately breaking the package

### Security Issues
- ⛔ **Active exploitation**: Known vulnerability being actively exploited in the wild
- ⛔ **Credentials in source**: API keys, passwords, or secrets in the repository
- ⛔ **Disabled security features**: Package disables security features without clear reason

### Legal Issues
- ⛔ **License violation**: Package includes code that violates its stated license
- ⛔ **No license**: No license file means all rights reserved (legally risky)
- ⛔ **License change without notice**: Recent sneaky license change to restrictive terms

## When to Reconsider Adding a Dependency

Before adding any dependency, ask these questions:

### Is the dependency actually needed?

**Write it yourself if:**
- The functionality is < 50 lines of straightforward code
- You only need a small subset of the package's features
- The package adds significant weight for minimal functionality
- Example: Don't add a 500KB package to pad strings or check if a number is odd

**Use the dependency if:**
- The problem domain is complex (crypto, date/time, parsing)
- Correctness is critical and well-tested implementations exist
- The functionality would require significant ongoing maintenance
- You need the full feature set, not just one function

### Cost-Benefit Analysis

```
Dependency Cost = (security risk) + (maintenance burden) + (bundle size) + (upgrade friction)
Dependency Value = (time saved) + (correctness gained) + (features needed) + (community support)

Only add if: Value significantly exceeds Cost
```

### Alternatives to Full Dependencies

1. **Copy the code**: For small, stable utilities, copy the source (with attribution)
2. **Polyfills**: Use targeted polyfills instead of full compatibility libraries
3. **Tree-shaking imports**: Use `import { specific } from 'package'` not `import *`
4. **Peer dependencies**: Let the consumer provide shared dependencies
5. **Optional dependencies**: Make heavy dependencies optional for users who need them

## Example Invocations

- "Should I use lodash for this project?"
- "Evaluate the axios package for HTTP requests"
- "Is date-fns a good choice for date handling?"
- "Compare express vs fastify vs koa"
- "Should I add this dependency: react-query"
- "Is this package safe to use in production?"

## Guidelines

### Be Evidence-Based
- Always cite specific data points
- Include version numbers and dates
- Reference actual metrics (downloads, contributors, issues)

### Be Balanced
- Acknowledge both strengths and weaknesses
- Don't dismiss packages for single issues
- Consider the specific use case context

### Be Actionable
- Provide clear recommendation
- Include next steps
- Suggest alternatives when appropriate

### Consider Context
- A CLI color library needs different scrutiny than an auth library
- Development dependencies have different risk profiles
- Project scale affects acceptable risk

## Privacy and Security

- Verify license compatibility before recommending
- Consider supply chain risks for sensitive applications
- Note when packages require additional security review
