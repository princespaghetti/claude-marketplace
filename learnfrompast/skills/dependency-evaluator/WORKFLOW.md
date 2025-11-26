# Dependency Evaluation Workflow

This file provides detailed workflow guidance for conducting systematic dependency evaluations. The main SKILL.md file provides the framework overview; this file provides step-by-step operational guidance.

## Table of Contents

- [Overview](#overview)
- [Pre-Evaluation: Should You Add Any Dependency?](#pre-evaluation-should-you-add-any-dependency)
- [Phase 1: Quick Assessment](#phase-1-quick-assessment)
- [Phase 2: Data Gathering](#phase-2-data-gathering)
- [Phase 3: Scoring & Analysis](#phase-3-scoring--analysis)
- [Phase 4: Report Generation](#phase-4-report-generation)
- [Performance Tips](#performance-tips)
- [Common Pitfalls to Avoid](#common-pitfalls-to-avoid)

---

## Overview

Follow this systematic process for thorough, efficient dependency evaluation. Not every evaluation requires all steps—use judgment based on complexity.

**For simple single-package evaluations:** Proceed directly through phases.
**For complex scenarios** (comparing 3+ packages, contradictory signals, critical dependencies): Take extra care in each phase.

---

## Pre-Evaluation: Should You Add Any Dependency?

Before evaluating a specific package, ask: **Is a dependency actually needed?**

### Write It Yourself If:
- The functionality is < 50 lines of straightforward code
- You only need a small subset of the package's features
- The package adds significant weight for minimal functionality
- Example: Don't add a 500KB package to pad strings or check if a number is odd

### Use a Dependency If:
- The problem domain is complex (crypto, date/time, parsing)
- Correctness is critical and well-tested implementations exist
- The functionality would require significant ongoing maintenance
- You need the full feature set, not just one function

**If you're unsure:** Prototype the functionality yourself (30-60 minutes). If it's trivial, you have your answer. If it's complex, you've confirmed a dependency is justified.

---

## Phase 1: Quick Assessment

**Goal:** Identify immediate dealbreakers before investing time in full evaluation.

### Steps

1. **Identify package ecosystem**
   - npm, PyPI, Cargo, Go, Maven, RubyGems, etc.
   - See [ECOSYSTEM_GUIDES.md](./ECOSYSTEM_GUIDES.md) for ecosystem-specific considerations

2. **Verify package identity**
   ```bash
   # Check package name carefully
   # Watch for typosquatting: react vs reakt, requests vs reqeusts
   ```
   - **Red flag:** Name suspiciously similar to popular package
   - **Red flag:** Package created very recently with popular-sounding name

3. **Check for immediate dealbreakers** (see SKILL.md § Critical Red Flags)
   - Supply chain risks (typosquatting, sudden ownership transfer)
   - Maintainer behavior issues (ransom-ware, protest-ware)
   - Active exploitation of known vulnerabilities
   - Legal issues (no license, license violations)

4. **Locate source repository**
   ```bash
   # npm
   npm view <package> repository.url

   # PyPI
   pip show <package> | grep "Home-page"

   # Cargo
   cargo metadata | jq '.packages[] | select(.name=="<package>") | .repository'
   ```
   - If no repository found → See [ERROR_HANDLING.md](./ERROR_HANDLING.md) § Missing GitHub Repository

5. **Quick license check**
   ```bash
   # npm
   npm view <package> license

   # GitHub
   gh api repos/{owner}/{repo}/license --jq '.license.spdx_id'
   ```
   - **Blocker if:** GPL for proprietary project, no license, incompatible license

### Decision Point

**If blocker found:**
→ Skip to Phase 4, generate AVOID recommendation with alternatives

**If no blockers:**
→ **Default:** Proceed to Phase 1.5 (Automated Data Gathering Script)
→ **Fallback:** Skip to Phase 2 (Manual Data Gathering) only if script unavailable

---

## Phase 1.5: Automated Data Gathering (Recommended)

**Goal:** Use the dependency evaluator script to quickly gather baseline data.

**Default approach:** Try the script first for supported ecosystems (npm, pypi, cargo, go). It saves 10-15 minutes of manual command execution and provides structured, complete data automatically.

**Skip the script only if:**
- Python 3.7+ is not available in your environment
- Unsupported ecosystem (Maven, RubyGems, NuGet, etc.)
- Script fails or produces errors (then fall back to manual workflow)
- Specific network/firewall restrictions prevent API access

### Using the Script

```bash
cd learnfrompast/skills/dependency-evaluator
python3 scripts/dependency_evaluator.py <package-name> <ecosystem> > data.json
```

**Examples:**
```bash
# npm package
python3 scripts/dependency_evaluator.py lodash npm > lodash-data.json

# PyPI package
python3 scripts/dependency_evaluator.py requests pypi > requests-data.json

# Cargo crate
python3 scripts/dependency_evaluator.py serde cargo > serde-data.json
```

### What the Script Provides

The script automatically gathers:
- ✓ Registry metadata (version, license, description)
- ✓ Version history and release count
- ✓ GitHub repository data (stars, issues, contributors)
- ✓ Community health metrics
- ✓ Structured error/warning messages

The script has limitations:
- ✗ npm audit (requires package.json context)
- ✗ Dependency tree analysis (requires installation)
- ✗ Manual investigation (documentation quality, ecosystem trends)

See [SCRIPT_USAGE.md](./SCRIPT_USAGE.md) for detailed documentation.

### Interpreting Script Output

Review the JSON output:

```json
{
  "registry_data": { ... },    // Use for Signals 1, 6, 7
  "github_data": { ... },      // Use for Signals 1, 2, 3, 9
  "security_data": { ... },    // Use for Signal 2 (often limited)
  "dependency_footprint": { ... }, // Use for Signal 5 (often limited)
  "warnings": [ ... ],         // Note data limitations
  "errors": [ ... ]            // Critical issues found
}
```

**If errors are present:** Verify package name, check network, review error messages

**If warnings are present:** Note limitations in your final report

### Decision Point

**If script succeeded:**
→ Proceed to Phase 2 to fill gaps (documentation, manual investigation)

**If script failed:**
→ Proceed to Phase 2 (Manual Data Gathering) using commands from COMMANDS.md

---

## Phase 2: Data Gathering

**Goal:** Collect evidence for all 10 evaluation signals efficiently.

> **Note:** If you skipped Phase 1.5 or the script provided incomplete data, use this phase to manually gather remaining information. If you used the script successfully, use this phase to fill gaps the script couldn't cover (documentation quality, manual investigation, ecosystem trends).

### General Strategy

1. **Run commands in parallel where possible** (see Performance Tips below)
2. **Gather at least 2 data points per signal** for evidence-based scoring
3. **Save command outputs** with timestamps for citation in report

### Data Gathering by Signal

Refer to [COMMANDS.md](./COMMANDS.md) for specific commands. General approach:

**1. Maintenance & Activity**
```bash
# Package registry: version history, release dates
npm view <package> time versions

# GitHub: recent activity
gh api repos/{owner}/{repo} --jq '{pushed_at, open_issues_count}'
gh api repos/{owner}/{repo}/commits --jq '.[0].commit.author.date'
```

**2. Security Posture**
```bash
# Ecosystem security tools
npm audit --json  # (npm)
# cargo audit     # (Rust, requires separate install)
# pip-audit       # (Python, requires separate install)

# GitHub security
gh api repos/{owner}/{repo}/security-advisories
```

**3. Community Health**
```bash
# GitHub community metrics
gh api repos/{owner}/{repo}/community/profile --jq '{health_percentage, files}'
gh api repos/{owner}/{repo}/contributors --jq 'length'

# Issue/PR activity
gh api repos/{owner}/{repo}/issues --jq '[.[] | select(.pull_request == null)] | .[0:5]'
```

**4. Documentation Quality**
- Manual review: README, docs site, API reference
- Check for: Migration guides, examples, TypeScript types (for JS)

**5. Dependency Footprint**
```bash
# View full dependency tree
npm ls --all <package>       # npm
cargo tree -p <package>      # Rust
go mod graph | grep <pkg>    # Go
```

**6. Production Adoption**
- Check weekly downloads on package registry site
- GitHub "Used by" count: https://github/{owner}/{repo}/network/dependents
- Web search: "<package> production" for case studies

**7. License Compatibility**
```bash
# Package license
npm view <package> license

# Dependency licenses (if SBOM available)
gh api repos/{owner}/{repo}/dependency-graph/sbom --jq '.sbom.packages[].licenseConcluded'
```

**8. API Stability**
- Manual review: CHANGELOG.md, GitHub Releases
- Check for: Semver adherence, breaking change frequency, deprecation policy

**9. Bus Factor & Funding**
- Check for: GitHub Sponsors, OpenCollective, corporate backing
- Review: Contributor affiliations, organizational support
- Search: "<package> funding" or "<package> sponsor"

**10. Ecosystem Momentum**
- Research: Ecosystem migration patterns, framework recommendations
- Check: Recent conference mentions, blog posts, technology radar reports

### Handling Missing Data

If commands fail or data is unavailable, see [ERROR_HANDLING.md](./ERROR_HANDLING.md) for fallback strategies.

---

## Phase 3: Scoring & Analysis

**Goal:** Translate gathered data into numerical scores and identify key findings.

### Scoring Process

1. **Score each signal 1-5 based on evidence**
   - See [SIGNAL_DETAILS.md](./SIGNAL_DETAILS.md) for detailed scoring guidance
   - Use ecosystem-relative assessment (compare to ecosystem norms)
   - **1/5:** Major red flags, well below ecosystem standards
   - **2/5:** Below expectations, concerning patterns
   - **3/5:** Acceptable, meets minimum standards
   - **4/5:** Good, above average for ecosystem
   - **5/5:** Excellent, significantly exceeds norms

2. **Apply weights based on dependency type**
   - See SKILL.md § Scoring Weights table
   - **Critical dependencies** (auth, security, data): High weight on Security, Maintenance, Funding
   - **Standard dependencies** (utilities, formatting): Balanced weights
   - **Dev dependencies** (testing, linting): Lower security weight, higher API stability

3. **Note critical concerns**
   - **If Security or Maintenance ≤ 2:** Flag as significant concern regardless of other scores
   - **If any High-weight signal ≤ 2:** Highlight prominently in report
   - **Overall weighted score < 25:** Default to EVALUATE FURTHER or AVOID
   - **Overall weighted score ≥ 35:** Generally safe to ADOPT (if no blockers)

4. **Calculate weighted score**
   - Multiply each signal score by its weight (H=3, M=2, L=1)
   - Sum weighted scores
   - Maximum possible: 50 (if all signals 5/5 with high weight)
   - Typical good package: 35-45

### Analysis Process

1. **Identify patterns:**
   - Are weaknesses clustered (e.g., all community signals low)?
   - Do strengths compensate for weaknesses?
   - Is there a trajectory (improving vs declining)?

2. **Consider context:**
   - Package purpose (critical vs utility)
   - Project scale (enterprise vs startup)
   - Team capabilities (can you fork if needed?)
   - Risk tolerance

3. **Weigh trade-offs:**
   - Heavy dependencies but excellent maintenance
   - Single maintainer but outstanding code quality
   - Lower popularity but superior architecture

4. **Check score interpretation rules:**
   - **Blocker override:** Any Critical Red Flag → AVOID regardless of scores
   - **Critical thresholds:** Security or Maintenance ≤ 2 → Strongly reconsider
   - **Weighting priority:** Security and Maintenance > Documentation or Ecosystem Momentum

---

## Phase 4: Report Generation

**Goal:** Create clear, actionable evaluation report using standard format.

### Report Structure

Use the Output Format template from SKILL.md:

```markdown
## Dependency Evaluation: <package-name>

### Summary
[2-3 sentence assessment with recommendation]

**Recommendation**: [ADOPT / EVALUATE FURTHER / AVOID]
**Risk Level**: [Low / Medium / High]
**Blockers Found**: [Yes/No]

### Blockers (if any)
- ⛔ [Specific blocker with evidence]

### Evaluation Scores
[Score table with evidence]

### Key Findings
#### Strengths
- [Specific strength with evidence]

#### Concerns
- [Specific concern with evidence]

### Alternatives Considered
[If applicable]

### Recommendation Details
[Detailed reasoning]

### If You Proceed (for ADOPT/EVALUATE FURTHER)
- [Specific risk mitigation advice]
```

### Report Quality Checklist

Before presenting report, verify:

- [ ] Cited specific versions and dates for all claims?
- [ ] Ran actual commands rather than making assumptions?
- [ ] All scores supported by evidence in "Evidence" column?
- [ ] If Security or Maintenance ≤ 2, flagged prominently?
- [ ] If any blocker exists, recommendation is AVOID?
- [ ] Provided at least 2 alternatives if recommending AVOID?
- [ ] "If You Proceed" section tailored to specific risks found?
- [ ] Recommendation aligns with weighted score and blocker rules?

### Writing Recommendations

**ADOPT:** Clear benefits, low/acceptable risk, minor concerns don't outweigh strengths
- Must have: No blockers, Security & Maintenance ≥ 3, weighted score typically ≥ 35
- Include: Specific version pinning strategy, monitoring recommendations

**EVALUATE FURTHER:** Mixed signals, decision depends on user's specific context
- Use when: Trade-offs exist, user priorities matter, some concerning but not blocking issues
- Include: Decision framework, specific questions for user to consider

**AVOID:** Dealbreaker issues present, risks outweigh benefits
- Must include: Specific reasons why (blockers, critical scores ≤ 2, security concerns)
- Must include: 2+ alternative recommendations with brief comparison

---

## Performance Tips

### Run Commands in Parallel

Independent commands can run simultaneously to save time:

```bash
# Example: Parallel execution
npm view <package> time &
npm view <package> versions &
gh api repos/{owner}/{repo} &
gh api repos/{owner}/{repo}/community/profile &
wait  # Wait for all background jobs to complete
```

**What to parallelize:**
- Different API endpoints (npm + GitHub)
- Multiple GitHub API calls to different endpoints
- Security scans + dependency tree analysis

**What NOT to parallelize:**
- Commands that depend on each other
- Avoid excessive parallel GitHub API calls (rate limits)

### Early Exit on Blockers

If Critical Red Flags found in Phase 1:
- Skip detailed scoring
- Generate AVOID recommendation immediately
- Focus time on finding good alternatives

### Save Common Data

If evaluating multiple packages in same ecosystem:
- Note ecosystem norms once, reference in all evaluations
- Save common baseline data (e.g., typical npm dependency counts)
- Reuse ecosystem-specific guidance

### Batch Similar Evaluations

When comparing 3+ alternatives:
1. Gather data for all packages first
2. Score all packages using consistent criteria
3. Generate comparison table
4. Write individual reports referencing comparison

---

## Common Pitfalls to Avoid

### Don't:

1. **Rely on download counts alone**
   - Bot traffic inflates npm stats
   - New packages may be high quality with low downloads
   - Old packages may have high downloads but be deprecated

2. **Dismiss single-maintainer projects automatically**
   - Many excellent tools have one dedicated maintainer
   - Assess maintainer quality, responsiveness, track record
   - Single maintainer with 5-year track record may be lower risk than 10 inactive contributors

3. **Penalize stable libraries for low commit frequency**
   - Low activity may indicate "done" not "abandoned"
   - Check if security issues are still addressed
   - Cryptography, date libraries, protocols may legitimately need few updates

4. **Assume high GitHub stars = good quality**
   - Stars can be gamed or reflect hype, not quality
   - Use stars as one signal among many
   - Production adoption more valuable than stars

5. **Make assumptions without running commands**
   - Always gather actual data
   - Don't guess about security, dependencies, or maintenance
   - If data unavailable, note it explicitly

6. **Ignore transitive dependencies**
   - Security vulnerabilities often in transitive deps
   - Unmaintained transitive deps are technical debt
   - Always check full dependency tree, not just direct deps

7. **Apply npm norms to other ecosystems**
   - Rust, Go, Python have different cultural expectations
   - What's normal for npm may be unusual for Cargo
   - Always use ecosystem-relative assessment

### Do:

1. **Verify package identity before installing**
   - Check for typosquatting (react vs reakt)
   - Verify package is the intended one
   - Be suspicious of new packages with popular-sounding names

2. **Check transitive dependencies**
   - Run full dependency tree analysis
   - Assess maintenance of transitive deps
   - Security issues often hide deep in tree

3. **Consider the user's specific use case**
   - CLI tool has different requirements than web library
   - Internal tool vs public-facing app affects risk tolerance
   - Enterprise vs startup affects acceptable bus factor

4. **Cite specific versions, dates, and metrics**
   - "Last release v2.4.1 on 2025-01-10" not "recently updated"
   - "50k weekly downloads" not "popular"
   - "CVE-2023-12345 patched in 48 hours" not "good security"

5. **Provide alternatives when recommending AVOID**
   - Always suggest 2+ alternatives
   - Briefly compare alternatives
   - Help user find a better option

6. **Run commands rather than assuming**
   - Don't guess dependency counts
   - Don't assume security based on popularity
   - Verify everything with actual data

---

## Workflow Variants

### Quick Evaluation (< 15 minutes)

For low-risk dev dependencies or quick checks:
1. Run blocker check only
2. Check maintenance (last release, commit activity)
3. Quick security scan (npm audit)
4. Brief recommendation

**Use when:** Dev dependency, low criticality, time-constrained

### Standard Evaluation (30-45 minutes)

Full 10-signal evaluation as described above.

**Use when:** Standard dependencies, moderate criticality

### Thorough Evaluation (1-2 hours)

Standard evaluation plus:
- Compare 3+ alternatives side-by-side
- Deep-dive into transitive dependencies
- Review issue history and maintainer responses
- Check multiple security databases
- Research production case studies

**Use when:** Critical dependencies (auth, security, data handling), large investment

### Comparison Evaluation (Multiple Packages)

When comparing alternatives:
1. Run Phase 1-2 for all packages in parallel
2. Create comparison matrix with all scores
3. Identify trade-offs between packages
4. Recommend based on user priorities

---

## Summary

**Key workflow principles:**
1. **Systematic:** Follow phases to ensure thoroughness
2. **Evidence-based:** Always cite specific data
3. **Efficient:** Parallelize where possible, early-exit on blockers
4. **Transparent:** Note limitations, missing data, assumptions
5. **Actionable:** Provide clear recommendations with next steps

**Remember:** The goal is informed decision-making, not perfect information. Provide best assessment with available data, clearly document limitations, and adjust recommendation confidence accordingly.
