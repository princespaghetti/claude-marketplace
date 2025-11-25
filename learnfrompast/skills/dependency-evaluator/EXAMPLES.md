# Dependency Evaluation Examples

This file contains real-world evaluation examples demonstrating how to apply the evaluation framework to different types of packages. Use these as templates for your own evaluations.

## Example 1: lodash (Well-Maintained, Widely Adopted)

### Summary
lodash is a modern JavaScript utility library delivering modularity, performance, and extras. It's one of the most widely-used npm packages with proven production reliability.

**Recommendation**: ADOPT
**Risk Level**: Low
**Blockers Found**: No

### Evaluation Scores

| Signal | Score | Weight | Notes |
|--------|-------|--------|-------|
| Maintenance | 5/5 | H | Regular releases, last update < 1 month ago |
| Security | 5/5 | H | Quick CVE response, active security scanning |
| Community | 5/5 | H | 50+ contributors, responsive maintainers |
| Documentation | 5/5 | M | Excellent docs site with all methods documented |
| Dependency Footprint | 5/5 | L | Zero dependencies, modular imports supported |
| Production Adoption | 5/5 | M | 150K+ dependents, used by major companies |
| License | 5/5 | H | MIT license, very permissive |
| API Stability | 5/5 | M | Stable API at v4.x, semver compliant |
| Funding/Sustainability | 4/5 | M | OpenCollective, multiple sponsors |
| Ecosystem Momentum | 4/5 | L | Mature but some moving to native alternatives |

**Weighted Score**: 48/50

### Key Findings

#### Strengths
- Zero dependencies eliminates transitive dependency risks
- Extensively battle-tested in production (millions of projects)
- Modular design allows importing only needed functions
- Comprehensive test coverage and documentation
- Consistent API with clear deprecation cycles

#### Concerns
- Some functions now duplicated by ES6+ native methods
- Bundle size can be large if importing entire library
- Ecosystem slowly moving toward native alternatives for simple cases

### Alternatives Considered
- **Native ES6+ methods**: For simple array/object operations
- **lodash-es**: ES modules version for better tree-shaking
- **ramda**: For functional programming approach

### Recommendation Details
lodash remains an excellent choice for projects needing comprehensive utility functions. The package is mature, well-maintained, and has proven reliability. The zero-dependency footprint and modular structure make it low-risk even for large applications.

### If You Proceed
- **Version strategy**: Pin to specific v4.x version, update quarterly
- **Import strategy**: Use modular imports (`import map from 'lodash/map'`) for better tree-shaking
- **Monitoring**: Watch for security advisories (rare but quick to patch)
- **Consider**: Evaluate each usage - simple operations might not need lodash

---

## Example 2: left-pad Incident (Cautionary Tale)

### Summary
The left-pad package (before 2016 removal) was an 11-line function for padding strings. The package's removal from npm broke thousands of builds, exposing dependency chain fragility.

**Recommendation**: AVOID - Write yourself
**Risk Level**: High (disproportionate risk for simple functionality)
**Blockers Found**: Yes

### Blockers
- ⛔ Extreme functionality-to-risk ratio: 11 lines of code creates supply chain vulnerability
- ⛔ Simple functionality easily implemented in-house with no dependencies

### Evaluation Scores

| Signal | Score | Weight | Notes |
|--------|-------|--------|-------|
| Maintenance | 3/5 | H | Was maintained, but single maintainer |
| Security | 4/5 | H | No inherent security issues in code |
| Community | 2/5 | H | Single maintainer, no backup |
| Documentation | 3/5 | M | Function was self-explanatory |
| Dependency Footprint | 5/5 | M | Zero dependencies |
| Production Adoption | 4/5 | M | Widely used (thousands of dependents) |
| License | 5/5 | H | MIT license |
| API Stability | 5/5 | M | Simple, stable API |
| Funding/Sustainability | 1/5 | H | Unfunded, single volunteer |
| Ecosystem Momentum | 2/5 | L | Highlighted supply chain risks |

**Weighted Score**: 30/50 (but AVOID due to blocker)

### Key Findings

#### Strengths
- Simple, focused functionality
- Zero dependencies
- Wide adoption indicated trust (before incident)

#### Concerns
- **Critical**: 11 lines of code creating major supply chain dependency
- Single point of failure (one person could remove it)
- Functionality trivially reproducible
- Risk greatly outweighs benefit

### Alternatives
```javascript
// Write it yourself (< 5 minutes):
function leftPad(str, len, char = ' ') {
  return String(char).repeat(Math.max(0, len - str.length)) + str;
}

// Or use native padStart (ES2017+):
str.padStart(len, char);
```

### Recommendation Details
This is a textbook example of when NOT to add a dependency. The left-pad incident (2016) demonstrated that even small, seemingly benign packages can create significant risk. For such simple functionality, in-house implementation or native methods are far safer.

### Lessons Learned
- Evaluate cost-benefit: Simple utilities often aren't worth the dependency
- Consider supply chain risk even for "safe" packages
- Bus factor matters even when code is simple
- Native language features often replace simple utilities

---

## Example 3: date-fns (Niche but High Quality)

### Summary
date-fns is a modern JavaScript date utility library with immutable functions and tree-shaking support. Despite lower download counts than moment.js, it represents superior modern design.

**Recommendation**: ADOPT
**Risk Level**: Low
**Blockers Found**: No

### Evaluation Scores

| Signal | Score | Weight | Notes |
|--------|-------|--------|-------|
| Maintenance | 5/5 | H | Active development, regular releases |
| Security | 5/5 | H | No CVEs, security-conscious design |
| Community | 4/5 | H | 20+ contributors, responsive core team |
| Documentation | 5/5 | M | Excellent docs with all functions explained |
| Dependency Footprint | 5/5 | M | Zero dependencies, tree-shakeable |
| Production Adoption | 4/5 | M | Growing adoption, 30K+ dependents |
| License | 5/5 | H | MIT license |
| API Stability | 5/5 | M | Stable v2.x API, clear semver |
| Funding/Sustainability | 3/5 | M | OpenCollective with modest funding |
| Ecosystem Momentum | 5/5 | L | Growing, recommended alternative to moment |

**Weighted Score**: 46/50

### Key Findings

#### Strengths
- Immutable, functional API (no date mutation bugs)
- Excellent tree-shaking (import only what you use)
- Comprehensive internationalization (i18n) support
- TypeScript-first design with excellent types
- Actively maintained with clear roadmap
- Zero dependencies eliminates security concerns

#### Concerns
- Smaller community than moment.js (but growing)
- Less Stack Overflow coverage than established alternatives
- Some learning curve for developers used to moment

### Alternatives Considered
- **moment.js**: Larger but deprecated, discourages new usage
- **day.js**: Smaller but less comprehensive API
- **Luxon**: From moment.js authors, more complex
- **Native Temporal API**: Future standard, not yet stable

### Recommendation Details
date-fns represents a modern, well-designed approach to date handling. The lower download counts compared to moment.js don't indicate quality issues - rather, it's a newer library solving the problem better. The immutable API, tree-shaking support, and active maintenance make it an excellent choice.

### If You Proceed
- **Version strategy**: Use v2.x, update with minor releases
- **Import strategy**: Import individual functions for optimal bundle size
- **TypeScript**: Leverage excellent built-in types
- **i18n**: Configure locales as needed (many available)
- **Monitoring**: Watch for v3.x (in development) migration path

---

## Example 4: request (Popular but Deprecated)

### Summary
The request package was the most popular HTTP client for Node.js for years but was fully deprecated in 2020. Despite high download counts, it should not be used in new projects.

**Recommendation**: AVOID - Use alternatives
**Risk Level**: High
**Blockers Found**: Yes

### Blockers
- ⛔ Officially deprecated by maintainers (February 2020)
- ⛔ No security updates will be provided
- ⛔ Large dependency footprint with known vulnerabilities

### Evaluation Scores

| Signal | Score | Weight | Notes |
|--------|-------|--------|-------|
| Maintenance | 1/5 | H | Officially deprecated, no updates since 2020 |
| Security | 2/5 | H | Known vulnerabilities, no patches |
| Community | 3/5 | H | Was large, now migrating away |
| Documentation | 4/5 | M | Still comprehensive (historical) |
| Dependency Footprint | 1/5 | M | 50+ transitive dependencies |
| Production Adoption | 3/5 | M | Still widely used (legacy), declining |
| License | 5/5 | H | Apache-2.0 license |
| API Stability | 5/5 | M | Stable (frozen) |
| Funding/Sustainability | 1/5 | H | No funding, officially unmaintained |
| Ecosystem Momentum | 1/5 | L | Ecosystem moved to alternatives |

**Weighted Score**: 18/50 (AVOID due to deprecation blocker)

### Key Findings

#### Strengths (Historical)
- Simple, intuitive API
- Extensive documentation and examples
- Wide adoption and community knowledge

#### Concerns
- **Critical**: Officially deprecated with no security updates
- **Critical**: Known security vulnerabilities unfixed
- Large dependency tree (50+ packages) increases attack surface
- Dependencies themselves may have vulnerabilities
- Maintainers explicitly recommend alternatives

### Alternatives (Recommended)
- **axios**: Most popular alternative, promise-based
- **got**: Modern, TypeScript-native, actively maintained
- **node-fetch**: Fetch API for Node.js
- **Native fetch**: Node.js 18+ includes fetch API

### Recommendation Details
Despite request's historical popularity and still-high download counts, it must be avoided. Official deprecation means no security patches will be released. The maintainers themselves recommend migrating to alternatives.

### If You're Using It (Migration Plan)
1. **Immediate action**: Audit all uses of request in codebase
2. **Choose alternative**: axios (simplest migration) or got (modern)
3. **Migration strategy**:
   ```javascript
   // Old (request)
   request('https://api.example.com', (err, res, body) => { ... });

   // New (axios)
   const response = await axios.get('https://api.example.com');
   const body = response.data;
   ```
4. **Test thoroughly**: HTTP clients have subtle differences
5. **Monitor**: Run security audits after migration

### Lessons Learned
- High download counts don't indicate current suitability
- Official deprecation is a hard blocker
- Ecosystem momentum matters - tools move on
- Plan for dependency migrations in long-lived projects

---

## Comparative Summary

| Package | Type | Recommendation | Key Lesson |
|---------|------|----------------|------------|
| lodash | Established utility | ADOPT | Battle-tested reliability with zero deps |
| left-pad | Micro-utility | AVOID | Write simple code yourself |
| date-fns | Modern alternative | ADOPT | Don't penalize for lower popularity if quality high |
| request | Deprecated popular | AVOID | Deprecation overrides all other signals |

## How to Use These Examples

1. **Template your evaluations**: Follow the structure (Summary, Scores, Findings, Alternatives, Recommendation)
2. **Adapt weighting**: Adjust signal weights based on your dependency type
3. **Cite evidence**: Include specific versions, dates, and metrics
4. **Consider context**: What works for one project may not fit another
5. **Think critically**: Don't mechanically score - understand the nuances
