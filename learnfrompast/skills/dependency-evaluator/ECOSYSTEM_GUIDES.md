# Ecosystem-Specific Evaluation Guides

Different language ecosystems have different norms, risks, and best practices. Use this guide to adjust your evaluation criteria based on the package ecosystem.

## Table of Contents

- [Ecosystem Baselines](#ecosystem-baselines)
- [Node.js / npm](#nodejs--npm)
- [Python / PyPI](#python--pypi)
- [Rust / Cargo](#rust--cargo)
- [Go](#go)
- [Ruby / RubyGems](#ruby--rubygems)
- [Java / Maven Central](#java--maven-central)
- [Cross-Ecosystem Patterns](#cross-ecosystem-patterns)
- [Adjusting Your Evaluation](#adjusting-your-evaluation)

---

## Ecosystem Baselines

Use these baselines for ecosystem-relative comparisons. These represent typical patterns as of 2025; use as context not rigid rules.

### Release Cadence Norms

| Ecosystem | Actively Developed | Mature/Stable | Concerning |
|-----------|-------------------|---------------|------------|
| npm | Monthly+ releases | Quarterly releases | >6 months no release |
| PyPI | Monthly-quarterly | Bi-annual releases | >9 months no release |
| Cargo | Bi-monthly to quarterly | Annual releases OK | >12 months no release |
| Go | Quarterly typical | Annual releases OK | >12 months no release |
| RubyGems | Monthly for Rails-related | Quarterly for utilities | >6 months no release |
| Maven | Quarterly typical | Bi-annual for mature | >9 months no release |

**Key:** "Concerning" means outlier for actively developed packages; mature packages may legitimately have longer gaps.

### Dependency Count Norms

| Ecosystem | Light | Typical | Heavy | Extreme |
|-----------|-------|---------|-------|---------|
| npm | <10 | 20-50 | 100-150 | 200+ |
| PyPI | <5 | 10-30 | 50-80 | 100+ |
| Cargo | <10 | 20-40 | 60-80 | 100+ |
| Go | <5 | 5-20 | 30-40 | 50+ |
| RubyGems | <5 | 10-25 | 40-60 | 80+ |
| Maven | <10 | 20-50 | 80-120 | 150+ |

**Counts are total transitive dependencies.** Adjust expectations based on package type (frameworks have more).

### Download Thresholds (Weekly)

| Ecosystem | Niche | Moderate | Popular | Very Popular |
|-----------|-------|----------|---------|--------------|
| npm | <500 | 1k-10k | 50k-100k | 500k+ |
| PyPI | <100 | 500-5k | 20k-50k | 200k+ |
| Cargo | <50 | 200-2k | 10k-30k | 100k+ |
| RubyGems | <100 | 500-5k | 20k-50k | 200k+ |

**Note:** Downloads alone don't indicate quality. Niche packages can be excellent; popular packages can be deprecated.

### Issue Response Time Norms

| Ecosystem | Excellent | Good | Acceptable | Concerning |
|-----------|-----------|------|------------|------------|
| npm (popular) | Hours-1 day | 2-7 days | 2-4 weeks | >1 month |
| npm (smaller) | 1-3 days | 1-2 weeks | 1 month | >2 months |
| PyPI | 1-3 days | 1-2 weeks | 3-4 weeks | >1 month |
| Cargo | 1-2 days | 3-7 days | 2-3 weeks | >1 month |
| Go | 1-3 days | 1-2 weeks | 3-4 weeks | >1 month |

**For security issues:** Expect 24-48hr acknowledgment regardless of ecosystem.

### Documentation Expectations

| Ecosystem | Minimum Expected | Excellent |
|-----------|------------------|-----------|
| npm | README with examples, TypeScript types | Dedicated docs site, migration guides, playground |
| PyPI | README with examples, type hints | ReadTheDocs site, Sphinx docs, examples repo |
| Cargo | README with examples, rustdoc | docs.rs complete, examples in repo, book/guide |
| Go | README with examples, godoc | pkg.go.dev complete, examples, design docs |
| RubyGems | README with examples | RDoc/YARD docs, Rails integration guide |

### Comparative Assessment Guidelines

**Use these baselines to ask:**
- Is this package's release cadence below the norm for its ecosystem and maturity level?
- Is the dependency count in the top quartile for similar packages in this ecosystem?
- Is the issue response time significantly slower than ecosystem expectations?
- Are downloads declining while ecosystem overall is growing?

**Example application:**
- npm package with 150 transitive deps → "Heavy" but not extreme; acceptable for framework, concerning for utility
- Cargo crate with no release in 10 months → Not yet concerning for mature stable crate
- PyPI package with 200 deps → Extreme; investigate why so many
- Go module with 40 deps → Unusual for Go (stdlib-first culture); investigate

---

## Node.js / npm

### Ecosystem Characteristics
- **Philosophy**: Micropackages are common; many tiny single-purpose modules
- **Package count**: Over 2 million packages (largest ecosystem)
- **Dependency culture**: Deep dependency trees are normalized
- **Versioning**: Semver is standard but not always followed strictly

### Unique Risks

**Left-pad Risk**
The infamous "left-pad incident" (2016) highlighted npm's vulnerability to tiny, critical packages being removed. Characteristics:
- Single-function packages with disproportionate usage
- High download counts but minimal functionality
- Supply chain risk when widely used packages are yanked

**npm-specific Supply Chain Attacks**
- Typosquatting is common (react vs. reakt)
- Package name confusion attacks
- Malicious install scripts in postinstall hooks
- Maintainer account compromises

### What to Watch For
- Packages with hundreds of transitive dependencies for simple tasks
- Postinstall scripts that download external code
- Packages that wrap simple native functionality unnecessarily
- Extremely high download counts but minimal GitHub activity (bot inflation)

### Preferred Patterns
- Packages with minimal dependencies
- Well-established micro-utilities from trusted authors
- Scoped packages (@organization/package) from known orgs
- Packages with verified publishers

### Recommended Tools
```bash
npm ls --all                    # Visualize full dependency tree
npm audit                       # Security vulnerability scanning
npm pack --dry-run              # Check bundle size
```

### Ecosystem-Specific Red Flags
- Packages requiring sudo or elevated permissions
- Packages with network calls in postinstall
- Packages with native dependencies when pure JS would suffice
- Suspicious similarity to popular package names

### Ecosystem-Specific Green Flags
- TypeScript type definitions included
- ES modules support
- Tree-shakeable exports
- Zero dependencies for utility packages

## Python / PyPI

### Ecosystem Characteristics
- **Philosophy**: "Batteries included" - stdlib-first approach
- **Package count**: Over 400,000 packages
- **Dependency culture**: Lighter dependency trees than npm
- **Versioning**: Mix of semver and date-based versioning

### Unique Risks

**PyPI Supply Chain Attacks**
- Notable typosquatting incidents (e.g., python3-dateutil vs. dateutil)
- Malicious packages targeting data scientists (fake ML libraries)
- Native code in wheels may contain malware
- setup.py can execute arbitrary code during install

**Dependency Confusion**
- Public PyPI packages with same names as private packages
- pip installs public version instead of intended private one

### What to Watch For
- Packages with names very similar to popular packages
- Unusual wheel distributions without source code
- Packages targeting specific communities (ML, data science) with suspicious features
- setup.py files with network calls or obfuscated code

### Preferred Patterns
- Packages from known maintainers and organizations
- Packages with signed releases (GPG signatures)
- Pure Python packages (no compiled extensions) when possible
- Packages maintained by Python Software Foundation or sub-projects

### Recommended Tools
```bash
pip show <package>              # View package metadata
pip index versions <package>    # Check version history
# Use pip-audit for security scanning (install separately)
```

### Ecosystem-Specific Red Flags
- Packages requesting unnecessary permissions in setup
- Typosquatting of popular packages (reqeusts vs. requests)
- Obfuscated code in setup.py
- Wheels only (no source distribution)

### Ecosystem-Specific Green Flags
- Listed in Python Packaging Authority (PyPA)
- Type hints (PEP 484) included
- Both source distributions and wheels available
- Active maintenance by known Python community members

## Rust / Cargo

### Ecosystem Characteristics
- **Philosophy**: Safety and correctness-first; explicit is better than implicit
- **Package count**: Over 100,000 crates
- **Dependency culture**: Moderate dependencies; emphasis on correctness
- **Versioning**: Strict semver adherence is cultural norm

### Unique Strengths
- Strong compile-time guarantees reduce certain vulnerability classes
- Cargo's built-in tooling is excellent (cargo tree, cargo metadata)
- Culture of good documentation (docs.rs)
- `#![forbid(unsafe_code)]` for packages avoiding unsafe blocks

### What to Watch For
- Crates pulling in many proc-macro dependencies (slow compile times)
- Heavy use of `unsafe` blocks without justification
- Transitive dependencies with unsafe code when unnecessary
- Version conflicts in dependency tree (Cargo is strict about this)

### Preferred Patterns
- Crates with `#![forbid(unsafe_code)]` for non-performance-critical code
- Well-documented use of unsafe with safety invariants explained
- Minimal proc-macro dependencies
- Idiomatic Rust patterns

### Recommended Tools
```bash
cargo tree -p <crate>           # Dependency tree visualization
cargo metadata --format-version 1  # Machine-readable metadata
cargo audit                     # Security vulnerability scanning (install separately)
```

### Ecosystem-Specific Red Flags
- Excessive unsafe code without documentation
- Non-idiomatic Rust (indicates unfamiliarity)
- Proc-macro heavy for simple functionality
- Breaking semver (very rare in Rust ecosystem)

### Ecosystem-Specific Green Flags
- Published on docs.rs with comprehensive documentation
- `#![forbid(unsafe_code)]` or well-justified unsafe usage
- Fast compile times relative to functionality
- Active maintenance by Rust community members
- Inclusion in "awesome-rust" lists

## Go

### Ecosystem Characteristics
- **Philosophy**: Simplicity, minimalism, stdlib-first
- **Package count**: Smaller than npm/PyPI (by design)
- **Dependency culture**: Fewer dependencies is idiomatic
- **Versioning**: Go modules with semantic versioning

### Unique Strengths
- Strong standard library reduces dependency needs
- Built-in dependency management (go mod)
- Static linking produces standalone binaries
- Import paths explicitly reference source repositories

### What to Watch For
- Packages that wrap stdlib with minimal added value
- Deep dependency trees (unusual in Go)
- Packages that violate Go idioms and conventions
- Module paths not matching repository structure

### Preferred Patterns
- Prefer stdlib solutions when available
- Minimal external dependencies
- Clear, simple APIs following Go conventions
- Well-structured module paths (github.com/org/project)

### Recommended Tools
```bash
go list -m -versions <module>   # List module versions
go mod graph                    # Dependency graph
go mod why <module>             # Why is this dependency included
```

### Ecosystem-Specific Red Flags
- Wrapping stdlib unnecessarily
- Complex APIs when simple would suffice
- Not following Go Project Layout
- Vendoring dependencies (uncommon with go mod)

### Ecosystem-Specific Green Flags
- Minimal dependencies (< 5 direct deps)
- Follows effective Go guidelines
- Clear documentation and examples
- Used in prominent Go projects

## Ruby / RubyGems

### Ecosystem Characteristics
- **Philosophy**: Convention over configuration, developer happiness
- **Package count**: Over 175,000 gems
- **Dependency culture**: Moderate; gems often do a lot
- **Versioning**: Generally follows semver

### Unique Characteristics
- Gems often monkey-patch core classes (can cause conflicts)
- Rails ecosystem dominates Ruby gem ecosystem
- Strong community conventions

### What to Watch For
- Gems that extensively monkey-patch core classes
- Dependencies that conflict with Rails (if using Rails)
- Gems that override standard library behavior
- Unmaintained gems for Rails version compatibility

### Preferred Patterns
- Well-documented gems with clear upgrade paths
- Gems that minimize monkey-patching
- Rails-compatible versioning (if applicable)
- Active maintenance matching Rails release cycles

### Recommended Tools
```bash
gem list <gem>                  # List installed versions
gem dependency <gem>            # Show dependencies
bundle outdated                 # Check for updates (in bundler projects)
```

### Ecosystem-Specific Red Flags
- Extensive monkey-patching without documentation
- Incompatibility with major Rails versions
- Gems requiring old Ruby versions
- No Bundler compatibility

### Ecosystem-Specific Green Flags
- Rails-compatible (if relevant)
- Minimal monkey-patching or well-documented overrides
- Active maintenance matching Ruby version releases
- Listed in awesome-ruby or Ruby Toolbox

## Java / Maven Central

### Ecosystem Characteristics
- **Philosophy**: Enterprise-ready, battle-tested
- **Package count**: Over 500,000 artifacts
- **Dependency culture**: Can be heavy; mature dependency resolution
- **Versioning**: Mix of semver and date-based

### Unique Strengths
- Mature ecosystem with established governance
- Strong backward compatibility culture
- Extensive enterprise adoption and vetting
- Maven Central has quality standards

### What to Watch For
- Dependency version conflicts (dependency hell)
- Transitive dependencies pulling in multiple versions
- Large artifact sizes
- Complex dependency trees

### Preferred Patterns
- Well-maintained artifacts from reputable organizations
- Clear compatibility matrices (Java version, framework version)
- Semantic versioning adherence
- Artifacts hosted on Maven Central (not random repos)

### Recommended Tools
```bash
mvn dependency:tree             # Dependency tree visualization
mvn dependency:analyze          # Unused dependency analysis
mvn versions:display-dependency-updates  # Check for updates
```

### Ecosystem-Specific Red Flags
- Artifacts only in obscure Maven repos
- Complex dependency resolution issues
- No Java version compatibility documented
- Transitive dependencies with licensing issues

### Ecosystem-Specific Green Flags
- Published to Maven Central
- Apache or Eclipse Foundation backing
- Clear Java version support policy
- Spring ecosystem compatibility (if relevant)
- OSGi bundle metadata (for OSGi projects)

## Cross-Ecosystem Patterns

### Supply Chain Security Varies by Ecosystem

**Highest Risk:**
- npm (largest attack surface, numerous incidents)
- PyPI (targeted attacks on data scientists)

**Medium Risk:**
- Maven (occasional but usually caught quickly)
- RubyGems (smaller ecosystem, fewer incidents)

**Lower Risk:**
- Cargo (newer, security-conscious culture)
- Go (stdlib-first reduces attack surface)

### Dependency Tree Norms

**Expect Heavier Trees:**
- npm (100+ transitive deps can be normal)
- Maven (enterprise frameworks bring many deps)

**Expect Lighter Trees:**
- Go (< 20 transitive deps typical)
- Rust (20-50 deps common)
- Python (30-60 deps typical)

### Versioning Discipline

**Strict Semver:**
- Rust/Cargo (breaking semver is rare)
- npm (expected but not always followed)

**Flexible Versioning:**
- Maven (mix of approaches)
- Python (mix of semver and datever)

### Documentation Culture

**Excellent Documentation Expected:**
- Rust (docs.rs standard)
- Python (ReadTheDocs common)

**Variable Documentation:**
- npm (ranges from excellent to none)
- Maven (often enterprise-focused docs)

## Adjusting Your Evaluation

### For npm Packages
- **Increase weight on**: Dependency Footprint, Security Posture
- **Be more lenient on**: Single maintainer (common for utilities)
- **Extra scrutiny for**: Packages with < 50 lines of code but high usage

### For Python Packages
- **Increase weight on**: Security Posture (typosquatting risk)
- **Be more lenient on**: Lower download counts (smaller ecosystem)
- **Extra scrutiny for**: Packages targeting data scientists/ML engineers

### For Rust Crates
- **Increase weight on**: API Stability, Documentation Quality
- **Be more lenient on**: Compile-time dependencies (proc-macros)
- **Extra scrutiny for**: Excessive unsafe code usage

### For Go Modules
- **Increase weight on**: Simplicity, Minimal Dependencies
- **Be more lenient on**: Lower GitHub stars (smaller community)
- **Extra scrutiny for**: Packages wrapping stdlib unnecessarily

### For Ruby Gems
- **Increase weight on**: Rails compatibility (if applicable)
- **Be more lenient on**: Monkey-patching (if well-documented)
- **Extra scrutiny for**: Core class modifications

### For Java Artifacts
- **Increase weight on**: Enterprise Adoption, Backward Compatibility
- **Be more lenient on**: Larger dependency trees (framework norm)
- **Extra scrutiny for**: Artifacts not on Maven Central
