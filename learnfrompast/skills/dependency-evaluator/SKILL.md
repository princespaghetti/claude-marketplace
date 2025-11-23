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
# For npm packages
npm view <package> time

# Check GitHub activity via web search
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

**How to investigate:**
- Search for CVE history: `"<package-name>" CVE`
- Check npm audit / pip-audit / cargo audit reports
- Look for security badges in README
- Review GitHub Security tab

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

**How to investigate:**
```bash
# Check contributor count via GitHub API or web
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
pip show <package>
pipdeptree -p <package>

# Rust
cargo tree -p <package>

# Go
go mod graph | grep <package>
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
# Node.js
npx license-checker --production --summary

# Python
pip-licenses

# Check package.json or pyproject.toml for license field
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

### Evaluation Scores

| Signal | Score | Notes |
|--------|-------|-------|
| Maintenance | X/5 | [brief note] |
| Security | X/5 | [brief note] |
| Community | X/5 | [brief note] |
| Documentation | X/5 | [brief note] |
| Dependency Footprint | X/5 | [brief note] |
| Production Adoption | X/5 | [brief note] |
| License | X/5 | [brief note] |
| API Stability | X/5 | [brief note] |
| Funding/Sustainability | X/5 | [brief note] |
| Ecosystem Momentum | X/5 | [brief note] |

**Overall Score**: X/50

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

- Don't recommend packages with known unpatched vulnerabilities
- Verify license compatibility before recommending
- Consider supply chain risks for sensitive applications
- Note when packages require additional security review
