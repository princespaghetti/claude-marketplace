#!/usr/bin/env python3
"""
Dependency evaluator script for gathering package ecosystem data.
Automates command execution and data collection for dependency analysis.

Uses only Python standard library - no external dependencies required.
"""

import argparse
import json
import subprocess
import sys
import urllib.request
import urllib.error
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple


class DependencyEvaluator:
    """Main class for evaluating dependencies across package ecosystems."""

    def __init__(self, package_name: str, ecosystem: str):
        """
        Initialize the dependency evaluator.

        Args:
            package_name: Name of the package to evaluate
            ecosystem: Package ecosystem (npm, pypi, cargo, go)
        """
        self.package_name = package_name
        self.ecosystem = ecosystem.lower()
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def run_command(self, cmd: List[str], timeout: int = 30) -> Tuple[bool, str, str]:
        """
        Execute a shell command and return results.

        Args:
            cmd: Command and arguments as list
            timeout: Command timeout in seconds

        Returns:
            Tuple of (success, stdout, stderr)
        """
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            return (result.returncode == 0, result.stdout, result.stderr)
        except subprocess.TimeoutExpired:
            self.warnings.append(f"Command timed out after {timeout}s: {' '.join(cmd)}")
            return (False, "", f"Timeout after {timeout}s")
        except FileNotFoundError:
            self.warnings.append(f"Command not found: {cmd[0]}")
            return (False, "", f"Command not found: {cmd[0]}")
        except Exception as e:
            self.warnings.append(f"Command failed: {' '.join(cmd)} - {str(e)}")
            return (False, "", str(e))

    def fetch_url(self, url: str, timeout: int = 10) -> Optional[Dict[str, Any]]:
        """
        Fetch JSON data from a URL.

        Args:
            url: URL to fetch
            timeout: Request timeout in seconds

        Returns:
            Parsed JSON data or None on failure
        """
        try:
            req = urllib.request.Request(url)
            req.add_header('User-Agent', 'dependency-evaluator/1.0')

            with urllib.request.urlopen(req, timeout=timeout) as response:
                data = response.read().decode('utf-8')
                return json.loads(data)
        except urllib.error.HTTPError as e:
            if e.code == 404:
                self.errors.append(f"Resource not found: {url}")
            elif e.code == 403:
                self.warnings.append(f"Access forbidden (rate limit?): {url}")
            else:
                self.warnings.append(f"HTTP {e.code} error fetching {url}")
            return None
        except urllib.error.URLError as e:
            self.warnings.append(f"Network error fetching {url}: {str(e)}")
            return None
        except json.JSONDecodeError as e:
            self.warnings.append(f"Invalid JSON from {url}: {str(e)}")
            return None
        except Exception as e:
            self.warnings.append(f"Error fetching {url}: {str(e)}")
            return None

    def gather_npm_data(self) -> Dict[str, Any]:
        """Gather data for npm packages."""
        data = {}

        # Get package metadata
        success, stdout, stderr = self.run_command(['npm', 'view', self.package_name, '--json'])
        if success and stdout:
            try:
                npm_data = json.loads(stdout)
                data['latest_version'] = npm_data.get('version', '')
                data['license'] = npm_data.get('license', '')
                data['description'] = npm_data.get('description', '')
                data['homepage'] = npm_data.get('homepage', '')
                data['repository_url'] = npm_data.get('repository', {}).get('url', '') if isinstance(npm_data.get('repository'), dict) else npm_data.get('repository', '')
                data['maintainers'] = npm_data.get('maintainers', [])
                data['keywords'] = npm_data.get('keywords', [])
            except json.JSONDecodeError:
                self.warnings.append("Failed to parse npm view output")

        # Get version history
        success, stdout, stderr = self.run_command(['npm', 'view', self.package_name, 'time', '--json'])
        if success and stdout:
            try:
                time_data = json.loads(stdout)
                data['publish_history'] = time_data
                data['versions_count'] = len([k for k in time_data.keys() if k not in ['created', 'modified']])
            except json.JSONDecodeError:
                self.warnings.append("Failed to parse npm time output")

        # Get all versions
        success, stdout, stderr = self.run_command(['npm', 'view', self.package_name, 'versions', '--json'])
        if success and stdout:
            try:
                versions = json.loads(stdout)
                data['all_versions'] = versions if isinstance(versions, list) else [versions]
            except json.JSONDecodeError:
                self.warnings.append("Failed to parse npm versions output")

        return data

    def gather_pypi_data(self) -> Dict[str, Any]:
        """Gather data for PyPI packages."""
        data = {}

        # Use PyPI JSON API
        pypi_url = f"https://pypi.org/pypi/{self.package_name}/json"
        pypi_data = self.fetch_url(pypi_url)

        if pypi_data:
            info = pypi_data.get('info', {})
            data['latest_version'] = info.get('version', '')
            data['license'] = info.get('license', '')
            data['description'] = info.get('summary', '')
            data['homepage'] = info.get('home_page', '')
            data['repository_url'] = info.get('project_urls', {}).get('Source', info.get('project_url', ''))
            data['author'] = info.get('author', '')
            data['keywords'] = info.get('keywords', '').split(',') if info.get('keywords') else []

            # Get release history
            releases = pypi_data.get('releases', {})
            data['versions_count'] = len(releases)
            data['publish_history'] = {
                version: release_list[0].get('upload_time', '') if release_list else ''
                for version, release_list in releases.items()
            }

        return data

    def gather_cargo_data(self) -> Dict[str, Any]:
        """Gather data for Cargo/Rust crates."""
        data = {}

        # Use crates.io API
        crates_url = f"https://crates.io/api/v1/crates/{self.package_name}"
        crate_data = self.fetch_url(crates_url)

        if crate_data and 'crate' in crate_data:
            crate = crate_data['crate']
            data['latest_version'] = crate.get('max_version', '')
            data['license'] = ', '.join(crate.get('license', '').split(' OR '))
            data['description'] = crate.get('description', '')
            data['homepage'] = crate.get('homepage', '')
            data['repository_url'] = crate.get('repository', '')
            data['downloads'] = crate.get('downloads', 0)
            data['recent_downloads'] = crate.get('recent_downloads', 0)

            # Get versions
            versions_url = f"https://crates.io/api/v1/crates/{self.package_name}/versions"
            versions_data = self.fetch_url(versions_url)
            if versions_data and 'versions' in versions_data:
                data['versions_count'] = len(versions_data['versions'])
                data['all_versions'] = [v.get('num', '') for v in versions_data['versions']]

        return data

    def gather_go_data(self) -> Dict[str, Any]:
        """Gather data for Go modules."""
        data = {}

        # Try go list command
        success, stdout, stderr = self.run_command(['go', 'list', '-m', '-json', self.package_name])
        if success and stdout:
            try:
                go_data = json.loads(stdout)
                data['module_path'] = go_data.get('Path', '')
                data['latest_version'] = go_data.get('Version', '')
                data['time'] = go_data.get('Time', '')
            except json.JSONDecodeError:
                self.warnings.append("Failed to parse go list output")

        return data

    def extract_github_repo(self, repo_url: str) -> Optional[Tuple[str, str]]:
        """
        Extract owner and repo name from GitHub URL.

        Args:
            repo_url: GitHub repository URL

        Returns:
            Tuple of (owner, repo) or None
        """
        if not repo_url:
            return None

        # Handle various GitHub URL formats
        import re
        patterns = [
            r'github\.com[:/]([^/]+)/([^/\.]+)',
            r'github\.com/([^/]+)/([^/\.]+)',
        ]

        for pattern in patterns:
            match = re.search(pattern, repo_url)
            if match:
                owner, repo = match.groups()
                # Remove .git suffix if present
                repo = repo.replace('.git', '')
                return (owner, repo)

        return None

    def gather_github_data(self, repo_url: str) -> Dict[str, Any]:
        """
        Gather data from GitHub repository.

        Args:
            repo_url: GitHub repository URL

        Returns:
            Dictionary of GitHub data
        """
        data = {}

        github_info = self.extract_github_repo(repo_url)
        if not github_info:
            self.warnings.append(f"Could not parse GitHub URL: {repo_url}")
            return data

        owner, repo = github_info
        data['repository_url'] = f"https://github.com/{owner}/{repo}"

        # Try using gh CLI first
        success, stdout, stderr = self.run_command(['gh', 'api', f'repos/{owner}/{repo}'])
        if success and stdout:
            try:
                repo_data = json.loads(stdout)
                data['pushed_at'] = repo_data.get('pushed_at', '')
                data['open_issues_count'] = repo_data.get('open_issues_count', 0)
                data['stargazers_count'] = repo_data.get('stargazers_count', 0)
                data['forks_count'] = repo_data.get('forks_count', 0)
                data['watchers_count'] = repo_data.get('watchers_count', 0)
                data['default_branch'] = repo_data.get('default_branch', '')
            except json.JSONDecodeError:
                self.warnings.append("Failed to parse gh api output")
        else:
            # Fallback to direct API call
            api_url = f"https://api.github.com/repos/{owner}/{repo}"
            repo_data = self.fetch_url(api_url)
            if repo_data:
                data['pushed_at'] = repo_data.get('pushed_at', '')
                data['open_issues_count'] = repo_data.get('open_issues_count', 0)
                data['stargazers_count'] = repo_data.get('stargazers_count', 0)
                data['forks_count'] = repo_data.get('forks_count', 0)
                data['watchers_count'] = repo_data.get('watchers_count', 0)
                data['default_branch'] = repo_data.get('default_branch', '')

        # Get community health
        success, stdout, stderr = self.run_command(['gh', 'api', f'repos/{owner}/{repo}/community/profile'])
        if success and stdout:
            try:
                community_data = json.loads(stdout)
                data['community_health'] = {
                    'health_percentage': community_data.get('health_percentage', 0),
                    'files': community_data.get('files', {})
                }
            except json.JSONDecodeError:
                pass

        # Get contributors count
        success, stdout, stderr = self.run_command(['gh', 'api', f'repos/{owner}/{repo}/contributors', '--jq', 'length'])
        if success and stdout.strip().isdigit():
            data['contributors_count'] = int(stdout.strip())

        # Get license
        success, stdout, stderr = self.run_command(['gh', 'api', f'repos/{owner}/{repo}/license', '--jq', '.license.spdx_id'])
        if success and stdout.strip():
            data['license_info'] = {'spdx_id': stdout.strip()}

        return data

    def gather_security_data(self) -> Dict[str, Any]:
        """Gather security-related data."""
        data = {}

        if self.ecosystem == 'npm':
            # Note: npm audit requires package.json, which we don't have in isolation
            # This is a limitation - would need to create temp package.json
            self.warnings.append("npm audit requires package.json context - skipping")

        return data

    def gather_dependency_footprint(self) -> Dict[str, Any]:
        """Gather dependency tree information."""
        data = {
            'direct_dependencies': 0,
            'total_dependencies': 0,
            'tree_depth': 1
        }

        if self.ecosystem == 'npm':
            # npm ls requires the package to be installed
            self.warnings.append("npm ls requires package installation - skipping")

        return data

    def evaluate(self) -> Dict[str, Any]:
        """
        Run the full evaluation and return structured results.

        Returns:
            Dictionary containing all gathered data
        """
        result = {
            'package': self.package_name,
            'ecosystem': self.ecosystem,
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'registry_data': {},
            'github_data': {},
            'security_data': {},
            'dependency_footprint': {},
            'errors': [],
            'warnings': []
        }

        # Gather ecosystem-specific data
        if self.ecosystem == 'npm':
            result['registry_data'] = self.gather_npm_data()
        elif self.ecosystem == 'pypi':
            result['registry_data'] = self.gather_pypi_data()
        elif self.ecosystem == 'cargo':
            result['registry_data'] = self.gather_cargo_data()
        elif self.ecosystem == 'go':
            result['registry_data'] = self.gather_go_data()
        else:
            self.errors.append(f"Unsupported ecosystem: {self.ecosystem}")
            result['errors'] = self.errors
            result['warnings'] = self.warnings
            return result

        # Gather GitHub data if repository URL found
        repo_url = result['registry_data'].get('repository_url', '')
        if repo_url and 'github.com' in repo_url:
            result['github_data'] = self.gather_github_data(repo_url)

        # Gather security data
        result['security_data'] = self.gather_security_data()

        # Gather dependency footprint
        result['dependency_footprint'] = self.gather_dependency_footprint()

        # Add errors and warnings
        result['errors'] = self.errors
        result['warnings'] = self.warnings

        return result


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description='Evaluate a package dependency across different ecosystems'
    )
    parser.add_argument(
        'package',
        help='Package name to evaluate'
    )
    parser.add_argument(
        'ecosystem',
        choices=['npm', 'pypi', 'cargo', 'go'],
        help='Package ecosystem'
    )

    args = parser.parse_args()

    evaluator = DependencyEvaluator(args.package, args.ecosystem)
    result = evaluator.evaluate()

    # Output JSON to stdout
    print(json.dumps(result, indent=2))

    # Return non-zero exit code if there were errors
    if result['errors']:
        sys.exit(1)


if __name__ == '__main__':
    main()
