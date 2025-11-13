---
description: Analyzes your zsh or bash command history to identify usage patterns, productivity improvements, automation opportunities, and skill development areas based on your actual shell workflows.
---

This command provides personalized insights into your command-line habits by analyzing your zsh history to reveal patterns, inefficiencies, and opportunities for improvement.


## Instructions

Read `~/.zsh_history` or `~/.bash_history` and analyze command patterns to generate a concise, actionable report.

### Analysis Focus

**Command Patterns**:
- Identify top 10-15 most frequent commands
- Categorize by purpose (version control, package management, file ops, development tools, etc.)
- Find repeated command sequences that could be automated

**Productivity Opportunities**:
- Long/repetitive commands suitable for aliasing (prioritize by frequency × length)
- Command chains executed together frequently
- Excessive directory navigation patterns

**Deliverables**:
- 3-4 high-impact improvement opportunities with Impact/Effort ratings
- Ready-to-use aliases and shell functions (copy-pasteable)
- 2-3 quick wins (< 5 min to implement)
- Brief skill development suggestions

### Report Structure

Keep the report focused and scannable:
1. **Summary**: Brief overview of command patterns and workflow (2-3 sentences)
2. **Top Commands**: List 10-15 most frequent with counts
3. **Improvement Opportunities**: 3-4 specific recommendations with before/after examples
4. **Suggested Aliases & Functions**: Copy-pasteable code block for ~/.zshrc
5. **Quick Wins**: 2-3 one-liner improvements

**Guidelines**:
- Be concise but specific - use actual counts from history
- Prioritize by impact (frequency × time saved)
- Provide working code, not templates
- Keep encouraging tone, highlight existing strengths
