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

## Reference Files

This skill uses progressive disclosure - core framework is below, detailed guidance in reference files:

- **[COMMANDS.md](./COMMANDS.md)** - Ecosystem-specific commands for gathering dependency data
- **[SIGNAL_DETAILS.md](./SIGNAL_DETAILS.md)** - Deep guidance for each of the 10 evaluation signals
- **[ECOSYSTEM_GUIDES.md](./ECOSYSTEM_GUIDES.md)** - Ecosystem-specific considerations (npm, PyPI, Cargo, etc.)
- **[EXAMPLES.md](./EXAMPLES.md)** - Real-world evaluation examples

Consult these files as needed during evaluation.

## Evaluation Framework

Evaluate dependencies using these ten key signals:

1. **Activity and Maintenance Patterns** - Commit history, release cadence, issue responsiveness
2. **Security Posture** - CVE history, security policies, vulnerability response time
3. **Community Health** - Contributor diversity, PR merge rates, bus factor
4. **Documentation Quality** - API docs, migration guides, examples
5. **Dependency Footprint** - Transitive dependencies, bundle size
6. **Production Adoption** - Download stats, notable users, trends
7. **License Compatibility** - License type, transitive license obligations
8. **API Stability** - Breaking change frequency, semver adherence
9. **Bus Factor and Funding** - Organizational backing, sustainability
10. **Ecosystem Momentum** - Framework alignment, technology trends

**For detailed investigation guidance**, see [SIGNAL_DETAILS.md](./SIGNAL_DETAILS.md).
**For ecosystem-specific commands**, see [COMMANDS.md](./COMMANDS.md).
**For ecosystem considerations**, see [ECOSYSTEM_GUIDES.md](./ECOSYSTEM_GUIDES.md).

## Evaluation Workflow

Follow this process for thorough, systematic evaluation:

### Phase 1: Quick Assessment
1. Identify package ecosystem (npm, PyPI, Cargo, etc.)
2. Check for immediate dealbreakers (see Critical Red Flags below)
3. If blocker found → Skip to recommendation: AVOID with explanation

### Phase 2: Data Gathering
1. Identify relevant commands for ecosystem (see COMMANDS.md)
2. Run commands in parallel where possible (save time)
3. For each of 10 signals, collect at least 2 data points
4. Save command outputs with timestamps for evidence

### Phase 3: Scoring & Analysis
1. Score each signal 1-5 based on evidence (see SIGNAL_DETAILS.md)
2. Apply weights (H/M/L) based on dependency type (see Scoring Weights below)
3. Note any concerns where Security or Maintenance ≤ 2
4. Calculate weighted score

### Phase 4: Report Generation
1. Use Output Format template (below)
2. Include specific versions, dates, and metrics as evidence
3. Ensure 2+ strengths and 2+ concerns listed
4. Provide clear recommendation with reasoning
5. If AVOID: suggest alternatives
6. If ADOPT: provide "If You Proceed" guidance

**Checkpoint**: Before presenting, verify all claims are evidence-based with specific data cited.

## When to Reconsider Adding a Dependency

Before detailed evaluation, ask: Is the dependency actually needed?

### Write It Yourself If:
- The functionality is < 50 lines of straightforward code
- You only need a small subset of the package's features
- The package adds significant weight for minimal functionality
- Example: Don't add a 500KB package to pad strings or check if a number is odd

### Use the Dependency If:
- The problem domain is complex (crypto, date/time, parsing)
- Correctness is critical and well-tested implementations exist
- The functionality would require significant ongoing maintenance
- You need the full feature set, not just one function

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
[List any dealbreaker issues - these override all scores]
- ⛔ [Blocker description with specific evidence]

### Evaluation Scores

| Signal | Score | Weight | Notes |
|--------|-------|--------|-------|
| Maintenance | X/5 | [H/M/L] | [specific evidence with dates/versions] |
| Security | X/5 | [H/M/L] | [specific evidence] |
| Community | X/5 | [H/M/L] | [specific evidence] |
| Documentation | X/5 | [H/M/L] | [specific evidence] |
| Dependency Footprint | X/5 | [H/M/L] | [specific evidence] |
| Production Adoption | X/5 | [H/M/L] | [specific evidence] |
| License | X/5 | [H/M/L] | [specific evidence] |
| API Stability | X/5 | [H/M/L] | [specific evidence] |
| Funding/Sustainability | X/5 | [H/M/L] | [specific evidence] |
| Ecosystem Momentum | X/5 | [H/M/L] | [specific evidence] |

**Weighted Score**: X/50 (adjusted for dependency criticality)

### Key Findings

#### Strengths
- [Specific strength with evidence]
- [Specific strength with evidence]

#### Concerns
- [Specific concern with evidence]
- [Specific concern with evidence]

### Alternatives Considered
[If applicable, mention alternatives worth evaluating]

### Recommendation Details
[Detailed reasoning for the recommendation with specific evidence]

### If You Proceed (for ADOPT recommendations)
[Specific advice tailored to risks found]
- Version pinning strategy
- Monitoring recommendations
- Specific precautions based on identified concerns
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

**Critical Dependencies**: Auth, security, data handling - require higher bar for all signals

**Standard Dependencies**: Utilities, formatting - balance all signals

**Development Dependencies**: Testing, linting - lower security concerns, focus on maintainability

### Score Interpretation Rules

**Blocker Override**: Any blocker issue → AVOID recommendation regardless of scores

**Critical Thresholds**:
- Security or Maintenance score ≤ 2 → Strongly reconsider regardless of other scores
- Any High-weight signal ≤ 2 → Flag as significant concern in report
- Overall weighted score < 25 → Default to EVALUATE FURTHER or AVOID
- Overall weighted score ≥ 35 → Generally safe to ADOPT (if no blockers)

**Weighting Priority**: Security and Maintenance typically matter more than Documentation or Ecosystem Momentum. A well-documented but unmaintained package is riskier than a poorly-documented but actively maintained one.

## Critical Red Flags (Dealbreakers)

These issues trigger automatic AVOID recommendation:

### Supply Chain Risks
- ⛔ Typosquatting: Package name suspiciously similar to popular package
- ⛔ Compiled binaries without source: Binary blobs without build instructions
- ⛔ Sudden ownership transfer: Recent transfer to unknown maintainer
- ⛔ Install scripts with network calls: Postinstall scripts downloading external code

### Maintainer Behavior
- ⛔ Ransom behavior: Maintainer demanding payment to fix security issues
- ⛔ Protest-ware: Code performing actions based on political/geographic conditions
- ⛔ Intentional sabotage history: Any history of deliberately breaking the package

### Security Issues
- ⛔ Active exploitation: Known vulnerability being actively exploited in wild
- ⛔ Credentials in source: API keys, passwords, or secrets in repository
- ⛔ Disabled security features: Package disables security without clear reason

### Legal Issues
- ⛔ License violation: Package includes code violating its stated license
- ⛔ No license: No license file means all rights reserved (legally risky)
- ⛔ License change without notice: Recent sneaky change to restrictive terms

## Common Pitfalls to Avoid

**Don't:**
- Rely on download counts alone (bot traffic inflates npm stats)
- Dismiss single-maintainer projects automatically (many excellent tools have one maintainer)
- Penalize stable libraries for low commit frequency (may indicate "done" not "abandoned")
- Assume high GitHub stars = good quality
- Make assumptions - always run actual commands

**Do:**
- Verify package identity (check for typosquatting before installing)
- Check transitive dependencies, not just the direct package
- Consider the user's specific use case when weighting signals
- Cite specific versions, dates, and metrics for all claims
- Provide alternatives if recommending AVOID
- Run commands rather than making assumptions

## Performance Guidance

To minimize token usage and maximize efficiency:

1. **Run commands in parallel**: Independent commands can run simultaneously
   ```bash
   # Example
   gh api repos/{owner}/{repo} &
   npm view <package> time &
   wait
   ```

2. **Early exit on blockers**: If Critical Red Flags found, skip detailed scoring

3. **Reference files on-demand**: Only consult COMMANDS.md / SIGNAL_DETAILS.md when needed

4. **Save common data**: If evaluating multiple packages, note common ecosystem information once

## Self-Validation Checklist

Before presenting your report, verify:

- [ ] Cited specific versions and dates for all claims?
- [ ] Ran actual commands rather than making assumptions?
- [ ] All scores supported by evidence in "Notes" column?
- [ ] If Security or Maintenance ≤ 2, flagged prominently?
- [ ] If any blocker exists, recommendation is AVOID?
- [ ] Provided at least 2 alternatives if recommending AVOID?
- [ ] "If You Proceed" section tailored to specific risks found?
- [ ] Recommendation aligns with weighted score and blocker rules?

## Example Invocations

- "Should I use lodash for this project?"
- "Evaluate the axios package for HTTP requests"
- "Is date-fns a good choice for date handling?"
- "Compare express vs fastify vs koa"
- "Should I add this dependency: react-query"
- "Is this package safe to use in production?"

## Guidelines

### Be Evidence-Based
- Always cite specific data points with versions and dates
- Run commands to gather evidence, don't assume
- Reference actual metrics (downloads, contributors, CVE numbers)

### Be Balanced
- Acknowledge both strengths and weaknesses
- Don't dismiss packages for single issues (unless blocker)
- Consider the specific use case context

### Be Actionable
- Provide clear ADOPT / EVALUATE FURTHER / AVOID recommendation
- Include next steps and alternatives
- Tailor "If You Proceed" advice to identified risks

### Consider Context
- A CLI color library needs different scrutiny than an auth library
- Development dependencies have different risk profiles than production deps
- Project scale affects acceptable risk tolerance
- Ecosystem norms vary (see ECOSYSTEM_GUIDES.md)

## Privacy and Security

- Verify license compatibility before recommending
- Consider supply chain risks for sensitive applications
- Note when packages require additional security review
- Flag packages requesting unusual permissions
