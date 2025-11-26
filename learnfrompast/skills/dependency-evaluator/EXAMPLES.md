# Dependency Evaluation Examples

This file contains concrete worked examples demonstrating the evaluation framework in action. Each example shows the complete evaluation process, scoring rationale, and final recommendation.

**Important:** These are hypothetical packages created for teaching purposes. They illustrate evaluation methodology, not real package recommendations.

## Table of Contents

- [Example 1: ExampleCo HTTP Client (npm) - ADOPT](#example-1-exampleco-http-client-npm---adopt)
- [Example 2: legacy-parser (PyPI) - AVOID](#example-2-legacy-parser-pypi---avoid)
- [Example 3: fast-compute (Rust) - ADOPT with Nuance](#example-3-fast-compute-rust---adopt-with-nuance)
- [Example 4: mega-framework (npm) - EVALUATE FURTHER](#example-4-mega-framework-npm---evaluate-further)
- [Key Takeaways](#key-takeaways-from-examples)

---

## Example 1: ExampleCo HTTP Client (npm) - ADOPT

**User Request:** "Should I use exampleco-http for making API requests in my Node.js application?"

**Package Context:**
- Name: exampleco-http (npm)
- Dependency Type: Standard (HTTP client)
- Use Case: REST API calls in backend service

### Summary
ExampleCo HTTP Client is a well-maintained, production-ready HTTP library with corporate backing, excellent security practices, and clean dependencies. Strong positive signals across all evaluation criteria make this a low-risk adoption.

**Recommendation**: ADOPT
**Risk Level**: Low
**Blockers Found**: No

### Evaluation Scores

| Signal (Weight) | Score | Evidence |
|-----------------|-------|----------|
| Maintenance (H) | 5/5   | Last release v2.4.1 on 2025-01-10. Weekly commits. 47 releases over 2 years. |
| Security (H) | 5/5   | SECURITY.md present. 2 historical CVEs patched <48hrs. Dependabot enabled. |
| Community (M) | 5/5   | 5 active maintainers from ExampleCo Inc. 89 contributors. PRs merged 2-4 days. |
| Documentation (M) | 4/5   | Comprehensive docs site. API reference complete. TypeScript types. Minor: advanced examples limited. |
| Dependency Footprint (M) | 5/5   | 8 total deps (2 direct, 6 transitive). Bundle: 45KB. No security issues. |
| Production Adoption (M) | 5/5   | 50k weekly downloads. 1,200+ dependents. Featured in Node.js blog. |
| License (H) | 5/5   | MIT. All deps MIT or Apache-2.0. No conflicts. |
| API Stability (M) | 5/5   | Strict semver. v2.x stable 18 months. Deprecation warnings 6mo before removal. |
| Funding (H) | 5/5   | Backed by ExampleCo Inc (series B). 3 full-time maintainers. |
| Ecosystem Momentum (L) | 4/5   | Growing adoption. Ecosystem shifting to native fetch, but package adds value. |

**Weighted Score**: 48/50

### Key Findings

**Strengths:**
- Corporate backing with 3 dedicated full-time engineers
- Fast security response (48hr CVE patches historically)
- Clean dependency tree (only 8 total packages)
- Production-proven (50k weekly downloads, major adopters)

**Concerns:**
- Ecosystem gradual shift to native `fetch` API (2-3 year horizon)
- Advanced use case documentation could be more comprehensive

### Alternatives Considered
- **Native fetch**: Zero dependencies but lacks retry/timeout/interceptor features
- **axios**: Higher downloads but heavier deps (15+) and slower maintenance
- **node-fetch**: Lightweight but minimal features

### Recommendation Details
Exemplary well-maintained package. Corporate backing, responsive security, clean dependencies, and strong community make this low-risk for production use. While the ecosystem is moving toward native `fetch`, this package provides significant value-adds that native fetch lacks (retries, interceptors, transforms). ExampleCo has committed to maintenance through 2027+.

### If You Proceed
- Pin to `^2.4.0` for patches/minors
- Monitor for ExampleCo native fetch migration plans
- Enable Dependabot/GitHub security alerts
- Review dependencies annually

---

## Example 2: legacy-parser (PyPI) - AVOID

**User Request:** "I need to parse legacy data format files. Should I use legacy-parser?"

**Package Context:**
- Name: legacy-parser (PyPI)
- Dependency Type: Standard (data parsing)
- Use Case: Parsing proprietary legacy format

### Summary
legacy-parser is an abandoned package with critical unpatched security vulnerabilities and zero maintainer activity for 3 years. Active CVEs including RCE make this completely unsuitable for any use.

**Recommendation**: AVOID
**Risk Level**: High
**Blockers Found**: Yes

### Blockers
⛔ **Active unpatched CVEs**: CVE-2023-12345 (RCE) and CVE-2024-67890 (DoS) public for 1+ year with no patches
⛔ **Complete abandonment**: Zero activity for 3 years, no security response
⛔ **Python 3.12 compatibility unknown**: No testing on modern Python

### Evaluation Scores

| Signal (Weight) | Score | Evidence |
|-----------------|-------|----------|
| Maintenance (H) | 1/5   | Last commit 2022-03-15 (3 years ago). Last release v0.4.2 on 2022-03-10. |
| Security (H) | 1/5   | 2 open CVEs (High RCE, Medium DoS). No security policy. No patches. |
| Community (M) | 1/5   | Single maintainer (jsmith). 47 open issues, no responses 2+ years. |
| Documentation (M) | 3/5   | Clear README with examples. Uses outdated Python 3.8 syntax. |
| Dependency Footprint (M) | 4/5   | 3 direct, 8 total deps. Lightweight. One transitive dep unmaintained. |
| Production Adoption (M) | 2/5   | 850 downloads/month (low). 12 dependents. Downloads declining -40% YoY. |
| License (H) | 5/5   | MIT. Clean licensing. |
| API Stability (M) | 2/5   | v0.4.x after 5+ years. Breaking changes in minors. No semver. |
| Funding (L) | 1/5   | No funding. Abandoned volunteer project. |
| Ecosystem Momentum (L) | 1/5   | Community migrated to alternatives. No Python 3.12 support verified. |

**Weighted Score**: 18/50

### Key Findings

**Strengths:**
- Clear basic documentation
- Lightweight dependencies
- Permissive MIT license

**Concerns:**
- Critical: CVE-2023-12345 RCE vulnerability unpatched
- Complete abandonment (3 years zero activity)
- No modern Python support verified
- Declining usage (-40% YoY)
- Unmaintained transitive dependency (old-xml-lib)

### Recommended Alternatives
- **modern-parser** (PyPI): Active fork with CVE patches. Same API. 5k downloads/month. 3-person team.
- **fast-parse** (PyPI): Different API, supports same format. Well-maintained. 12k downloads/month.
- **format-tools** (PyPI): Comprehensive legacy format tools. Larger but production-ready. 50k downloads/month.

### Recommendation Details
**Do not use legacy-parser.** Critical RCE vulnerability (CVE-2023-12345) with no patch. Project abandoned in 2022. Using this package exposes your application to known exploitable vulnerabilities.

Use **modern-parser** instead—API-compatible drop-in replacement with CVE patches:

```python
# Before
from legacy_parser import Parser

# After
from modern_parser import Parser  # API-compatible
```

### Migration Path
1. Replace with `modern-parser` (API-compatible)
2. Test parsing behavior thoroughly
3. Run `pip-audit` to verify no other vulnerable deps
4. Monitor modern-parser security advisories

---

## Example 3: fast-compute (Rust) - ADOPT with Nuance

**User Request:** "I need a fast computation library for my Rust project. Is fast-compute good?"

**Package Context:**
- Name: fast-compute (crates.io)
- Dependency Type: Standard (performance-critical)
- Use Case: High-performance numerical computations

### Summary
Excellent single-maintainer library with outstanding code quality, documentation, and performance. Single maintainer is highly skilled and responsive. The bus factor of 1 is the only significant concern, but overall quality justifies adoption with proper risk mitigation.

**Recommendation**: ADOPT (with monitoring)
**Risk Level**: Medium
**Blockers Found**: No

### Evaluation Scores

| Signal (Weight) | Score | Evidence |
|-----------------|-------|----------|
| Maintenance (H) | 4/5   | Last release v1.8.2 on 2025-01-05. Bi-monthly releases. Commits 2-3x/week. |
| Security (H) | 5/5   | Zero CVEs. 95% `#![forbid(unsafe_code)]`. 5% unsafe well-documented. Passes cargo-audit. |
| Community (M) | 3/5   | Single maintainer (asmith) but very responsive. 12 contributors for small PRs. Issues answered 24-48hr. |
| Documentation (M) | 5/5   | Excellent docs.rs. Comprehensive examples. API reference with math explanations. |
| Dependency Footprint (M) | 5/5   | 3 total deps (num-traits, rayon, serde). All tier-1 crates. |
| Production Adoption (M) | 4/5   | 52k downloads. 60+ crate dependents. In awesome-rust list. 2 known production users. |
| License (H) | 5/5   | MIT/Apache-2.0 dual (Rust standard). Clean dep licenses. |
| API Stability (M) | 5/5   | v1.x stable 2 years. Strict semver. 1 breaking change (well-communicated). |
| Funding (M) | 2/5   | No corporate backing. GitHub Sponsors: 3 sponsors, $50/mo. No sustainability plan. |
| Ecosystem Momentum (M) | 4/5   | Growing adoption in Rust scientific computing. Active community discussion. |

**Weighted Score**: 42/50

### Key Findings

**Strengths:**
- Exceptional performance (3-5x faster than alternatives)
- Outstanding docs.rs documentation with mathematical proofs
- Minimal unsafe code (95% safe, 5% expertly justified)
- Highly responsive maintainer (24-48hr triage)
- Clean dependencies (tier-1 crates only)

**Concerns:**
- Bus factor = 1 (single maintainer, no succession plan)
- Limited funding ($50/month)
- Project depends entirely on one person's availability

### Alternatives Considered
- **compute-rs**: More contributors but slower performance, less complete docs
- **sci-compute**: Corporate backing but heavier deps, less idiomatic Rust
- **nalgebra**: More general-purpose, well-maintained, less specialized

### Recommendation Details
fast-compute demonstrates how one skilled maintainer can produce outstanding software. Code quality, documentation, and performance are all excellent. The maintainer (asmith) has shown 2+ years of consistent, responsive maintenance.

**Single-maintainer risk is real but manageable.** This pattern is common in Rust—many excellent crates have one primary maintainer. The question is whether benefits outweigh risks.

**Choose this when:**
- Performance advantage (3-5x) is significant for your use case
- Your team can fork/maintain if needed
- Rust expertise available to maintain fork
- Specialized functionality justifies risk

**Choose alternative when:**
- Organization requires multi-maintainer policy
- Cannot maintain a fork
- compute-rs or sci-compute meet performance needs

### If You Proceed
- **Sponsor the project**: $20-50/month helps sustainability
- **Monitor actively**: Watch for maintenance velocity changes
- **Build relationship**: Engage constructively in issues/PRs
- **Fork strategy**: Ensure team can fork if needed
- **Consider contributing**: Reduces bus factor, builds familiarity
- **Vendor dependency**: `cargo vendor` for production
- **Pin carefully**: `fast-compute = "1.8"` for patches only

---

## Example 4: mega-framework (npm) - EVALUATE FURTHER

**User Request:** "Should I use mega-framework for my new web application?"

**Package Context:**
- Name: mega-framework (npm)
- Dependency Type: Critical (application framework)
- Use Case: Full-stack SaaS application

### Summary
Comprehensive, well-maintained framework with excellent community and corporate backing. However, 203-dependency footprint with some unmaintained transitive deps and 2.4MB bundle size create significant concerns. Decision depends heavily on specific project requirements and constraints.

**Recommendation**: EVALUATE FURTHER
**Risk Level**: Medium
**Blockers Found**: No (but significant concerns)

### Evaluation Scores

| Signal (Weight) | Score | Evidence |
|-----------------|-------|----------|
| Maintenance (H) | 4/5   | Last release v5.2.0 on 2025-01-15. Monthly releases. 200+ contributors. |
| Security (H) | 4/5   | SECURITY.md present. 3 CVEs in 2024, patched 7-14 days. Large attack surface concern. |
| Community (M) | 5/5   | 200+ contributors, 15 core team. PRs merged quickly. Discord 5k+ members. health_percentage: 92. |
| Documentation (M) | 5/5   | Excellent docs site. Comprehensive tutorials, API reference, guides. Active blog. |
| Dependency Footprint (L) | 2/5   | **Heavy**: 203 total deps (15 direct, 188 transitive). 3 unmaintained 2+ years. Bundle: 2.4MB. |
| Production Adoption (M) | 5/5   | 350k weekly downloads. Used by TechCorp, DataCo, CloudSystems. Case studies available. |
| License (H) | 5/5   | MIT. 2 deps Apache-2.0, rest MIT/BSD. No conflicts. |
| API Stability (M) | 3/5   | Major versions (v4→v5) required substantial refactoring. Deprecation warnings provided. |
| Funding (H) | 5/5   | Backed by Mega Corp (public). 10 full-time engineers. OpenCollective: $45k/mo. |
| Ecosystem Momentum (M) | 4/5   | Strong momentum, competitors emerging. Top-3 in category. 500+ plugins. |

**Weighted Score**: 39/50

### Key Findings

**Strengths:**
- Comprehensive batteries-included framework
- Excellent docs and active community
- Well-funded with dedicated team
- Production-proven at major companies
- Active development and security response

**Concerns:**
- **203 total dependencies** (extreme)
- **3 unmaintained transitive deps**: old-event-emitter (2yr), legacy-promisify (3yr), util-deprecated (2yr)
- **2.4MB bundle size** significant weight
- **Complex migrations**: v4→v5 required substantial refactoring
- **High lock-in**: Switching frameworks very costly

### Unmaintained Transitive Dependencies
1. **old-event-emitter** (2 years) - via router-lib
2. **legacy-promisify** (3 years) - via async-helpers → data-layer
3. **util-deprecated** (2 years) - via build-tools

Mega Corp aware (issue #4521) but hasn't prioritized replacement.

### Alternatives Considered
- **slim-framework**: 45 total deps, modular, growing. Less mature.
- **modern-stack**: Newer, 80 deps, lighter. Less production-proven.
- **Build-your-own**: Use focused libraries (react-router, redux, vite). More work, more flexibility.

### Recommendation Details
mega-framework is **mixed**. Well-maintained and production-ready with strong backing. For teams valuing comprehensive solutions and accepting the weight, it's viable.

**The 203-dependency footprint is concerning**, especially with unmaintained transitive deps. This is technical debt and potential security risk.

### Decision Framework

**Choose mega-framework if:**
- You value comprehensive integration over modularity
- Have security resources to monitor 200+ deps
- Need full feature set (SSR, routing, state, build, testing)
- Bundle size not critical (internal tools, admin dashboards)
- Can handle complex major version migrations

**Choose alternative if:**
- Minimize dependencies/bundle size is priority
- Prefer modular, focused libraries
- Performance critical (public web, mobile)
- Want component flexibility

**Recommendation: Evaluate slim-framework first.** Similar DX with 1/5 the dependencies. If insufficient, mega-framework acceptable *with monitoring*.

### If You Proceed
- **Monitor deps**: `npm audit` in CI, Dependabot for 203 deps
- **Security advisories**: Critical given attack surface
- **Budget migrations**: Plan 2-4 weeks for major versions
- **Track unmaintained deps**: Monitor old-event-emitter, legacy-promisify, util-deprecated
- **Tree-shaking**: Use modular imports
- **Measure bundle impact**: Profile before committing
- **Use LTS versions**: v5 LTS for stability

---

## Key Takeaways from Examples

### Pattern Recognition

1. **Single maintainer ≠ automatic rejection** (fast-compute): Assess quality, responsiveness, track record
2. **Abandonment + CVEs = AVOID** (legacy-parser): Security vulns without patches are dealbreakers
3. **Corporate backing ≠ perfect** (mega-framework): Well-funded projects can have concerning dependencies
4. **Multiple strong signals overcome weaknesses** (ExampleCo): Excellence across signals builds confidence

### Evaluation Best Practices

- **Weight appropriately**: Security and maintenance > documentation
- **Context matters**: Heavy framework may be fine for internal tools, not public sites
- **Provide alternatives**: Always suggest alternatives for AVOID or EVALUATE FURTHER
- **Be specific**: Cite versions, dates, CVEs, metrics
- **Acknowledge trade-offs**: Few packages are perfect

### Recommendation Clarity

- **ADOPT**: Clear benefits, low/acceptable risk, concerns don't outweigh strengths
- **AVOID**: Dealbreaker issues (security, abandonment, licensing) + alternatives
- **EVALUATE FURTHER**: Mixed signals, decision depends on user context/priorities

## How to Use These Examples

1. **Template evaluations**: Follow structure (Summary, Scores, Findings, Alternatives, Recommendation)
2. **Gather real data**: These are hypothetical—run actual commands for real evaluations
3. **Adapt weighting**: Adjust signal weights for dependency type (critical vs dev)
4. **Cite evidence**: Include specific versions, dates, metrics, command outputs
5. **Consider context**: Risk tolerance varies by project
6. **Think critically**: Don't mechanically score—understand nuances
