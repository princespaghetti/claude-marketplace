#!/usr/bin/env python3
"""
Pytest tests for workflow_analyzer.py
Tests the parsing of Claude Code conversation logs and workflow pattern detection.
"""

import json
import pytest
import tempfile
from pathlib import Path
from workflow_analyzer import analyze_sessions, generate_report, main
import sys
from io import StringIO


# Test Fixtures

@pytest.fixture
def sample_user_message():
    """Create a sample user message in the JSONL format."""
    return {
        "type": "user",
        "message": {
            "role": "user",
            "content": "Please commit these changes and push to the repository"
        },
        "isSidechain": False,
        "userType": "external",
        "sessionId": "test-session-123",
        "uuid": "test-uuid-456"
    }


@pytest.fixture
def sample_assistant_message():
    """Create a sample assistant message."""
    return {
        "type": "assistant",
        "message": {
            "role": "assistant",
            "content": [{"type": "text", "text": "I'll help you commit and push the changes."}]
        },
        "sessionId": "test-session-123",
        "uuid": "test-uuid-789"
    }


@pytest.fixture
def sample_file_snapshot():
    """Create a sample file history snapshot entry."""
    return {
        "type": "file-history-snapshot",
        "messageId": "test-message-id",
        "snapshot": {
            "messageId": "test-message-id",
            "trackedFileBackups": {},
            "timestamp": "2025-11-15T15:08:49.297Z"
        },
        "isSnapshotUpdate": False
    }


@pytest.fixture
def sample_meta_message():
    """Create a sample meta message that should be filtered out."""
    return {
        "type": "user",
        "message": {
            "role": "user",
            "content": "<command-message>Running test command</command-message>"
        },
        "isMeta": True,
        "sessionId": "test-session-123"
    }


@pytest.fixture
def create_test_session_file():
    """Factory fixture to create temporary JSONL session files."""
    def _create_file(messages, project_name="test-project", session_id="session-001"):
        """
        Create a temporary JSONL file with the given messages.

        Args:
            messages: List of message dictionaries
            project_name: Name of the project directory
            session_id: Session ID for the file name

        Returns:
            Path to the created temporary file
        """
        # Create temp directory structure
        temp_dir = tempfile.mkdtemp()
        project_dir = Path(temp_dir) / project_name
        project_dir.mkdir(parents=True, exist_ok=True)

        # Create session file
        session_file = project_dir / f"{session_id}.jsonl"
        with open(session_file, 'w') as f:
            for msg in messages:
                f.write(json.dumps(msg) + '\n')

        return str(session_file)

    return _create_file


# Tests for analyze_sessions()

def test_analyze_sessions_empty_list():
    """Test analyze_sessions with an empty list of files."""
    result = analyze_sessions([])

    assert result['summary']['total_sessions_analyzed'] == 0
    assert result['summary']['sessions_with_user_prompts'] == 0
    assert result['summary']['total_user_prompts'] == 0
    assert len(result['project_activity']) == 0


def test_analyze_sessions_single_user_prompt(create_test_session_file, sample_user_message):
    """Test analyzing a session file with a single user prompt."""
    session_file = create_test_session_file([sample_user_message])
    result = analyze_sessions([session_file])

    assert result['summary']['total_sessions_analyzed'] == 1
    assert result['summary']['sessions_with_user_prompts'] == 1
    assert result['summary']['total_user_prompts'] == 1
    assert 'test-project' in result['project_activity']


def test_analyze_sessions_filters_meta_messages(create_test_session_file, sample_user_message, sample_meta_message):
    """Test that meta messages are properly filtered out."""
    session_file = create_test_session_file([sample_user_message, sample_meta_message])
    result = analyze_sessions([session_file])

    # Should only count the non-meta message
    assert result['summary']['total_user_prompts'] == 1


def test_analyze_sessions_filters_command_messages(create_test_session_file):
    """Test that command messages are filtered out."""
    command_msg = {
        "type": "user",
        "message": {
            "role": "user",
            "content": "<command>ls -la</command>"
        }
    }
    local_command_msg = {
        "type": "user",
        "message": {
            "role": "user",
            "content": "<local-command>git status</local-command>"
        }
    }

    session_file = create_test_session_file([command_msg, local_command_msg])
    result = analyze_sessions([session_file])

    # Command messages should be filtered out
    assert result['summary']['total_user_prompts'] == 0


def test_analyze_sessions_filters_short_messages(create_test_session_file):
    """Test that messages shorter than 20 characters are filtered out."""
    short_msg = {
        "type": "user",
        "message": {
            "role": "user",
            "content": "hi"
        }
    }

    session_file = create_test_session_file([short_msg])
    result = analyze_sessions([session_file])

    assert result['summary']['total_user_prompts'] == 0


def test_analyze_sessions_ignores_assistant_messages(create_test_session_file, sample_assistant_message):
    """Test that assistant messages are ignored."""
    session_file = create_test_session_file([sample_assistant_message])
    result = analyze_sessions([session_file])

    assert result['summary']['total_user_prompts'] == 0


def test_analyze_sessions_ignores_file_snapshots(create_test_session_file, sample_file_snapshot):
    """Test that file snapshots are ignored."""
    session_file = create_test_session_file([sample_file_snapshot])
    result = analyze_sessions([session_file])

    assert result['summary']['total_user_prompts'] == 0


def test_analyze_sessions_handles_malformed_json(create_test_session_file):
    """Test that malformed JSON lines are gracefully ignored."""
    # Create a file with malformed JSON
    temp_dir = tempfile.mkdtemp()
    project_dir = Path(temp_dir) / "test-project"
    project_dir.mkdir(parents=True, exist_ok=True)
    session_file = project_dir / "session-001.jsonl"

    with open(session_file, 'w') as f:
        f.write('{"type": "user", "message": {"role": "user", "content": "valid message here that is long enough"}}\n')
        f.write('{"invalid json malformed\n')
        f.write('{"type": "user", "message": {"role": "user", "content": "another valid message that is long enough"}}\n')

    result = analyze_sessions([str(session_file)])

    # Should process the valid lines and skip the malformed one
    assert result['summary']['total_user_prompts'] == 2


# Tests for pattern detection

def test_detect_git_commit_push_pattern(create_test_session_file):
    """Test detection of git commit and push workflow pattern."""
    messages = [
        {
            "type": "user",
            "message": {
                "role": "user",
                "content": "Please review the git status and commit the changes"
            }
        },
        {
            "type": "user",
            "message": {
                "role": "user",
                "content": "Now push these changes to the remote repository"
            }
        }
    ]

    session_file = create_test_session_file(messages)
    result = analyze_sessions([session_file])

    assert result['patterns']['git_commit_push']['count'] == 1
    assert len(result['patterns']['git_commit_push']['examples']) == 1


def test_detect_version_publish_pattern(create_test_session_file):
    """Test detection of version bump and publish workflow pattern."""
    messages = [
        {
            "type": "user",
            "message": {
                "role": "user",
                "content": "Update the plugin version to 1.2.3 in the marketplace.json file"
            }
        },
        {
            "type": "user",
            "message": {
                "role": "user",
                "content": "Now publish the updated plugin to the marketplace"
            }
        }
    ]

    session_file = create_test_session_file(messages)
    result = analyze_sessions([session_file])

    assert result['patterns']['version_publish']['count'] == 1


def test_detect_documentation_update_pattern(create_test_session_file):
    """Test detection of README/documentation update patterns."""
    messages = [
        {
            "type": "user",
            "message": {
                "role": "user",
                "content": "Please update the README file with the new installation instructions"
            }
        }
    ]

    session_file = create_test_session_file(messages)
    result = analyze_sessions([session_file])

    assert result['patterns']['documentation_updates']['count'] == 1


def test_detect_test_fix_cycle_pattern(create_test_session_file):
    """Test detection of test and fix cycle patterns."""
    messages = [
        {
            "type": "user",
            "message": {
                "role": "user",
                "content": "Run the test suite and check for any failures"
            }
        },
        {
            "type": "user",
            "message": {
                "role": "user",
                "content": "Fix the error in the test_workflow_analyzer function"
            }
        }
    ]

    session_file = create_test_session_file(messages)
    result = analyze_sessions([session_file])

    assert result['patterns']['test_fix_cycles']['count'] == 1


def test_detect_implementation_workflow_pattern(create_test_session_file):
    """Test detection of implementation workflow patterns."""
    messages = [
        {
            "type": "user",
            "message": {
                "role": "user",
                "content": "Implement a new feature for workflow pattern detection in the analyzer"
            }
        }
    ]

    session_file = create_test_session_file(messages)
    result = analyze_sessions([session_file])

    assert result['patterns']['implementation_workflows']['count'] == 1


def test_multiple_sessions_from_different_projects(create_test_session_file):
    """Test analyzing multiple sessions from different projects."""
    messages = [
        {
            "type": "user",
            "message": {
                "role": "user",
                "content": "This is a test message for the project analysis feature in the analyzer"
            }
        }
    ]

    session1 = create_test_session_file(messages, project_name="project-a", session_id="session-001")
    session2 = create_test_session_file(messages, project_name="project-b", session_id="session-002")
    session3 = create_test_session_file(messages, project_name="project-a", session_id="session-003")

    result = analyze_sessions([session1, session2, session3])

    assert result['summary']['total_sessions_analyzed'] == 3
    assert result['summary']['sessions_with_user_prompts'] == 3
    assert 'project-a' in result['project_activity']
    assert 'project-b' in result['project_activity']
    assert result['project_activity']['project-a'] == 2
    assert result['project_activity']['project-b'] == 1


def test_pattern_examples_limited_to_five(create_test_session_file):
    """Test that pattern examples are limited to 5 per pattern type."""
    messages = [
        {
            "type": "user",
            "message": {
                "role": "user",
                "content": "Commit and push the changes to the remote repository with git"
            }
        }
    ]

    # Create 10 sessions with the same pattern
    session_files = [
        create_test_session_file(messages, session_id=f"session-{i:03d}")
        for i in range(10)
    ]

    result = analyze_sessions(session_files)

    # Should detect 10 occurrences
    assert result['patterns']['git_commit_push']['count'] == 10
    # But only store 5 examples
    assert len(result['patterns']['git_commit_push']['examples']) == 5


def test_prompts_stored_with_metadata(create_test_session_file):
    """Test that prompts are stored with project and session metadata."""
    messages = [
        {
            "type": "user",
            "message": {
                "role": "user",
                "content": "This is a test message for metadata verification in the prompt storage"
            }
        }
    ]

    session_file = create_test_session_file(
        messages,
        project_name="metadata-test-project",
        session_id="metadata-session-001"
    )

    result = analyze_sessions([session_file])

    # Check that the session data contains the expected metadata
    assert result['summary']['sessions_with_user_prompts'] == 1
    assert 'metadata-test-project' in result['project_activity']


# Tests for generate_report()

def test_generate_report_basic_structure():
    """Test that generate_report produces a valid markdown report."""
    analysis_data = {
        'summary': {
            'total_sessions_analyzed': 10,
            'sessions_with_user_prompts': 8,
            'total_user_prompts': 50,
            'date_range': 'Last 30 days'
        },
        'project_activity': {
            'project-a': 5,
            'project-b': 3
        },
        'patterns': {
            'git_commit_push': {'count': 5, 'examples': []},
            'version_publish': {'count': 3, 'examples': []},
            'documentation_updates': {'count': 2, 'examples': []},
            'test_fix_cycles': {'count': 1, 'examples': []},
            'implementation_workflows': {'count': 4, 'examples': []}
        }
    }

    report = generate_report(analysis_data)

    # Check for key sections
    assert '# Claude Code Workflow Analysis Report' in report
    assert '## Analysis Summary' in report
    assert '## High-Priority Patterns' in report
    assert '## Project-Specific Insights' in report
    assert '## Recommendations' in report

    # Check that numbers are included
    assert '10' in report  # total sessions
    assert '50' in report  # total prompts


def test_generate_report_includes_examples(create_test_session_file):
    """Test that the report includes examples from detected patterns."""
    messages = [
        {
            "type": "user",
            "message": {
                "role": "user",
                "content": "Update version to 2.0.0 and publish the plugin to the marketplace"
            }
        }
    ]

    session_file = create_test_session_file(messages, project_name="example-project")
    analysis_data = analyze_sessions([session_file])
    report = generate_report(analysis_data)

    # Should include example text from the version publish pattern
    assert 'example-project' in report or 'Example from' in report


def test_generate_report_project_activity_sorted():
    """Test that project activity is sorted by frequency."""
    analysis_data = {
        'summary': {
            'total_sessions_analyzed': 15,
            'sessions_with_user_prompts': 15,
            'total_user_prompts': 100,
            'date_range': 'Last 30 days'
        },
        'project_activity': {
            'low-activity': 1,
            'high-activity': 10,
            'medium-activity': 4
        },
        'patterns': {
            'git_commit_push': {'count': 0, 'examples': []},
            'version_publish': {'count': 0, 'examples': []},
            'documentation_updates': {'count': 0, 'examples': []},
            'test_fix_cycles': {'count': 0, 'examples': []},
            'implementation_workflows': {'count': 0, 'examples': []}
        }
    }

    report = generate_report(analysis_data)

    # Find the project activity section
    lines = report.split('\n')
    project_section_start = None
    for i, line in enumerate(lines):
        if '**Most Active Projects:**' in line:
            project_section_start = i
            break

    assert project_section_start is not None

    # The first project listed should be 'high-activity'
    # Look for the next few lines after the header
    project_lines = lines[project_section_start+1:project_section_start+6]
    project_text = '\n'.join(project_lines)

    # high-activity should appear before medium-activity and low-activity
    high_pos = project_text.find('high-activity')
    medium_pos = project_text.find('medium-activity')

    assert high_pos != -1
    assert high_pos < medium_pos or medium_pos == -1


def test_generate_report_time_savings_calculations():
    """Test that time savings are calculated correctly in the report."""
    analysis_data = {
        'summary': {
            'total_sessions_analyzed': 10,
            'sessions_with_user_prompts': 10,
            'total_user_prompts': 50,
            'date_range': 'Last 30 days'
        },
        'project_activity': {},
        'patterns': {
            'git_commit_push': {'count': 10, 'examples': []},
            'version_publish': {'count': 5, 'examples': []},
            'documentation_updates': {'count': 3, 'examples': []},
            'test_fix_cycles': {'count': 2, 'examples': []},
            'implementation_workflows': {'count': 4, 'examples': []}
        }
    }

    report = generate_report(analysis_data)

    # Check that time savings are mentioned
    assert 'Time savings' in report or 'hours saved' in report

    # Verify calculations are present (git: 10*4=40min, version: 5*10=50min, docs: 3*6=18min)
    # Total for top 3: (40+50+18)/60 = 1.8 hours
    # The report should contain this calculation
    assert 'hours saved per month' in report


def test_generate_report_zero_patterns():
    """Test report generation when no patterns are detected."""
    analysis_data = {
        'summary': {
            'total_sessions_analyzed': 5,
            'sessions_with_user_prompts': 0,
            'total_user_prompts': 0,
            'date_range': 'Last 30 days'
        },
        'project_activity': {},
        'patterns': {
            'git_commit_push': {'count': 0, 'examples': []},
            'version_publish': {'count': 0, 'examples': []},
            'documentation_updates': {'count': 0, 'examples': []},
            'test_fix_cycles': {'count': 0, 'examples': []},
            'implementation_workflows': {'count': 0, 'examples': []}
        }
    }

    # Should not raise an exception
    report = generate_report(analysis_data)

    assert isinstance(report, str)
    assert len(report) > 0
    assert '# Claude Code Workflow Analysis Report' in report


# Tests for main() function

def test_main_function_with_stdin(create_test_session_file, monkeypatch, capsys):
    """Test the main() function with stdin input."""
    messages = [
        {
            "type": "user",
            "message": {
                "role": "user",
                "content": "This is a test message for the main function integration test"
            }
        }
    ]

    session_file = create_test_session_file(messages)

    # Mock stdin to provide the session file path
    mock_stdin = StringIO(f"{session_file}\n")
    monkeypatch.setattr('sys.stdin', mock_stdin)

    # Run main
    main()

    # Capture output
    captured = capsys.readouterr()

    # Verify report was generated
    assert '# Claude Code Workflow Analysis Report' in captured.out
    assert 'Analysis Summary' in captured.out


def test_main_function_empty_stdin(monkeypatch, capsys):
    """Test the main() function with empty stdin."""
    mock_stdin = StringIO("")
    monkeypatch.setattr('sys.stdin', mock_stdin)

    # Run main
    main()

    # Capture output
    captured = capsys.readouterr()

    # Should still generate a report, just with no data
    assert '# Claude Code Workflow Analysis Report' in captured.out


def test_main_function_multiple_files(create_test_session_file, monkeypatch, capsys):
    """Test the main() function with multiple session files."""
    messages = [
        {
            "type": "user",
            "message": {
                "role": "user",
                "content": "Test message for multi-file integration test in main function"
            }
        }
    ]

    session1 = create_test_session_file(messages, session_id="session-001")
    session2 = create_test_session_file(messages, session_id="session-002")

    # Mock stdin with multiple file paths
    mock_stdin = StringIO(f"{session1}\n{session2}\n")
    monkeypatch.setattr('sys.stdin', mock_stdin)

    # Run main
    main()

    # Capture output
    captured = capsys.readouterr()

    # Should process both files
    assert '# Claude Code Workflow Analysis Report' in captured.out
    # Should indicate 2 sessions were analyzed
    assert '2' in captured.out


# Edge cases and error handling

def test_nonexistent_file_handling():
    """Test that nonexistent files are handled gracefully."""
    result = analyze_sessions(['/nonexistent/path/to/file.jsonl'])

    # Should not crash, just return empty results
    assert result['summary']['total_sessions_analyzed'] == 1
    assert result['summary']['sessions_with_user_prompts'] == 0


def test_empty_file_handling(create_test_session_file):
    """Test handling of empty session files."""
    session_file = create_test_session_file([])
    result = analyze_sessions([session_file])

    assert result['summary']['total_sessions_analyzed'] == 1
    assert result['summary']['sessions_with_user_prompts'] == 0
    assert result['summary']['total_user_prompts'] == 0


def test_unicode_content_handling(create_test_session_file):
    """Test handling of Unicode characters in message content."""
    messages = [
        {
            "type": "user",
            "message": {
                "role": "user",
                "content": "Test with Unicode: 你好世界 🚀 émojis and spëcial çharacters"
            }
        }
    ]

    session_file = create_test_session_file(messages)
    result = analyze_sessions([session_file])

    assert result['summary']['total_user_prompts'] == 1


def test_very_long_message_handling(create_test_session_file):
    """Test handling of very long messages."""
    long_content = "x" * 10000 + " this is a very long message " + "y" * 10000
    messages = [
        {
            "type": "user",
            "message": {
                "role": "user",
                "content": long_content
            }
        }
    ]

    session_file = create_test_session_file(messages)
    result = analyze_sessions([session_file])

    assert result['summary']['total_user_prompts'] == 1


def test_message_content_as_list(create_test_session_file):
    """Test handling when message content is a list instead of string."""
    messages = [
        {
            "type": "user",
            "message": {
                "role": "user",
                "content": [
                    {"type": "text", "text": "This is content as a list structure"}
                ]
            }
        }
    ]

    session_file = create_test_session_file(messages)
    result = analyze_sessions([session_file])

    # Should be skipped since it's not a string
    assert result['summary']['total_user_prompts'] == 0


def test_missing_message_fields(create_test_session_file):
    """Test handling of messages with missing required fields."""
    messages = [
        {
            "type": "user",
            # Missing 'message' field
        },
        {
            "type": "user",
            "message": {
                # Missing 'role' field
                "content": "This message is missing the role field"
            }
        },
        {
            "type": "user",
            "message": {
                "role": "user"
                # Missing 'content' field
            }
        }
    ]

    session_file = create_test_session_file(messages)
    result = analyze_sessions([session_file])

    # All should be skipped due to missing fields
    assert result['summary']['total_user_prompts'] == 0
