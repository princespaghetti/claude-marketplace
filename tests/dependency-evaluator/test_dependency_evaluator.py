#!/usr/bin/env python3
"""
Pytest tests for dependency_evaluator.py
Tests package evaluation across ecosystems with mocked external dependencies.
"""

import json
import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from io import BytesIO
import subprocess
import urllib.error

# Add the dependency evaluator script directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'learnfrompast' / 'skills' / 'dependency-evaluator' / 'scripts'))
from dependency_evaluator import DependencyEvaluator, main


# Test Fixtures

@pytest.fixture
def npm_evaluator():
    """Create a DependencyEvaluator instance for npm ecosystem."""
    return DependencyEvaluator('lodash', 'npm')


@pytest.fixture
def pypi_evaluator():
    """Create a DependencyEvaluator instance for PyPI ecosystem."""
    return DependencyEvaluator('requests', 'pypi')


@pytest.fixture
def cargo_evaluator():
    """Create a DependencyEvaluator instance for Cargo ecosystem."""
    return DependencyEvaluator('serde', 'cargo')


@pytest.fixture
def go_evaluator():
    """Create a DependencyEvaluator instance for Go ecosystem."""
    return DependencyEvaluator('github.com/gorilla/mux', 'go')


@pytest.fixture
def mock_npm_view_output():
    """Sample npm view JSON output."""
    return json.dumps({
        "version": "4.17.21",
        "license": "MIT",
        "description": "Lodash modular utilities",
        "homepage": "https://lodash.com/",
        "repository": {
            "type": "git",
            "url": "git+https://github.com/lodash/lodash.git"
        },
        "maintainers": [
            {"name": "jdalton", "email": "john.david.dalton@gmail.com"}
        ],
        "keywords": ["modules", "stdlib", "util"]
    })


@pytest.fixture
def mock_npm_time_output():
    """Sample npm time JSON output."""
    return json.dumps({
        "created": "2012-04-23T18:00:00.000Z",
        "modified": "2024-01-15T10:00:00.000Z",
        "4.17.21": "2021-02-20T15:49:28.936Z",
        "4.17.20": "2020-02-18T21:23:38.996Z"
    })


@pytest.fixture
def mock_npm_versions_output():
    """Sample npm versions JSON output."""
    return json.dumps(["4.17.20", "4.17.21"])


@pytest.fixture
def mock_pypi_api_response():
    """Sample PyPI API JSON response."""
    return {
        "info": {
            "version": "2.31.0",
            "license": "Apache 2.0",
            "summary": "Python HTTP library",
            "home_page": "https://requests.readthedocs.io",
            "project_urls": {
                "Source": "https://github.com/psf/requests"
            },
            "author": "Kenneth Reitz",
            "keywords": "http,requests,api"
        },
        "releases": {
            "2.31.0": [{"upload_time": "2023-05-22T14:30:00"}],
            "2.30.0": [{"upload_time": "2023-05-01T10:00:00"}]
        }
    }


@pytest.fixture
def mock_cargo_api_response():
    """Sample crates.io API JSON response."""
    return {
        "crate": {
            "max_version": "1.0.195",
            "license": "MIT OR Apache-2.0",
            "description": "A serialization framework",
            "homepage": "https://serde.rs",
            "repository": "https://github.com/serde-rs/serde",
            "downloads": 500000000,
            "recent_downloads": 25000000
        }
    }


@pytest.fixture
def mock_cargo_versions_response():
    """Sample crates.io versions API response."""
    return {
        "versions": [
            {"num": "1.0.195"},
            {"num": "1.0.194"},
            {"num": "1.0.193"}
        ]
    }


@pytest.fixture
def mock_github_api_response():
    """Sample GitHub API response."""
    return {
        "pushed_at": "2024-12-15T10:30:00Z",
        "open_issues_count": 42,
        "stargazers_count": 58000,
        "forks_count": 12000,
        "watchers_count": 58000,
        "default_branch": "main"
    }


@pytest.fixture
def mock_github_community_response():
    """Sample GitHub community health API response."""
    return {
        "health_percentage": 85,
        "files": {
            "readme": {"url": "https://github.com/..."},
            "contributing": {"url": "https://github.com/..."},
            "license": {"url": "https://github.com/..."}
        }
    }


# Tests for DependencyEvaluator initialization

def test_evaluator_initialization():
    """Test basic initialization of DependencyEvaluator."""
    evaluator = DependencyEvaluator('test-package', 'npm')
    assert evaluator.package_name == 'test-package'
    assert evaluator.ecosystem == 'npm'
    assert evaluator.errors == []
    assert evaluator.warnings == []


def test_evaluator_ecosystem_lowercase():
    """Test that ecosystem is converted to lowercase."""
    evaluator = DependencyEvaluator('test-package', 'NPM')
    assert evaluator.ecosystem == 'npm'


# Tests for run_command()

def test_run_command_success():
    """Test successful command execution."""
    evaluator = DependencyEvaluator('test', 'npm')

    with patch('subprocess.run') as mock_run:
        mock_run.return_value = Mock(returncode=0, stdout='test output', stderr='')
        success, stdout, stderr = evaluator.run_command(['echo', 'test'])

        assert success is True
        assert stdout == 'test output'
        assert stderr == ''


def test_run_command_failure():
    """Test failed command execution."""
    evaluator = DependencyEvaluator('test', 'npm')

    with patch('subprocess.run') as mock_run:
        mock_run.return_value = Mock(returncode=1, stdout='', stderr='error message')
        success, stdout, stderr = evaluator.run_command(['false'])

        assert success is False
        assert stderr == 'error message'


def test_run_command_not_found():
    """Test command not found error."""
    evaluator = DependencyEvaluator('test', 'npm')

    with patch('subprocess.run', side_effect=FileNotFoundError()):
        success, stdout, stderr = evaluator.run_command(['nonexistent-command'])

        assert success is False
        assert len(evaluator.warnings) == 1
        assert 'Command not found' in evaluator.warnings[0]


def test_run_command_timeout():
    """Test command timeout handling."""
    evaluator = DependencyEvaluator('test', 'npm')

    with patch('subprocess.run', side_effect=subprocess.TimeoutExpired('cmd', 30)):
        success, stdout, stderr = evaluator.run_command(['sleep', '100'], timeout=30)

        assert success is False
        assert len(evaluator.warnings) == 1
        assert 'timed out' in evaluator.warnings[0]


def test_run_command_exception():
    """Test generic exception handling in run_command."""
    evaluator = DependencyEvaluator('test', 'npm')

    with patch('subprocess.run', side_effect=Exception('Unknown error')):
        success, stdout, stderr = evaluator.run_command(['test'])

        assert success is False
        assert len(evaluator.warnings) == 1
        assert 'Command failed' in evaluator.warnings[0]


# Tests for fetch_url()

def test_fetch_url_success(pypi_evaluator, mock_pypi_api_response):
    """Test successful URL fetch."""
    mock_response = BytesIO(json.dumps(mock_pypi_api_response).encode('utf-8'))

    with patch('urllib.request.urlopen', return_value=mock_response):
        result = pypi_evaluator.fetch_url('https://pypi.org/pypi/requests/json')

        assert result is not None
        assert result['info']['version'] == '2.31.0'


def test_fetch_url_404():
    """Test 404 error handling."""
    evaluator = DependencyEvaluator('nonexistent', 'npm')

    with patch('urllib.request.urlopen', side_effect=urllib.error.HTTPError('url', 404, 'Not Found', {}, None)):
        result = evaluator.fetch_url('https://example.com/notfound')

        assert result is None
        assert len(evaluator.errors) == 1
        assert 'not found' in evaluator.errors[0].lower()


def test_fetch_url_403_rate_limit():
    """Test 403 rate limit error handling."""
    evaluator = DependencyEvaluator('test', 'npm')

    with patch('urllib.request.urlopen', side_effect=urllib.error.HTTPError('url', 403, 'Forbidden', {}, None)):
        result = evaluator.fetch_url('https://api.github.com/repos/test/test')

        assert result is None
        assert len(evaluator.warnings) == 1
        assert 'rate limit' in evaluator.warnings[0].lower() or 'forbidden' in evaluator.warnings[0].lower()


def test_fetch_url_network_error():
    """Test network error handling."""
    evaluator = DependencyEvaluator('test', 'npm')

    with patch('urllib.request.urlopen', side_effect=urllib.error.URLError('Network error')):
        result = evaluator.fetch_url('https://example.com')

        assert result is None
        assert len(evaluator.warnings) == 1
        assert 'Network error' in evaluator.warnings[0]


def test_fetch_url_invalid_json():
    """Test invalid JSON response handling."""
    evaluator = DependencyEvaluator('test', 'npm')
    mock_response = BytesIO(b'not valid json')

    with patch('urllib.request.urlopen', return_value=mock_response):
        result = evaluator.fetch_url('https://example.com')

        assert result is None
        assert len(evaluator.warnings) == 1
        assert 'Invalid JSON' in evaluator.warnings[0]


# Tests for npm data gathering

def test_gather_npm_data_success(npm_evaluator, mock_npm_view_output, mock_npm_time_output, mock_npm_versions_output):
    """Test successful npm data gathering."""
    with patch.object(npm_evaluator, 'run_command') as mock_cmd:
        mock_cmd.side_effect = [
            (True, mock_npm_view_output, ''),
            (True, mock_npm_time_output, ''),
            (True, mock_npm_versions_output, '')
        ]

        data = npm_evaluator.gather_npm_data()

        assert data['latest_version'] == '4.17.21'
        assert data['license'] == 'MIT'
        assert data['description'] == 'Lodash modular utilities'
        assert 'github.com/lodash/lodash' in data['repository_url']
        assert data['versions_count'] == 2
        assert '4.17.21' in data['all_versions']


def test_gather_npm_data_command_failure(npm_evaluator):
    """Test npm data gathering with command failures."""
    with patch.object(npm_evaluator, 'run_command', return_value=(False, '', 'error')):
        data = npm_evaluator.gather_npm_data()

        assert data == {}


def test_gather_npm_data_invalid_json(npm_evaluator):
    """Test npm data gathering with invalid JSON."""
    with patch.object(npm_evaluator, 'run_command', return_value=(True, 'not json', '')):
        data = npm_evaluator.gather_npm_data()

        assert len(npm_evaluator.warnings) > 0
        assert 'Failed to parse' in npm_evaluator.warnings[0]


# Tests for PyPI data gathering

def test_gather_pypi_data_success(pypi_evaluator, mock_pypi_api_response):
    """Test successful PyPI data gathering."""
    with patch.object(pypi_evaluator, 'fetch_url', return_value=mock_pypi_api_response):
        data = pypi_evaluator.gather_pypi_data()

        assert data['latest_version'] == '2.31.0'
        assert data['license'] == 'Apache 2.0'
        assert data['description'] == 'Python HTTP library'
        assert 'github.com/psf/requests' in data['repository_url']
        assert data['versions_count'] == 2


def test_gather_pypi_data_api_failure(pypi_evaluator):
    """Test PyPI data gathering with API failure."""
    with patch.object(pypi_evaluator, 'fetch_url', return_value=None):
        data = pypi_evaluator.gather_pypi_data()

        assert data == {}


def test_gather_pypi_data_missing_fields(pypi_evaluator):
    """Test PyPI data gathering with missing fields."""
    incomplete_response = {"info": {}}

    with patch.object(pypi_evaluator, 'fetch_url', return_value=incomplete_response):
        data = pypi_evaluator.gather_pypi_data()

        assert data['latest_version'] == ''
        assert data['license'] == ''


# Tests for Cargo data gathering

def test_gather_cargo_data_success(cargo_evaluator, mock_cargo_api_response, mock_cargo_versions_response):
    """Test successful Cargo data gathering."""
    def mock_fetch(url):
        if 'versions' in url:
            return mock_cargo_versions_response
        return mock_cargo_api_response

    with patch.object(cargo_evaluator, 'fetch_url', side_effect=mock_fetch):
        data = cargo_evaluator.gather_cargo_data()

        assert data['latest_version'] == '1.0.195'
        assert 'MIT' in data['license'] or 'Apache' in data['license']
        assert data['description'] == 'A serialization framework'
        assert 'github.com/serde-rs/serde' in data['repository_url']
        assert data['versions_count'] == 3


def test_gather_cargo_data_api_failure(cargo_evaluator):
    """Test Cargo data gathering with API failure."""
    with patch.object(cargo_evaluator, 'fetch_url', return_value=None):
        data = cargo_evaluator.gather_cargo_data()

        assert data == {}


# Tests for Go data gathering

def test_gather_go_data_success(go_evaluator):
    """Test successful Go data gathering."""
    go_output = json.dumps({
        "Path": "github.com/gorilla/mux",
        "Version": "v1.8.1",
        "Time": "2023-12-01T10:00:00Z"
    })

    with patch.object(go_evaluator, 'run_command', return_value=(True, go_output, '')):
        data = go_evaluator.gather_go_data()

        assert data['module_path'] == 'github.com/gorilla/mux'
        assert data['latest_version'] == 'v1.8.1'


def test_gather_go_data_command_failure(go_evaluator):
    """Test Go data gathering with command failure."""
    with patch.object(go_evaluator, 'run_command', return_value=(False, '', 'error')):
        data = go_evaluator.gather_go_data()

        assert data == {}


# Tests for GitHub URL extraction

def test_extract_github_repo_https():
    """Test GitHub URL extraction from HTTPS URL."""
    evaluator = DependencyEvaluator('test', 'npm')
    result = evaluator.extract_github_repo('https://github.com/lodash/lodash')

    assert result == ('lodash', 'lodash')


def test_extract_github_repo_git():
    """Test GitHub URL extraction from git URL."""
    evaluator = DependencyEvaluator('test', 'npm')
    result = evaluator.extract_github_repo('git+https://github.com/lodash/lodash.git')

    assert result == ('lodash', 'lodash')


def test_extract_github_repo_ssh():
    """Test GitHub URL extraction from SSH URL."""
    evaluator = DependencyEvaluator('test', 'npm')
    result = evaluator.extract_github_repo('git@github.com:lodash/lodash.git')

    assert result == ('lodash', 'lodash')


def test_extract_github_repo_invalid():
    """Test GitHub URL extraction with invalid URL."""
    evaluator = DependencyEvaluator('test', 'npm')
    result = evaluator.extract_github_repo('https://example.com/not/github')

    assert result is None


def test_extract_github_repo_empty():
    """Test GitHub URL extraction with empty string."""
    evaluator = DependencyEvaluator('test', 'npm')
    result = evaluator.extract_github_repo('')

    assert result is None


# Tests for GitHub data gathering

def test_gather_github_data_with_gh_cli(npm_evaluator, mock_github_api_response, mock_github_community_response):
    """Test GitHub data gathering using gh CLI."""
    def mock_run_cmd(cmd):
        if 'community/profile' in ' '.join(cmd):
            return (True, json.dumps(mock_github_community_response), '')
        elif 'contributors' in ' '.join(cmd):
            return (True, '50', '')
        elif 'license' in ' '.join(cmd):
            return (True, 'MIT', '')
        else:
            return (True, json.dumps(mock_github_api_response), '')

    with patch.object(npm_evaluator, 'run_command', side_effect=mock_run_cmd):
        data = npm_evaluator.gather_github_data('https://github.com/lodash/lodash')

        assert data['repository_url'] == 'https://github.com/lodash/lodash'
        assert data['stargazers_count'] == 58000
        assert data['open_issues_count'] == 42
        assert data['contributors_count'] == 50
        assert data['community_health']['health_percentage'] == 85


def test_gather_github_data_fallback_to_api(npm_evaluator, mock_github_api_response):
    """Test GitHub data gathering fallback to direct API."""
    with patch.object(npm_evaluator, 'run_command', return_value=(False, '', 'gh not found')):
        with patch.object(npm_evaluator, 'fetch_url', return_value=mock_github_api_response):
            data = npm_evaluator.gather_github_data('https://github.com/lodash/lodash')

            assert data['stargazers_count'] == 58000
            assert data['open_issues_count'] == 42


def test_gather_github_data_invalid_url(npm_evaluator):
    """Test GitHub data gathering with invalid URL."""
    data = npm_evaluator.gather_github_data('https://example.com/invalid')

    assert len(npm_evaluator.warnings) > 0
    assert 'Could not parse' in npm_evaluator.warnings[0]


# Tests for full evaluation

def test_evaluate_npm_package(npm_evaluator):
    """Test full evaluation of an npm package."""
    with patch.object(npm_evaluator, 'gather_npm_data', return_value={'latest_version': '4.17.21', 'repository_url': 'https://github.com/lodash/lodash'}):
        with patch.object(npm_evaluator, 'gather_github_data', return_value={'stargazers_count': 58000}):
            with patch.object(npm_evaluator, 'gather_security_data', return_value={}):
                with patch.object(npm_evaluator, 'gather_dependency_footprint', return_value={}):
                    result = npm_evaluator.evaluate()

                    assert result['package'] == 'lodash'
                    assert result['ecosystem'] == 'npm'
                    assert 'timestamp' in result
                    assert result['registry_data']['latest_version'] == '4.17.21'
                    assert result['github_data']['stargazers_count'] == 58000


def test_evaluate_pypi_package(pypi_evaluator):
    """Test full evaluation of a PyPI package."""
    with patch.object(pypi_evaluator, 'gather_pypi_data', return_value={'latest_version': '2.31.0'}):
        with patch.object(pypi_evaluator, 'gather_security_data', return_value={}):
            with patch.object(pypi_evaluator, 'gather_dependency_footprint', return_value={}):
                result = pypi_evaluator.evaluate()

                assert result['package'] == 'requests'
                assert result['ecosystem'] == 'pypi'
                assert result['registry_data']['latest_version'] == '2.31.0'


def test_evaluate_unsupported_ecosystem():
    """Test evaluation with unsupported ecosystem."""
    evaluator = DependencyEvaluator('test', 'unsupported')
    result = evaluator.evaluate()

    assert len(result['errors']) > 0
    assert 'Unsupported ecosystem' in result['errors'][0]


def test_evaluate_with_errors(npm_evaluator):
    """Test evaluation that encounters errors."""
    with patch.object(npm_evaluator, 'gather_npm_data', return_value={}):
        npm_evaluator.errors.append('Test error')
        with patch.object(npm_evaluator, 'gather_security_data', return_value={}):
            with patch.object(npm_evaluator, 'gather_dependency_footprint', return_value={}):
                result = npm_evaluator.evaluate()

                assert len(result['errors']) > 0
                assert 'Test error' in result['errors']


def test_evaluate_with_warnings(npm_evaluator):
    """Test evaluation that encounters warnings."""
    with patch.object(npm_evaluator, 'gather_npm_data', return_value={}):
        npm_evaluator.warnings.append('Test warning')
        with patch.object(npm_evaluator, 'gather_security_data', return_value={}):
            with patch.object(npm_evaluator, 'gather_dependency_footprint', return_value={}):
                result = npm_evaluator.evaluate()

                assert len(result['warnings']) > 0
                assert 'Test warning' in result['warnings']


# Tests for main() CLI function

def test_main_with_npm_package(capsys):
    """Test main() function with npm package."""
    test_args = ['dependency_evaluator.py', 'lodash', 'npm']

    with patch('sys.argv', test_args):
        with patch.object(DependencyEvaluator, 'evaluate', return_value={
            'package': 'lodash',
            'ecosystem': 'npm',
            'errors': [],
            'warnings': []
        }):
            with pytest.raises(SystemExit) as exc_info:
                main()

            # Should exit with 0 (no errors)
            assert exc_info.value.code is None or exc_info.value.code == 0

            captured = capsys.readouterr()
            output = json.loads(captured.out)
            assert output['package'] == 'lodash'


def test_main_with_errors(capsys):
    """Test main() function with errors."""
    test_args = ['dependency_evaluator.py', 'test', 'npm']

    with patch('sys.argv', test_args):
        with patch.object(DependencyEvaluator, 'evaluate', return_value={
            'package': 'test',
            'ecosystem': 'npm',
            'errors': ['Package not found'],
            'warnings': []
        }):
            with pytest.raises(SystemExit) as exc_info:
                main()

            # Should exit with 1 (errors present)
            assert exc_info.value.code == 1


def test_main_invalid_ecosystem():
    """Test main() with invalid ecosystem argument."""
    test_args = ['dependency_evaluator.py', 'test', 'invalid']

    with patch('sys.argv', test_args):
        with pytest.raises(SystemExit):
            main()


# Edge cases

def test_unicode_package_name():
    """Test handling of Unicode characters in package name."""
    evaluator = DependencyEvaluator('test-包', 'npm')
    assert evaluator.package_name == 'test-包'


def test_empty_registry_data(npm_evaluator):
    """Test handling of empty registry data."""
    with patch.object(npm_evaluator, 'run_command', return_value=(True, '', '')):
        data = npm_evaluator.gather_npm_data()

        # Should not crash, just return empty data
        assert isinstance(data, dict)


def test_github_data_without_repo_url(npm_evaluator):
    """Test evaluation when no repository URL is found."""
    with patch.object(npm_evaluator, 'gather_npm_data', return_value={}):
        with patch.object(npm_evaluator, 'gather_security_data', return_value={}):
            with patch.object(npm_evaluator, 'gather_dependency_footprint', return_value={}):
                result = npm_evaluator.evaluate()

                assert result['github_data'] == {}


def test_security_data_npm_warning(npm_evaluator):
    """Test that npm audit shows appropriate warning."""
    data = npm_evaluator.gather_security_data()

    assert len(npm_evaluator.warnings) > 0
    assert 'npm audit' in npm_evaluator.warnings[0]


def test_dependency_footprint_npm_warning(npm_evaluator):
    """Test that dependency footprint shows appropriate warning."""
    data = npm_evaluator.gather_dependency_footprint()

    assert len(npm_evaluator.warnings) > 0
    assert 'npm ls' in npm_evaluator.warnings[0]


def test_npm_repository_as_string(npm_evaluator):
    """Test handling npm repository field as string instead of object."""
    npm_output = json.dumps({
        "version": "1.0.0",
        "repository": "https://github.com/test/test"
    })

    with patch.object(npm_evaluator, 'run_command', return_value=(True, npm_output, '')):
        data = npm_evaluator.gather_npm_data()

        assert data['repository_url'] == 'https://github.com/test/test'


def test_pypi_keywords_as_string(pypi_evaluator):
    """Test PyPI keywords field as comma-separated string."""
    response = {
        "info": {
            "version": "1.0.0",
            "keywords": "http,api,requests"
        },
        "releases": {}
    }

    with patch.object(pypi_evaluator, 'fetch_url', return_value=response):
        data = pypi_evaluator.gather_pypi_data()

        assert isinstance(data['keywords'], list)
        assert 'http' in data['keywords']


def test_cargo_license_with_or(cargo_evaluator):
    """Test Cargo license field with OR separator."""
    response = {
        "crate": {
            "max_version": "1.0.0",
            "license": "MIT OR Apache-2.0",
            "description": "Test crate",
            "repository": "https://github.com/test/test",
            "downloads": 1000,
            "recent_downloads": 100
        }
    }

    with patch.object(cargo_evaluator, 'fetch_url', return_value=response):
        data = cargo_evaluator.gather_cargo_data()

        assert 'MIT' in data['license'] or 'Apache' in data['license']
