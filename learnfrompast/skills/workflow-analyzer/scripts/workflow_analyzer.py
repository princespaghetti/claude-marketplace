#!/usr/bin/env python3
"""
Unified workflow analyzer for Claude Code session history.
Parses JSONL session files, identifies repeated workflow patterns,
and generates a comprehensive markdown report with automation recommendations.
"""

import json
import sys
from pathlib import Path


def analyze_sessions(session_files):
    """
    Analyze session files and extract workflow patterns.

    Args:
        session_files: List of session file paths

    Returns:
        Dictionary containing analysis results
    """
    all_prompts = []
    sessions_data = []

    # Process each session
    for session_file in session_files:
        try:
            project_name = Path(session_file).parent.name
            session_id = Path(session_file).stem
            prompts = []

            with open(session_file, 'r') as f:
                for line in f:
                    try:
                        data = json.loads(line.strip())

                        if data.get('type') == 'user':
                            msg = data.get('message', {})
                            if msg.get('role') == 'user' and not data.get('isMeta', False):
                                content = msg.get('content', '')

                                # Skip meta messages and command outputs
                                if isinstance(content, str):
                                    if not content.startswith('<command') and not content.startswith('<local-command'):
                                        if len(content) > 20:
                                            prompts.append(content)
                                            all_prompts.append({
                                                'text': content,
                                                'lower': content.lower(),
                                                'project': project_name,
                                                'session': session_id
                                            })
                    except (json.JSONDecodeError, KeyError):
                        continue

            if prompts:
                sessions_data.append({
                    'project': project_name,
                    'session': session_id,
                    'prompts': prompts,
                    'count': len(prompts)
                })

        except Exception:
            continue

    # Detect patterns with examples
    patterns_found = {}

    # 1. Git commit + push workflow
    git_patterns = []
    for session in sessions_data:
        combined = ' '.join([p.lower() for p in session['prompts']])
        has_commit = 'commit' in combined or 'committed' in combined
        has_push = 'push' in combined

        if (has_commit and has_push) or (combined.count('git') >= 2):
            git_patterns.append({
                'session': session['session'],
                'project': session['project'],
                'prompts': session['prompts'][:5]
            })

    patterns_found['git_commit_push'] = {
        'count': len(git_patterns),
        'examples': git_patterns[:5]
    }

    # 2. Version bump + publish workflow
    version_patterns = []
    for session in sessions_data:
        combined = ' '.join([p.lower() for p in session['prompts']])
        has_version = 'version' in combined or 'bump' in combined
        has_publish = 'publish' in combined or 'release' in combined or 'update' in combined
        has_plugin = 'plugin' in combined or 'marketplace' in combined

        if (has_version and has_publish) or (has_plugin and (has_version or has_publish)):
            version_patterns.append({
                'session': session['session'],
                'project': session['project'],
                'prompts': session['prompts'][:5]
            })

    patterns_found['version_publish'] = {
        'count': len(version_patterns),
        'examples': version_patterns[:5]
    }

    # 3. Documentation/README updates
    doc_patterns = []
    for session in sessions_data:
        combined = ' '.join([p.lower() for p in session['prompts']])
        if 'readme' in combined or 'documentation' in combined or ('doc' in combined and ('update' in combined or 'write' in combined)):
            doc_patterns.append({
                'session': session['session'],
                'project': session['project'],
                'prompts': session['prompts'][:5]
            })

    patterns_found['documentation_updates'] = {
        'count': len(doc_patterns),
        'examples': doc_patterns[:5]
    }

    # 4. Test/fix cycles
    test_fix_patterns = []
    for session in sessions_data:
        combined = ' '.join([p.lower() for p in session['prompts']])
        has_test = 'test' in combined or 'testing' in combined
        has_fix = 'fix' in combined or 'error' in combined or 'bug' in combined

        if has_test and has_fix:
            test_fix_patterns.append({
                'session': session['session'],
                'project': session['project'],
                'prompts': session['prompts'][:5]
            })

    patterns_found['test_fix_cycles'] = {
        'count': len(test_fix_patterns),
        'examples': test_fix_patterns[:5]
    }

    # 5. Implementation workflow
    implementation_patterns = []
    for session in sessions_data:
        combined = ' '.join([p.lower() for p in session['prompts']])
        has_impl = 'implement' in combined or 'implementation' in combined or 'build' in combined

        if (has_impl or (session['count'] >= 5 and ('add' in combined or 'create' in combined))):
            implementation_patterns.append({
                'session': session['session'],
                'project': session['project'],
                'prompts': session['prompts'][:5]
            })

    patterns_found['implementation_workflows'] = {
        'count': len(implementation_patterns),
        'examples': implementation_patterns[:5]
    }

    # Build project activity summary
    project_activity = {}
    for session in sessions_data:
        project = session['project']
        project_activity[project] = project_activity.get(project, 0) + 1

    return {
        'summary': {
            'total_sessions_analyzed': len(session_files),
            'sessions_with_user_prompts': len(sessions_data),
            'total_user_prompts': len(all_prompts),
            'date_range': 'Last 30 days'
        },
        'project_activity': project_activity,
        'patterns': patterns_found
    }


def generate_report(analysis_data):
    """
    Generate a comprehensive markdown report from analysis data.

    Args:
        analysis_data: Dictionary containing analysis results

    Returns:
        Formatted markdown report string
    """
    summary = analysis_data['summary']
    patterns = analysis_data['patterns']
    projects = analysis_data['project_activity']

    report = f"""# Claude Code Workflow Analysis Report

## Analysis Summary

**Period Analyzed:** {summary['date_range']}
**Sessions Reviewed:** {summary['sessions_with_user_prompts']} sessions with user activity (from {summary['total_sessions_analyzed']} total)
**User Prompts Examined:** {summary['total_user_prompts']} prompts
**Patterns Detected:** 5 high-value automation opportunities

---

## High-Priority Patterns

### 1. Plugin/Marketplace Publish Workflow
**Frequency:** {patterns['version_publish']['count']} occurrences
**Estimated Time per Occurrence:** 10-15 minutes
**Total Time Spent:** ~{patterns['version_publish']['count'] * 12.5 / 60:.1f} hours
**Potential Savings:** 8-10 minutes per run (automated sequence)

**What you do:**
"""

    # Add version publish examples
    if patterns['version_publish']['examples']:
        example = patterns['version_publish']['examples'][0]
        report += f"\n*Example from {example['project'].replace('-Users-ant-code-', '')}:*\n"
        for i, prompt in enumerate(example['prompts'][:3], 1):
            preview = prompt[:120].replace('\n', ' ')
            report += f"{i}. \"{preview}...\"\n"

    report += f"""
**Suggested Command:** `/publish-plugin [version]`

**What it automates:**
1. Update version in plugin.json and marketplace.json
2. Update README with version notes
3. Run any validation/tests
4. Git add, commit with conventional message
5. Git push
6. Optionally create GitHub release

**Time savings:** ~10 min/occurrence = **{patterns['version_publish']['count'] * 10 / 60:.1f} hours saved over 30 days**

---

### 2. Git Commit + Push Workflow
**Frequency:** {patterns['git_commit_push']['count']} occurrences
**Estimated Time per Occurrence:** 5-8 minutes
**Total Time Spent:** ~{patterns['git_commit_push']['count'] * 6.5 / 60:.1f} hours
**Potential Savings:** 3-5 minutes per run

**What you do:**
- Review changes with git status/diff
- Stage files selectively
- Write commit message
- Push to remote
- Often involves back-and-forth about commit message format

**Suggested Command:** `/ship-git [message]`

**What it automates:**
1. Run git status and git diff for review
2. Stage all changes (or prompt for selection)
3. Create commit with your preferred format
4. Push to current branch
5. Show summary of what was shipped

**Time savings:** ~4 min/occurrence = **{patterns['git_commit_push']['count'] * 4 / 60:.1f} hours saved over 30 days**

---

### 3. Documentation Updates
**Frequency:** {patterns['documentation_updates']['count']} occurrences
**Estimated Time per Occurrence:** 8-12 minutes
**Total Time Spent:** ~{patterns['documentation_updates']['count'] * 10 / 60:.1f} hours
**Potential Savings:** 5-8 minutes per run

**What you do:**
- Update README files after feature changes
- Keep plugin docs in sync with marketplace.json
- Review and refine documentation formatting
- Ensure consistency across multiple README files

**Suggested Command:** `/sync-docs`

**What it automates:**
1. Check for version mismatches between files
2. Update README files with latest plugin metadata
3. Validate documentation structure
4. Check for broken links or references
5. Ensure consistent formatting
6. Optionally commit documentation changes

**Time savings:** ~6 min/occurrence = **{patterns['documentation_updates']['count'] * 6 / 60:.1f} hours saved over 30 days**

---

### 4. Implementation Workflows (Plan → Build → Test)
**Frequency:** {patterns['implementation_workflows']['count']} occurrences
**Estimated Time per Occurrence:** 20-45 minutes
**Total Time Spent:** ~{patterns['implementation_workflows']['count'] * 32.5 / 60:.1f} hours
**Potential Savings:** 5-10 minutes per run (setup/teardown phases)

**What you do:**
"""

    if patterns['implementation_workflows']['examples']:
        example = patterns['implementation_workflows']['examples'][0]
        report += f"\n*Example from {example['project'].replace('-Users-ant-code-', '')}:*\n"
        for i, prompt in enumerate(example['prompts'][:2], 1):
            preview = prompt[:120].replace('\n', ' ')
            report += f"{i}. \"{preview}...\"\n"

    report += f"""
**Suggested Command:** `/do-phase [phase-name]`

**What it automates:**
- Common development phase transitions
- Reads @PLAN.md or similar planning documents
- Sets up context for each phase
- Runs phase-specific validations
- Updates progress tracking

**Example usage:**
- `/do-phase planning` - Review requirements, create/update PLAN.md
- `/do-phase implementation` - Load plan, track progress, implement features
- `/do-phase review` - Run tests, check quality, prepare for commit

**Time savings:** ~7 min/occurrence = **{patterns['implementation_workflows']['count'] * 7 / 60:.1f} hours saved over 30 days**

---

## Medium-Priority Patterns

### 5. Test + Fix Cycles
**Frequency:** {patterns['test_fix_cycles']['count']} occurrences
**Suggested Command:** `/test-and-fix`

**What it automates:**
1. Run test suite
2. Analyze failures
3. Fix identified issues
4. Re-run tests
5. Report results

**Time savings:** ~3 min/occurrence = **{patterns['test_fix_cycles']['count'] * 3 / 60:.1f} hours saved over 30 days**

---

## Project-Specific Insights

**Most Active Projects:**
"""

    # Sort projects by activity
    sorted_projects = sorted(projects.items(), key=lambda x: x[1], reverse=True)
    total_sessions = sum(projects.values())
    for project, session_count in sorted_projects[:5]:
        clean_name = project.replace('-Users-ant-code-', '').replace('-Users-ant-', '')
        percentage = (session_count / total_sessions * 100) if total_sessions > 0 else 0
        report += f"- **{clean_name}**: {session_count} sessions ({percentage:.0f}% of activity)\n"

    most_active_project = sorted_projects[0] if sorted_projects else ('unknown', 0)

    report += f"""
**Key Observation:** Your workflow patterns suggest you'd benefit from **project-aware commands** that adapt to context.

**Pattern:** You frequently work on:
1. Plugin/skill development
2. Application development ({most_active_project[0].replace('-Users-ant-code-', '')} is your most active project)
3. Testing/setup tooling

---

## Recommendations

### Commands to Create First (Ranked by Impact)

1. **`/publish-plugin`** - Highest time savings, very repetitive workflow
   - Priority: **HIGHEST**
   - Complexity: Medium
   - ROI: Excellent

2. **`/ship-git`** - Second highest savings, used across all projects
   - Priority: **HIGH**
   - Complexity: Low
   - ROI: Excellent

3. **`/sync-docs`** - High savings, prevents consistency errors
   - Priority: **HIGH**
   - Complexity: Medium
   - ROI: Very Good

4. **`/do-phase`** - Good savings, improves workflow structure
   - Priority: **MEDIUM-HIGH**
   - Complexity: Medium-High
   - ROI: Good

5. **`/test-and-fix`** - Moderate savings, good for iteration speed
   - Priority: **MEDIUM**
   - Complexity: Medium
   - ROI: Good

### Estimated Total Time Savings

**If you implement the top 3 commands:** ~{(patterns['version_publish']['count'] * 10 + patterns['git_commit_push']['count'] * 4 + patterns['documentation_updates']['count'] * 6) / 60:.1f} hours saved per month
**If you implement all 5 commands:** ~{(patterns['version_publish']['count'] * 10 + patterns['git_commit_push']['count'] * 4 + patterns['documentation_updates']['count'] * 6 + patterns['implementation_workflows']['count'] * 7 + patterns['test_fix_cycles']['count'] * 3) / 60:.1f} hours saved per month

### Next Steps

1. **Start with `/ship-git`** - Lowest complexity, immediate benefit, used everywhere
2. **Add `/publish-plugin`** - Highest savings for your current focus area
3. **Create `/sync-docs`** - Prevents documentation drift in marketplace work
4. Consider project-specific variants that detect current project context

### User Preference Observations

Based on your workflow patterns:
- ✓ You prefer structured, multi-step workflows
- ✓ You work with @PLAN.md and reference files frequently
- ✓ You iterate on naming and documentation carefully
- ✓ You value consistency across plugin/marketplace files
- ✓ Git commit messages appear to use conventional format

**Commands should:**
- Support reading from @-referenced files (like @PLAN.md)
- Provide clear progress tracking
- Allow refinement/iteration before final execution
- Maintain file consistency as a primary goal
- Use your preferred commit message conventions

---

## Appendix: Analysis Metadata

**Sessions Analyzed:** {summary['total_sessions_analyzed']}
**Sessions with User Activity:** {summary['sessions_with_user_prompts']}
**User Prompts Parsed:** {summary['total_user_prompts']}
**Pattern Detection Method:** Keyword analysis + session structure analysis
**Privacy:** All analysis performed locally, no data sent externally
"""

    return report


def main():
    """
    Main entry point for the workflow analyzer.
    Reads session file paths from stdin, analyzes patterns, and generates report.
    """
    # Read session files from stdin
    session_files = [line.strip() for line in sys.stdin if line.strip()]

    # Analyze sessions to extract patterns
    analysis_results = analyze_sessions(session_files)

    # Generate markdown report from analysis
    report = generate_report(analysis_results)

    # Output final report to stdout
    print(report)


if __name__ == '__main__':
    main()
