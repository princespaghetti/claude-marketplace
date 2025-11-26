# Error Handling and Fallback Strategies

This guide provides fallback strategies when commands fail, data is unavailable, or tools are missing. The goal is to complete evaluations with available information rather than blocking on missing data.

## Table of Contents

- [Missing GitHub Repository](#missing-github-repository)
- [GitHub CLI (`gh`) Not Available](#github-cli-gh-not-available)
- [Package Not Found in Registry](#package-not-found-in-registry)
- [Private/Enterprise Package Registries](#privateenterprise-package-registries)
- [Command Failures](#command-failures)
- [Incomplete or Missing Data](#incomplete-or-missing-data)
- [Network/API Rate Limiting](#networkapi-rate-limiting)

---

## Missing GitHub Repository

**Scenario:** Package metadata doesn't include GitHub repository link, or link is broken.

### Fallback Strategy

1. **Try registry metadata first:**
   ```bash
   # npm
   npm view <package> repository.url
   npm view <package> homepage

   # PyPI
   pip show <package> | grep "Home-page"
   pip show <package> | grep "Project-URL"

   # Cargo
   cargo metadata --format-version 1 | jq '.packages[] | select(.name=="<package>") | .repository'
   ```

2. **Web search as backup:**
   - Search: `"<package-name>" <ecosystem> github`
   - Search: `"<package-name>" source code repository`
   - Check package's documentation site for repository link

3. **If repository truly doesn't exist:**
   - **Mark affected signals as "Unable to Assess":**
     - Community Health → Cannot assess contributor diversity, PR velocity
     - Maintenance (partial) → Can assess releases, cannot assess commit frequency
     - Security (partial) → Can check CVEs, cannot verify security policy
   - **Note limitation prominently in report:**
     ```markdown
     **⚠️ Limited Evaluation**: No source repository found. GitHub-based signals (community health, commit activity) could not be assessed. Evaluation based on registry data and public CVE databases only.
     ```
   - **Reduce confidence in recommendation:**
     - Strong ADOPT becomes EVALUATE FURTHER
     - EVALUATE FURTHER may become AVOID (lack of transparency is concerning)

4. **Red flag considerations:**
   - Closed-source package in open-source ecosystem is unusual
   - No source repository reduces auditability significantly
   - Consider if this is acceptable for your use case

---

## GitHub CLI (`gh`) Not Available

**Scenario:** `gh` command not installed or not authenticated.

### Fallback Strategy

1. **Use package registry commands only:**
   ```bash
   # npm - still provides rich data
   npm view <package> time
   npm view <package> versions
   npm view <package> maintainers
   npm audit

   # PyPI
   pip show <package>
   pip index versions <package>

   # Cargo
   cargo search <package>
   cargo metadata
   ```

2. **Manual checks for GitHub data:**
   - Visit repository URL directly in browser
   - Check: Stars, forks, last commit date, open issues count
   - Review: README, SECURITY.md, CONTRIBUTING.md
   - Manually note findings

3. **Web-based alternatives:**
   - Use https://libraries.io to查看 package stats
   - Check ecosystem-specific sites:
     - npm: npmjs.com package page
     - PyPI: pypi.org package page
     - Cargo: crates.io package page
   - Review security databases: https://osv.dev

4. **Note limitation in report:**
   ```markdown
   **Note**: GitHub API data unavailable (gh CLI not installed). Community health metrics based on manual review and registry data.
   ```

5. **Recommendation:**
   - Include installation instructions: `brew install gh` / `apt install gh`
   - For complete analysis, installing `gh` is recommended

---

## Package Not Found in Registry

**Scenario:** `npm view <package>` or equivalent returns "package not found."

### Diagnosis Steps

1. **Verify package name:**
   - Check for typos
   - Verify correct ecosystem (npm vs PyPI vs Cargo)
   - Check if package uses scope: `@org/package-name`

2. **Check if package was removed/yanked:**
   ```bash
   # npm - check if ever existed
   npm view <package> --json 2>&1 | grep "404"

   # PyPI - yanked versions show in history
   pip index versions <package>

   # Cargo - yanked crates still visible
   cargo search <package>
   ```

3. **Possible causes:**
   - **Typo in package name** → Correct and retry
   - **Wrong ecosystem** → Verify it's npm not PyPI, etc.
   - **Package removed/unpublished** → **MAJOR RED FLAG**
   - **Private package** → See Private/Enterprise section below
   - **Pre-release/beta only** → Check version tags

### If Package Was Removed

**This is a critical finding:**

```markdown
## Dependency Evaluation: <package-name>

**Recommendation**: AVOID
**Risk Level**: Critical
**Blockers Found**: Yes

### Blockers
⛔ **Package has been unpublished from registry**

This is an extremely serious red flag. Possible causes:
- Security incident (compromised package)
- Maintainer protest or dispute
- Legal/licensing issue
- Malware discovery

**Do NOT use this package.** Investigate why it was removed before considering any alternatives.
```

---

## Private/Enterprise Package Registries

**Scenario:** Package is in private registry, company npm registry, etc.

### Approach

1. **Acknowledge evaluation limits:**
   ```markdown
   **Note**: This is a private/enterprise package. Public ecosystem data (download counts, public dependents) not available. Evaluation based on:
   - Internal repository access
   - Company security policies
   - Internal usage metrics (if available)
   ```

2. **Focus on accessible signals:**
   - ✅ **Maintenance**: If you have repo access, assess commit history
   - ✅ **Security**: Check internal security scan results
   - ✅ **Community**: Assess internal team size, responsiveness
   - ✅ **Documentation**: Review internal docs
   - ❌ **Production Adoption**: Public data unavailable; use internal metrics
   - ❌ **Ecosystem Momentum**: Not applicable for private packages

3. **Adjust weighting:**
   - Increase weight on: Internal security scans, maintainer responsiveness, documentation
   - Decrease weight on: Public production adoption, ecosystem momentum

4. **Company-specific considerations:**
   - Internal packages may have lower documentation standards (acceptable if team is accessible)
   - Security may be handled by company-wide scanning (acceptable if robust)
   - Bus factor more critical (if sole maintainer leaves company, what happens?)

---

## Command Failures

### npm Commands Fail

**Scenario:** `npm view <package>` returns errors.

**Possible causes:**
- Network issues → Retry with `--registry` flag
- npm not installed → Install npm
- Package truly doesn't exist → See "Package Not Found" section

**Fallback:**
```bash
# Try alternative registry
npm view <package> --registry=https://registry.npmjs.org

# Use npms.io API
curl https://api.npms.io/v2/package/<package>
```

### GitHub API Rate Limiting

**Scenario:** `gh api` returns 403 rate limit error.

**Fallback:**
```bash
# Check rate limit status
gh api rate_limit

# Wait for reset (shown in rate_limit response)
# OR authenticate to get higher limits
gh auth login
```

**If blocked:**
- Note in report: "GitHub API rate limited; data gathered from alternative sources"
- Use web UI for manual checks
- Use https://libraries.io as alternative data source

### Python pip Commands Fail

**Scenario:** `pip show <package>` fails or hangs.

**Fallbacks:**
```bash
# Try with different Python version
python3 -m pip show <package>

# Use PyPI JSON API directly
curl https://pypi.org/pypi/<package>/json

# Check installed packages
pip list | grep <package>
```

---

## Incomplete or Missing Data

### Handling Partial Data

When some data is unavailable, proceed with available signals:

**Assessment approach:**
1. **Clearly mark unavailable signals** in your evaluation
2. **Weight available signals more heavily**
3. **Note data limitations** in final recommendation
4. **Adjust confidence level:**
   - Missing 1-2 signals → Proceed with note
   - Missing 3-5 signals → Lower confidence, more cautious recommendation
   - Missing 6+ signals → Insufficient data for recommendation

**Example report structure:**
```markdown
### Evaluation Scores

| Signal (Weight) | Score | Evidence |
|-----------------|-------|----------|
| Maintenance (H) | 4/5   | Last release 2 weeks ago... |
| Security (H) | Unable to Assess | No source repository found |
| Community (M) | Unable to Assess | No source repository found |
| Documentation (M) | 3/5   | README present but minimal... |
...

**Note**: Unable to assess Community Health and Security Posture due to missing source repository. Recommendation confidence: Medium.
```

### When Data Is Too Limited

**If 6+ signals cannot be assessed:**

```markdown
## Dependency Evaluation: <package-name>

**Recommendation**: INSUFFICIENT DATA
**Risk Level**: Unknown
**Blockers Found**: Data unavailable

Unable to complete evaluation due to insufficient data:
- No source repository found
- Package registry data minimal
- No public security scan results
- No community metrics available

**Recommendation**: Request more information from package maintainers or choose alternative with better transparency.
```

---

## Network/API Rate Limiting

### GitHub API Rate Limits

**Unauthenticated:** 60 requests/hour
**Authenticated:** 5,000 requests/hour

**When rate limited:**
1. Authenticate: `gh auth login`
2. Check reset time: `gh api rate_limit`
3. Prioritize most important API calls
4. Use conditional requests (ETags) to save quota

### npm Registry Rate Limits

npm registry typically doesn't rate limit, but:
- If experiencing issues, use `--registry` flag
- Consider using npm's v2 API for programmatic access
- Check network/VPN isn't blocking registry

### Working Within Limits

**Efficient API usage:**
```bash
# Batch requests where possible
# Good: Single call with jq to extract multiple fields
gh api repos/{owner}/{repo} --jq '{stars: .stargazers_count, forks: .forks_count, updated: .updated_at}'

# Avoid: Multiple calls for same data
gh api repos/{owner}/{repo} --jq '.stargazers_count'
gh api repos/{owner}/{repo} --jq '.forks_count'  # Wasteful
```

**Prioritize calls:**
1. Critical: Security advisories, CVE history
2. High: Maintenance activity, release dates
3. Medium: Contributor counts, PR metrics
4. Low: Star counts, fork counts

---

## General Error Handling Principles

### 1. Degrade Gracefully
- Partial data is better than no evaluation
- Clearly document what's missing
- Adjust confidence levels appropriately

### 2. Be Transparent
- Always note data limitations in report
- Explain which signals couldn't be assessed and why
- Don't guess or fill in missing data

### 3. Provide Alternatives
- If tool missing, provide installation instructions
- If data unavailable, suggest manual verification steps
- If evaluation incomplete, recommend next steps

### 4. Fail Safely
- When in doubt about data quality, recommend EVALUATE FURTHER not ADOPT
- Missing security data should increase caution, not be ignored
- Lack of transparency is itself a red flag

### 5. Document for User
Always include a "Data Collection Summary" in reports when errors occurred:

```markdown
## Data Collection Summary

**Commands executed successfully:**
- ✅ npm view <package> (version, license, maintainers)
- ✅ npm audit (security scan)

**Commands failed/unavailable:**
- ❌ gh api (GitHub CLI not installed) → Manual GitHub review performed
- ⚠️  npm ls (package not installed) → Analyzed published dependency tree

**Data limitations:**
- Community metrics based on manual review, not API data
- Contributor diversity not quantitatively assessed

**Recommendation confidence:** Medium (due to missing API data)
```

---

## Quick Reference: Command Failure Matrix

| Failure | Cause | Fallback | Impact |
|---------|-------|----------|--------|
| `npm view` fails | Package not found | Verify name, check if removed | CRITICAL if removed |
| `gh api` fails | CLI not installed | Manual GitHub review, libraries.io | Reduces accuracy |
| `gh api` 403 | Rate limited | Wait for reset, authenticate | Temporary delay |
| `pip show` fails | Package not installed | `pip index versions`, PyPI web | Minor - use API |
| No repository found | Closed source | Registry data only | Lower confidence |
| CVE search empty | No vulnerabilities OR no scans | Assume no known CVEs, note uncertainty | Acceptable |
| Download stats unavailable | Private package | Internal metrics | Expected for private |

---

## Summary

**Key principle:** Never let missing data completely block an evaluation. Provide best assessment with available information, clearly document limitations, and adjust recommendation confidence accordingly.

Missing data handling priority:
1. **Security data missing** → Increase caution significantly
2. **Maintenance data missing** → Hard to recommend ADOPT
3. **Community data missing** → Note but less critical
4. **Documentation data missing** → Can assess manually
5. **Ecosystem momentum missing** → Least critical

**When absolutely stuck:** Recommend EVALUATE FURTHER with specific next steps for user to investigate manually.
