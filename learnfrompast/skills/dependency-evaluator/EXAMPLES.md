# Dependency Evaluation Examples

## Important Note

**These are hypothetical examples for demonstration purposes only.** They show how to structure evaluation reports, not actual package recommendations.

For real evaluations:
- Run actual commands to gather current data
- Cite specific versions, dates, and metrics
- Verify information is current before making decisions
- Don't rely on these examples as factual assessments

---

## Example 1: well-maintained-lib (High Quality, Widely Adopted)

### Summary
well-maintained-lib is a hypothetical utility library with excellent maintenance practices, strong community support, and proven production reliability. This example demonstrates evaluating a high-quality, low-risk dependency.

**Recommendation**: ADOPT
**Risk Level**: Low
**Blockers Found**: No

### Evaluation Scores

| Signal | Score | Weight | Notes |
|--------|-------|--------|-------|
| Maintenance | 5/5 | H | Regular releases every 2-3 months, last release 3 weeks ago (v4.2.1) |
| Security | 5/5 | H | Security policy documented, 2 CVEs in history both patched within 48 hours |
| Community | 5/5 | H | 45 active contributors, PRs merged within 3-7 days |
| Documentation | 5/5 | M | Comprehensive docs site, API reference, migration guides for each major version |
| Dependency Footprint | 5/5 | L | Zero dependencies, 45KB minified+gzipped |
| Production Adoption | 5/5 | M | 180K+ dependents on npm, used by Fortune 500 companies |
| License | 5/5 | H | MIT license, no transitive license issues |
| API Stability | 5/5 | M | Strict semver since v1.0, currently at v4.2.1, clear deprecation policy |
| Funding/Sustainability | 4/5 | M | OpenCollective with $15K/year, 3 full-time maintainers employed by sponsoring companies |
| Ecosystem Momentum | 4/5 | L | Mature ecosystem, some functionality now available in language built-ins |

**Weighted Score**: 47/50

### Key Findings

#### Strengths
- Zero-dependency architecture eliminates supply chain risks
- Proven at scale with millions of daily downloads
- Strong security track record with quick CVE response times
- Active, diverse contributor base reduces bus factor
- Excellent documentation reduces onboarding friction

#### Concerns
- Some functionality overlaps with modern language built-ins (though library still adds value)
- Bundle size acceptable but not minimal (45KB could be 20KB if refactored)
- Funding is adequate but not exceptional for project scale

### Alternatives Considered
- **native-features**: For simple use cases, language built-ins may suffice
- **lightweight-alternative**: Smaller bundle (15KB) but less comprehensive API
- **competing-lib**: Similar features but less mature (only v2.0)

### Recommendation Details
well-maintained-lib represents a textbook example of a high-quality dependency. Strong maintenance, security practices, community health, and production adoption make it low-risk. The zero-dependency footprint and permissive license eliminate common concerns.

### If You Proceed
- **Version strategy**: Pin to v4.x, review release notes for each minor update
- **Import strategy**: Use tree-shakeable imports where available to minimize bundle size
- **Monitoring**: Subscribe to GitHub releases and security advisories
- **Performance**: Profile bundle size impact; consider code-splitting for large imports
- **Consider alternatives**: Evaluate if newer language features can replace simpler use cases

---

## Example 2: tiny-util (Micro-Package with Supply Chain Risk)

### Summary
tiny-util is a hypothetical single-purpose utility package providing 15 lines of functionality. While technically sound, it represents disproportionate supply chain risk for minimal value.

**Recommendation**: AVOID - Write yourself
**Risk Level**: High (disproportionate risk-to-value ratio)
**Blockers Found**: Yes

### Blockers
- ⛔ Extreme risk-to-value ratio: 15 lines of simple code creates unnecessary supply chain dependency
- ⛔ Functionality trivially reproducible with language built-ins or 5 minutes of coding

### Evaluation Scores

| Signal | Score | Weight | Notes |
|--------|-------|--------|-------|
| Maintenance | 3/5 | H | Single maintainer, sporadic updates (last release 4 months ago) |
| Security | 4/5 | H | No inherent vulnerabilities, but package could be compromised |
| Community | 2/5 | H | Solo developer, no backup maintainers, 0 recent PR activity |
| Documentation | 3/5 | M | README explains usage clearly, but minimal examples |
| Dependency Footprint | 5/5 | M | Zero dependencies, 1.2KB total |
| Production Adoption | 4/5 | M | 50K+ dependents (high for such simple functionality) |
| License | 5/5 | H | MIT license |
| API Stability | 5/5 | M | Stable v1.x API, unchanged for 2 years |
| Funding/Sustainability | 1/5 | H | No funding, volunteer-maintained |
| Ecosystem Momentum | 3/5 | L | Usage remains stable but no growth |

**Weighted Score**: 28/50 (but AVOID due to blocker)

### Key Findings

#### Strengths
- Simple, focused functionality
- No dependencies reduces some risks
- Permissive license
- Proven stability (API unchanged)

#### Concerns
- **Critical**: 15 lines of code creates major supply chain dependency
- Single point of failure (one maintainer with npm publish rights)
- Functionality easily implementable in-house
- Risk massively outweighs benefit
- Package could be removed, compromised, or abandoned

### Alternative Solution
```javascript
// Implement yourself (5 minutes):
function utilityFunction(input, options = {}) {
  // 10-15 lines of straightforward logic
  // Full control, no external dependency
  // Can be customized to exact needs
  return result;
}

// Or use language built-ins:
// Modern languages often have this functionality natively
```

### Recommendation Details
This exemplifies when NOT to add a dependency. The infamous left-pad incident (2016) demonstrated that tiny packages can create massive ecosystem disruption. For such simple functionality, in-house implementation is vastly safer and provides full control.

### Cost-Benefit Analysis
- **Dependency cost**: Supply chain risk, package management overhead, potential for removal/compromise
- **Dependency value**: Saves 5 minutes of implementation time
- **Verdict**: Cost >>> Value

### Lessons Learned
- Simple utilities often aren't worth the dependency risk
- Consider bus factor even for "safe" code
- Maintain control over critical functionality
- Language built-ins often replace simple utilities

---

## Example 3: modern-alternative (Quality Library, Lower Popularity)

### Summary
modern-alternative is a hypothetical well-designed library that solves a problem better than established alternatives, but has lower download counts due to being newer. This demonstrates not penalizing quality for popularity.

**Recommendation**: ADOPT
**Risk Level**: Low
**Blockers Found**: No

### Evaluation Scores

| Signal | Score | Weight | Notes |
|--------|-------|--------|-------|
| Maintenance | 5/5 | H | Active development, releases every 3-4 weeks, responsive maintainers |
| Security | 5/5 | H | Zero CVEs, security-conscious architecture, Dependabot enabled |
| Community | 4/5 | H | 25 contributors, growing community, responsive to issues within 24-48 hours |
| Documentation | 5/5 | M | Excellent docs site, migration guide from competing-lib, comprehensive examples |
| Dependency Footprint | 5/5 | M | Zero dependencies, tree-shakeable, 12KB minified+gzipped |
| Production Adoption | 3/5 | M | 8K dependents (low compared to established alternative with 200K, but growing 40% YoY) |
| License | 5/5 | H | MIT license |
| API Stability | 5/5 | M | Stable v2.x API, excellent semver adherence, clear deprecation cycle |
| Funding/Sustainability | 3/5 | M | GitHub Sponsors with modest funding, 2 part-time maintainers |
| Ecosystem Momentum | 5/5 | L | Rapidly growing, recommended in official framework documentation, conference talks |

**Weighted Score**: 45/50

### Key Findings

#### Strengths
- Modern architecture solving known problems with established alternatives
- Superior design (immutable, functional, tree-shakeable)
- Excellent documentation including migration guides
- Zero dependencies eliminates security concerns
- Growing ecosystem momentum (40% YoY growth)
- Framework vendors recommending as best practice

#### Concerns
- Smaller community than 10-year-old established alternative
- Less Stack Overflow coverage (newer library)
- Some developers unfamiliar with modern patterns
- Lower download count might signal less battle-testing

### Alternatives Considered
- **established-lib**: 10x more downloads but deprecated, maintainers discourage new usage
- **minimal-alternative**: Smaller footprint (8KB) but less comprehensive
- **enterprise-option**: Corporate-backed but more complex, heavier (50KB)

### Recommendation Details
modern-alternative demonstrates that lower popularity doesn't indicate lower quality. Being newer with growing adoption is different from declining/abandoned. The superior architecture, excellent maintenance, and ecosystem momentum outweigh popularity concerns. Framework vendors recommending it signals quality validation.

### Context: Popularity vs. Quality
- Established alternative has 25x more downloads but is deprecated
- modern-alternative growing 40% YoY indicates market validation
- Quality metrics (maintenance, security, design) are excellent
- Being "newer" isn't a flaw when improving on established patterns

### If You Proceed
- **Version strategy**: Use stable v2.x, follow semver updates
- **Migration path**: Excellent migration docs from established-lib available
- **Team training**: Budget time for developers unfamiliar with modern patterns
- **Monitoring**: Watch ecosystem adoption and maintainer activity
- **Community**: Join GitHub Discussions for support (active community)

---

## Example 4: deprecated-package (Popular but Unmaintained)

### Summary
deprecated-package is a hypothetical library that was industry-standard for years but is now officially deprecated and unmaintained. Despite continued high download counts from legacy projects, it must not be used in new projects.

**Recommendation**: AVOID - Use maintained alternatives
**Risk Level**: High
**Blockers Found**: Yes

### Blockers
- ⛔ Officially deprecated by maintainers (announced 18 months ago)
- ⛔ No security updates will be provided
- ⛔ Known unfixed vulnerabilities (CVE-2023-XXXXX rated 7.5/10)

### Evaluation Scores

| Signal | Score | Weight | Notes |
|--------|-------|--------|-------|
| Maintenance | 1/5 | H | Deprecated, no commits for 18 months, issues closed without fixes |
| Security | 1/5 | H | 3 known CVEs unfixed, maintainers stated no patches will be released |
| Community | 2/5 | H | Historical community large, actively migrating away |
| Documentation | 4/5 | M | Comprehensive historical docs (frozen) |
| Dependency Footprint | 2/5 | M | 35+ transitive dependencies, several also unmaintained |
| Production Adoption | 3/5 | M | Still 100K+ weekly downloads (legacy projects), declining 15% quarterly |
| License | 5/5 | H | Apache-2.0 license (permissive) |
| API Stability | 5/5 | M | Stable (frozen forever) |
| Funding/Sustainability | 1/5 | H | No funding, maintainers moved to other projects |
| Ecosystem Momentum | 1/5 | L | Ecosystem migrated to alternatives, no conference mentions |

**Weighted Score**: 16/50 (AVOID due to deprecation blocker)

### Key Findings

#### Strengths (Historical)
- Was industry-standard for 8+ years
- Comprehensive documentation and examples
- Wide historical adoption provided extensive Stack Overflow coverage
- Simple, well-understood API

#### Concerns
- **Critical**: Official deprecation with explicit "do not use in new projects" warning
- **Critical**: Known security vulnerabilities will never be patched
- **Critical**: Transitive dependencies also aging/unmaintained
- Large dependency tree (35+ packages) increases attack surface
- Download counts misleading (legacy projects, not new adoption)
- Maintainers recommend specific alternatives in deprecation notice

### Alternatives (Recommended by Maintainers)
- **modern-replacement**: Promise-based API, actively maintained, recommended by deprecated-package authors
- **lightweight-option**: Minimal dependencies, smaller footprint
- **framework-builtin**: Framework v3+ includes equivalent functionality natively

### Recommendation Details
Official deprecation is an absolute blocker regardless of other factors. No security patches means any newly discovered vulnerabilities will remain unfixed. High download counts are misleading—they reflect legacy usage, not suitability for new projects.

### Migration Context
For teams currently using deprecated-package:
1. **Assess impact**: Identify all usage in codebase
2. **Choose alternative**: modern-replacement offers easiest migration path
3. **Timeline**: Prioritize by security exposure (public-facing first)
4. **Testing**: HTTP/network libraries require thorough integration testing
5. **Monitor**: Run security audits before and after migration

### Migration Example
```javascript
// Old (deprecated-package)
deprecated.method('https://api.example.com', (err, res, body) => {
  if (err) return handleError(err);
  processData(body);
});

// New (modern-replacement)
try {
  const response = await modernReplacement.get('https://api.example.com');
  processData(response.data);
} catch (err) {
  handleError(err);
}
```

### Lessons Learned
- High download counts don't indicate current suitability
- Official deprecation overrides all other positive signals
- Security considerations are paramount—unmaintained = unacceptable
- Plan for dependency lifecycle in long-lived projects
- Ecosystem momentum matters—tools and standards evolve

---

## Comparative Summary

| Package | Type | Recommendation | Key Lesson |
|---------|------|----------------|------------|
| well-maintained-lib | Established, high-quality | ADOPT | Strong signals across all dimensions = low risk |
| tiny-util | Micro-package | AVOID | Simple code doesn't justify supply chain risk |
| modern-alternative | Quality newer option | ADOPT | Don't penalize quality for lower popularity |
| deprecated-package | Deprecated popular | AVOID | Deprecation and security override everything |

## How to Use These Examples

1. **Template your evaluations**: Follow the structure (Summary, Scores, Findings, Alternatives, Recommendation)
2. **Gather real data**: These are hypothetical—always run actual commands for real evaluations
3. **Adapt weighting**: Adjust signal weights based on your dependency type (critical vs. dev dependencies)
4. **Cite evidence**: Include specific versions, dates, metrics, and command outputs
5. **Consider context**: What works for one project may not fit another's risk tolerance
6. **Think critically**: Don't mechanically score—understand nuances and special circumstances
7. **Update regularly**: Real evaluations age quickly; re-evaluate critical dependencies periodically

## Structure Breakdown

Each example demonstrates:
- **Clear recommendation** with reasoning
- **Evidence-based scoring** (not gut feelings)
- **Balanced analysis** (strengths AND concerns)
- **Actionable alternatives** when recommending AVOID
- **Contextual guidance** for ADOPT recommendations
- **Lessons learned** to build evaluation intuition
