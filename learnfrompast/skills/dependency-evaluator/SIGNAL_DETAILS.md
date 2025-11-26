# Evaluation Signal Details

This file provides deep guidance for each of the 10 evaluation signals used in dependency assessment. For each signal, you'll find what it measures, how to investigate it, how to interpret results, and what constitutes red vs. green flags.

## Assessment Philosophy: Ecosystem-Relative Evaluation

**Use comparative assessment rather than absolute thresholds.** What's "normal" varies significantly by:
- **Ecosystem**: npm vs PyPI vs Cargo vs Go have different cultural norms
- **Package type**: Frameworks vs utilities vs libraries have different expectations
- **Maturity**: New packages vs mature stable packages have different activity patterns

**Throughout this guide:**
- Red/green flags are framed as comparisons to ecosystem norms
- Specific numbers provide context, not rigid cutoffs
- "Significantly below/above norm" means outlier for package category in its ecosystem
- Always compare package to similar packages in same ecosystem before scoring

See [ECOSYSTEM_GUIDES.md](./ECOSYSTEM_GUIDES.md) for ecosystem-specific baselines and norms.

## 1. Activity and Maintenance Patterns

### What This Signal Measures
The frequency and consistency of package updates, bug fixes, and maintainer responsiveness. Active maintenance indicates the package is being improved and issues are being addressed.

### What to Check
- Commit history and release cadence
- Time since last release
- How quickly critical bugs and security issues get addressed
- Issue triage responsiveness
- Consistency of maintenance over time

### Ecosystem-Relative Assessment

**Compare package activity against ecosystem norms rather than absolute thresholds.** What's "normal" varies significantly by language, package type, and maturity.

**Release Cadence Comparison:**
- **Red flag**: Release cadence significantly below ecosystem norm for similar packages
  - npm actively-developed packages: Most release monthly or more; quarterly is typical minimum
  - Rust crates: Bi-monthly to quarterly is common; annual can be acceptable for stable crates
  - Python packages: Monthly to quarterly for active development
  - Go modules: Quarterly common; infrequent releases normal due to stdlib-first culture
- **Assessment**: Is this package's release pattern an outlier for its category within its ecosystem?

**Commit Activity Comparison:**
- **Red flag**: Commit activity has ceased while similar packages maintain activity
  - Look at comparable packages in same ecosystem/category
  - Mature stable libraries may legitimately have low commit frequency
  - New/actively-developed tools should show regular activity
- **Green flag**: Inactivity with zero open security issues may indicate package is "done" (complete, not abandoned)
- **Context**: Protocol implementations, math utilities, stable APIs may need few updates

**Issue Response Comparison:**
- **Red flag**: Issue response time significantly slower than ecosystem norm
  - npm: Hours to days typical for popular packages; weeks acceptable
  - Smaller ecosystems: Days to weeks is normal
  - Compare: Are issues being triaged, or ignored completely?
- **Critical**: Unaddressed security issues override all activity metrics

**Backlog Assessment:**
- **Red flag**: Issue backlog growing while similar packages maintain healthy triage
  - npm popular packages: 20-50 open issues may be normal if being triaged
  - Smaller projects: 10+ untriaged issues concerning
  - Key: Are maintainers responding, even if not immediately fixing?

### Red Flags (Ecosystem-Relative)
- Release cadence significantly below ecosystem median for package category
- Commit activity ceased while comparable packages remain active
- Issue response time far slower than ecosystem norm
- Growing backlog with zero maintainer engagement
- Unaddressed security issues (absolute red flag regardless of ecosystem)

### Green Flags (Ecosystem-Relative)
- Release cadence at or above ecosystem median
- Commit activity appropriate for package maturity and ecosystem
- Issue triage responsiveness comparable to or better than ecosystem norm
- Active PR review and merging
- Security issues addressed promptly even if feature development is slow

### Common False Positives
- **Low activity in mature libraries**: A date library or cryptography implementation that hasn't changed in years might be complete, not abandoned. Check if issues are triaged and security updates still happen.
- **Seasonal patterns**: Academic or side-project packages may have irregular but acceptable maintenance patterns
- **Small scope packages**: A package that does one thing well may legitimately need few updates

## 2. Security Posture

### What This Signal Measures
How the project handles security vulnerabilities, whether it has established security practices, and its history of security issues.

### What to Check
- Security policy existence (SECURITY.md)
- Vulnerability disclosure process
- History of security advisories and CVEs
- Response time to past vulnerabilities
- Automated security scanning (Dependabot, Snyk badges)
- Proactive security measures

### How to Investigate
- Search for CVE history: `"<package-name>" CVE`
- Look for security badges in README (Snyk, Dependabot)
- Review GitHub Security tab
- Check OSV database: https://osv.dev
- Run ecosystem security tools (npm audit, etc.)

### Red Flags
- No security policy or disclosure process documented
- Slow CVE response time (30+ days from disclosure to patch)
- Multiple unpatched vulnerabilities
- No security scanning in CI/CD
- History of severe vulnerabilities
- Dismissive attitude toward security reports

### Green Flags
- Published SECURITY.md with clear reporting process
- Quick CVE patches (< 7 days for critical issues)
- Security scanning enabled (Dependabot, Snyk)
- Bug bounty program
- Security-focused documentation
- Proactive security audits

### Common False Positives
- **Old, fixed vulnerabilities**: Past CVEs that were quickly patched show good response, not poor security
- **Reported but not exploitable**: Some CVE reports may be theoretical or non-exploitable in practice

## 3. Community Health

### What This Signal Measures
The breadth and engagement of the project's community, contributor diversity, and the "bus factor" (what happens if the main maintainer leaves).

### What to Check
- Contributor diversity (single maintainer vs. team)
- PR merge rates and issue response times
- Stack Overflow activity
- Community forum engagement
- Maintainer communication style
- Organizational backing

### How to Interpret
- `health_percentage` (from GitHub API) > 70 is good; < 50 suggests missing community files
- Multiple contributors (not just 1-2) indicates healthier bus factor
- Issues with comments show maintainer engagement; many 0-comment issues is a red flag
- PRs merged within days/weeks is healthy; months suggests slow maintenance

### Red Flags
- Single maintainer with no backup or succession plan
- PRs sitting for months unreviewed
- Hostile or dismissive responses to issues
- No community engagement (Discord, Slack, forums)
- Maintainer burnout signals
- All recent activity from a single contributor

### Green Flags
- Multiple active maintainers (3+ regular contributors)
- PRs reviewed within days
- Active Discord/Slack/forum community
- "Good first issue" labels for newcomers
- Welcoming, constructive communication
- Clear governance model or code of conduct
- Corporate or foundation backing

### Common False Positives
- **Single maintainer**: Many excellent packages have one dedicated maintainer. This is higher risk but not automatically disqualifying if the maintainer is responsive and the codebase is simple enough to fork.
- **Low community activity for niche tools**: Specialized packages may have small but high-quality communities

## 4. Documentation Quality

### What This Signal Measures
How well the package is documented, including API references, usage examples, migration guides, and architectural decisions.

### What to Check
- Comprehensive API documentation
- Migration guides between major versions
- Real-world usage examples that work
- Architectural decision records (ADRs)
- TypeScript types / type definitions
- Inline code documentation
- Getting started tutorials

### Red Flags
- Minimal or outdated README
- No API reference documentation
- No migration guides for breaking changes
- Examples that don't work with current version
- Missing type definitions for TypeScript
- No explanation of key concepts
- Documentation and code out of sync

### Green Flags
- Comprehensive documentation site (e.g., Docusaurus, MkDocs)
- Versioned documentation matching releases
- Clear upgrade guides with examples
- Working examples and tutorials
- Interactive playgrounds or demos
- Architecture diagrams
- Searchable API reference
- Contribution guidelines

### Common False Positives
- **Self-documenting APIs**: Very simple, intuitive APIs may not need extensive docs
- **Code-focused projects**: Some low-level libraries may have minimal prose but excellent code comments

## 5. Dependency Footprint

### What This Signal Measures
The size and complexity of the dependency tree, including transitive dependencies and overall bundle size impact.

### What to Check
- Number of direct dependencies
- Number of transitive dependencies
- Total dependency tree depth
- Quality and maintenance of transitive dependencies
- Bundle size impact
- Presence of native/binary dependencies

### Interpreting Dependency Trees (Ecosystem-Relative)

**Compare dependency counts against ecosystem norms:**

**Total Count Assessment:**
- **npm**: 20-50 transitive deps common; 100+ raises concerns; 200+ is extreme
- **Python/PyPI**: 10-30 transitive deps typical; 50+ concerning for utilities
- **Rust/Cargo**: 20-40 transitive deps common (proc-macros inflate counts); 80+ heavy
- **Go**: 5-20 deps typical (stdlib-first culture); 40+ unusual
- **Key**: Compare functionality complexity to dependency count—simple utility with ecosystem-high dep count is red flag

**Duplicate Versions:**
- Multiple versions of same package indicate potential conflicts
- More concerning in npm (version resolution complex) than Cargo (strict resolution)

**Tree Depth:**
- Deep nesting (5+ levels) harder to audit regardless of ecosystem
- Rust proc-macro deps often add depth without adding risk

**Abandoned Transitive Dependencies:**
- Assess transitive deps using same maintenance criteria as direct deps
- One abandoned transitive dep may not be blocker; many suggests poor dep hygiene

**Bundle Size vs. Functionality:**
- npm: Compare to similar packages—is this outlier for what it does?
- Rust: Compile-time deps don't affect binary size, only build time
- Assess: Does bundle size match functionality provided?

### Red Flags (Ecosystem-Relative)
- Dependency count in top quartile for package's functionality and ecosystem
- Transitive dependencies with known vulnerabilities
- Bundle size significantly above ecosystem norm for similar functionality
- Multiple unmaintained transitive dependencies
- Conflicting dependency version requirements
- Native dependencies when ecosystem-standard pure implementation available

### Green Flags (Ecosystem-Relative)
- Dependency count at or below ecosystem median for package type
- All dependencies well-maintained and reputable
- Tree-shakeable / modular imports (npm, modern JS)
- Native deps only when necessary for performance/functionality
- Flat, shallow dependency structure
- Dependencies regularly updated

### Common False Positives
- **Framework packages**: Full frameworks (React, Vue, Angular) legitimately have more dependencies
- **Native performance**: Some packages legitimately need native bindings for performance

## 6. Production Adoption

### What This Signal Measures
Real-world usage of the package in production environments, indicating battle-tested reliability and community trust.

### What to Check
- Download statistics and trends
- GitHub "Used by" count (dependents)
- Notable companies/projects using it
- Tech blog case studies
- Production deployment mentions
- Community recommendations

### How to Investigate
- Check weekly/monthly download counts (npm, PyPI, crates.io)
- Review GitHub dependents graph
- Search "<package> production" in tech blogs
- Look for case studies from reputable companies
- Check framework/platform official recommendations

### Red Flags
- High download counts but no visible production usage (bot inflation)
- Only tutorial/example usage, no production mentions
- Declining download trends over time
- No notable adopters despite being old
- All usage from forks or abandoned projects

### Green Flags
- Used by large, reputable organizations
- Growing or stable download trends
- Featured in production case studies
- Part of major frameworks' recommended ecosystems
- Referenced in official platform documentation
- Active "Who's using this" list

### Common False Positives
- **New packages**: Legitimately new packages may have low downloads but high quality
- **Niche tools**: Specialized packages may have low downloads but be essential for their domain
- **Internal tooling**: Some excellent packages are used primarily internally

## 7. License Compatibility

### What This Signal Measures
Whether the package's license and its dependencies' licenses are compatible with your project's license and intended use.

### What to Check
- Package license type (MIT, Apache-2.0, GPL, etc.)
- License compatibility with your project
- License stability (no recent unexpected changes)
- Transitive dependency licenses
- Patent grants (especially Apache-2.0)

### Red Flags
- Copyleft licenses (GPL, AGPL) for proprietary projects
- No license specified (all rights reserved by default)
- Recent license changes without notice
- Conflicting transitive dependency licenses
- Licenses with advertising clauses
- Ambiguous or custom licenses

### Green Flags
- Permissive licenses (MIT, Apache-2.0, BSD-3-Clause)
- Clear LICENSE file in repository
- Consistent licensing across all dependencies
- SPDX identifiers used
- Patent grants (Apache-2.0)
- Well-understood, OSI-approved licenses

### Common False Positives
- **GPL for standalone tools**: GPL is fine for CLI tools and dev dependencies that don't link into your code
- **Dual licensing**: Some projects offer both commercial and open-source licenses

## 8. API Stability

### What This Signal Measures
How frequently the API changes in breaking ways, adherence to semantic versioning, and the deprecation process.

### What to Check
- Changelog for breaking changes
- Semantic versioning adherence
- Deprecation policy and process
- Frequency of breaking changes in minor versions
- Migration tooling (codemods) for major upgrades
- Version number progression

### How to Investigate
- Review CHANGELOG.md or GitHub releases
- Check version history for breaking change patterns
- Look for semver violations (breaking changes in patches/minors)
- Check for deprecation warnings before removal

### Red Flags
- Frequent breaking changes in minor/patch versions
- No changelog or release notes
- No deprecation warnings before API removal
- Stuck at 0.x version for years
- Breaking changes without major version bumps
- No migration guides for major versions

### Green Flags
- Strict semantic versioning adherence
- Clear, multi-release deprecation cycle
- Stable API (1.x+ with rare breaking changes)
- Migration codemods for major upgrades
- Detailed changelogs with examples
- Beta/RC releases before major versions
- Long-term support (LTS) versions

### Common False Positives
- **Pre-1.0 experimentation**: 0.x versions are expected to have breaking changes
- **Rapid iteration by design**: Some frameworks intentionally move fast and document it clearly

## 9. Bus Factor and Funding

### What This Signal Measures
The sustainability of the project if key contributors leave, and whether there's financial support for ongoing maintenance.

### What to Check
- Organizational backing (CNCF, Apache Foundation, company sponsorship)
- OpenCollective or GitHub Sponsors presence
- Corporate contributor presence
- Full-time vs. volunteer maintainers
- Succession planning
- Funding transparency

### How to Investigate
- Check for sponsor badges in README
- Look for corporate affiliations in contributor profiles
- Search "<package> funding" or "<package> sponsor"
- Check foundation membership (Linux Foundation, Apache, etc.)
- Review OpenCollective or GitHub Sponsors pages

### Red Flags
- Solo volunteer maintainer for critical infrastructure
- No funding mechanism or sponsorship
- Maintainer burnout signals in issues/discussions
- Company backing withdrawn recently
- Underfunded relative to usage scale
- No succession plan

### Green Flags
- Foundation backing (Linux Foundation, Apache, CNCF)
- Active sponsorship program with multiple sponsors
- Corporate maintainers (paid full-time)
- Sustainable funding model
- Multiple organizations contributing
- Clear governance structure
- Successor maintainers identified

### Common False Positives
- **Passion projects**: Some maintainers prefer unfunded projects and sustain them long-term
- **Mature, low-maintenance tools**: Stable packages may not need significant funding

## 10. Ecosystem Momentum

### What This Signal Measures
Whether the technology and ecosystem around the package is growing, stable, or declining.

### What to Check
- Is the ecosystem migrating to alternatives?
- Framework/platform official support and alignment
- Technology trend direction
- Competitor activity
- Conference talks and blog posts
- Job market demand

### How to Investigate
- Search for ecosystem discussions and trends
- Check if framework docs recommend alternatives
- Review technology radar reports (ThoughtWorks, etc.)
- Monitor competitor package growth
- Check conference talk mentions

### Red Flags
- Ecosystem actively migrating to alternatives
- Deprecated by the framework it supports
- Based on sunset technology (Flash, CoffeeScript)
- No mentions at recent conferences
- Declining search trends
- Framework removed official support

### Green Flags
- Growing ecosystem adoption
- Aligned with platform direction and roadmap
- Active plugin/extension ecosystem
- Regular conference mentions
- Increasing search and job trends
- Framework official recommendation
- Standards body involvement

### Common False Positives
- **Stable, mature ecosystems**: Not every package needs to be trendy; stability can be valuable
- **Niche domains**: Specialized tools may have small but stable ecosystems

## General Interpretation Guidelines

### Context Matters
Always adjust signal interpretation based on:
- **Dependency criticality**: Auth libraries need stricter standards than dev tools
- **Project scale**: Enterprise projects have lower risk tolerance
- **Domain complexity**: Cryptography packages need different evaluation than UI libraries
- **Ecosystem norms**: Rust culture emphasizes different values than npm culture

### Weighted Scoring
Not all signals are equally important:
- **Critical dependencies**: Prioritize Security, Maintenance, Funding
- **Standard dependencies**: Balance all signals
- **Dev dependencies**: Prioritize Maintenance, API Stability

### Blocker Override
Any critical red flag (supply chain risk, security exploitation, license violation) should result in AVOID recommendation regardless of other scores.

### Evidence-Based Assessment
Always cite specific data:
- Version numbers and dates
- Actual download counts or GitHub stars
- Specific CVE numbers
- Named organizations using the package
- Measured bundle sizes

### Nuanced Judgment
Avoid purely mechanical scoring:
- A 3/5 in one signal with concerning details may be worse than 2/5 with clear mitigation
- Consider trajectory: improving vs. declining
- Weight recent data more than historical
