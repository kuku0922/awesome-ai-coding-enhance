#!/usr/bin/env python3
"""
Version querying utilities for Go Gin project generator.

This module provides functions to query latest versions of Go packages
and frameworks from various sources including GitHub API and Go modules.
"""

import requests
import json
import re
from typing import Dict, Optional, Tuple
from packaging import version


def query_github_api_latest_release(repo_owner: str, repo_name: str) -> Optional[str]:
    """
    Query the latest release version from GitHub API.

    Args:
        repo_owner: Repository owner (e.g., "gin-gonic")
        repo_name: Repository name (e.g., "gin")

    Returns:
        Latest version string or None if failed
    """
    try:
        url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()
        tag_name = data.get("tag_name", "")

        # Remove 'v' prefix if present
        if tag_name.startswith('v'):
            tag_name = tag_name[1:]

        return tag_name
    except Exception as e:
        print(f"Failed to query GitHub API for {repo_owner}/{repo_name}: {e}")
        return None


def query_go_module_version(module_path: str) -> Optional[str]:
    """
    Query the latest version of a Go module using Go proxy API.

    Args:
        module_path: Go module path (e.g., "github.com/gin-gonic/gin")

    Returns:
        Latest version string or None if failed
    """
    try:
        url = f"https://proxy.golang.org/{module_path}/@v/list"
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        versions = response.text.strip().split('\n')
        # Filter out pre-release versions and find the latest stable version
        stable_versions = []

        for ver in versions:
            if ver and not re.search(r'-(alpha|beta|rc|pre)', ver):
                stable_versions.append(version.parse(ver))

        if stable_versions:
            latest = max(stable_versions)
            return str(latest)

        return None
    except Exception as e:
        print(f"Failed to query Go module version for {module_path}: {e}")
        return None


def get_gin_framework_info() -> Dict[str, str]:
    """
    Get comprehensive information about the Gin framework.

    Returns:
        Dictionary containing version info and import paths
    """
    gin_info = {
        "module_path": "github.com/gin-gonic/gin",
        "import_path": "github.com/gin-gonic/gin",
        "version": None,
        "github_repo": "gin-gonic/gin"
    }

    # Try GitHub API first
    latest_version = query_github_api_latest_release("gin-gonic", "gin")

    # Fallback to Go proxy if GitHub fails
    if not latest_version:
        latest_version = query_go_module_version(gin_info["module_path"])

    # Default to known stable version if both fail
    gin_info["version"] = latest_version or "1.9.1"

    return gin_info


def get_go_version_info() -> Dict[str, str]:
    """
    Get information about the latest Go version.

    Returns:
        Dictionary containing Go version info
    """
    try:
        # Query Go's official API for latest stable version
        response = requests.get("https://golang.org/dl/?mode=json", timeout=10)
        response.raise_for_status()

        data = response.json()
        if data:
            # Find the latest stable version
            stable_versions = [item for item in data if item.get("stable", False)]
            if stable_versions:
                latest = stable_versions[0]
                version_str = latest["version"]
                # Remove 'go' prefix if present
                if version_str.startswith('go'):
                    version_str = version_str[2:]
                return {"version": version_str, "stable": True}

        # Fallback to known stable version
        return {"version": "1.21.5", "stable": True}
    except Exception as e:
        print(f"Failed to query Go version: {e}")
        return {"version": "1.21.5", "stable": True}


def get_common_dependency_versions() -> Dict[str, Dict[str, str]]:
    """
    Get versions for common Go dependencies used in Gin projects.

    Returns:
        Dictionary mapping dependency names to version info
    """
    dependencies = {
        "gorm": {
            "module_path": "gorm.io/gorm",
            "import_path": "gorm.io/gorm",
            "github_repo": "go-gorm/gorm"
        },
        "gorm-driver-postgres": {
            "module_path": "gorm.io/driver/postgres",
            "import_path": "gorm.io/driver/postgres",
        },
        "gorm-driver-mysql": {
            "module_path": "gorm.io/driver/mysql",
            "import_path": "gorm.io/driver/mysql",
        },
        "gorm-driver-sqlite": {
            "module_path": "gorm.io/driver/sqlite",
            "import_path": "gorm.io/driver/sqlite",
        },
        "viper": {
            "module_path": "github.com/spf13/viper",
            "import_path": "github.com/spf13/viper",
            "github_repo": "spf13/viper"
        },
        "logrus": {
            "module_path": "github.com/sirupsen/logrus",
            "import_path": "github.com/sirupsen/logrus",
            "github_repo": "sirupsen/logrus"
        },
        "zap": {
            "module_path": "go.uber.org/zap",
            "import_path": "go.uber.org/zap",
            "github_repo": "uber-go/zap"
        },
        "jwt": {
            "module_path": "github.com/golang-jwt/jwt",
            "import_path": "github.com/golang-jwt/jwt/v5",
            "github_repo": "golang-jwt/jwt"
        },
        "validator": {
            "module_path": "github.com/go-playground/validator",
            "import_path": "github.com/go-playground/validator/v10",
            "github_repo": "go-playground/validator"
        },
        "swaggo": {
            "module_path": "github.com/swaggo/swag",
            "import_path": "github.com/swaggo/swag",
            "github_repo": "swaggo/swag"
        },
        "gin-cors": {
            "module_path": "github.com/gin-contrib/cors",
            "import_path": "github.com/gin-contrib/cors",
            "github_repo": "gin-contrib/cors"
        },
        "testify": {
            "module_path": "github.com/stretchr/testify",
            "import_path": "github.com/stretchr/testify",
            "github_repo": "stretchr/testify"
        }
    }

    # Query versions for dependencies
    for dep_name, dep_info in dependencies.items():
        if "github_repo" in dep_info:
            repo_parts = dep_info["github_repo"].split("/")
            latest_version = query_github_api_latest_release(repo_parts[0], repo_parts[1])
        else:
            latest_version = query_go_module_version(dep_info["module_path"])

        dep_info["version"] = latest_version or "latest"

    return dependencies


def generate_go_mod_content(project_name: str, module_path: str, dependencies: Dict[str, bool]) -> str:
    """
    Generate go.mod file content with specified dependencies.

    Args:
        project_name: Name of the project
        module_path: Go module path (e.g., "github.com/user/project")
        dependencies: Dictionary of dependencies to include

    Returns:
        go.mod file content as string
    """
    lines = [
        f"module {module_path}",
        "",
        f"go {get_go_version_info()['version']}",
        ""
    ]

    # Get Gin and dependency versions
    gin_info = get_gin_framework_info()
    all_deps = get_common_dependency_versions()

    # Always include Gin
    lines.append(f"\trequire {gin_info['import_path']} v{gin_info['version']}")

    # Add selected dependencies
    for dep_name, include in dependencies.items():
        if include and dep_name in all_deps:
            dep_info = all_deps[dep_name]
            version = dep_info["version"]
            if version != "latest":
                lines.append(f"\trequire {dep_info['import_path']} v{version}")

    lines.append("")

    return "\n".join(lines)


if __name__ == "__main__":
    # Test the version querying functionality
    print("=== Go Gin Generator - Version Query Test ===")

    print("\n-- Gin Framework Info --")
    gin_info = get_gin_framework_info()
    print(f"Import Path: {gin_info['import_path']}")
    print(f"Latest Version: v{gin_info['version']}")

    print("\n-- Go Version Info --")
    go_info = get_go_version_info()
    print(f"Go Version: {go_info['version']}")

    print("\n-- Common Dependencies --")
    deps = get_common_dependency_versions()
    for name, info in list(deps.items())[:5]:  # Show first 5 for testing
        print(f"{name}: {info['import_path']} v{info['version']}")

    print(f"\n... and {len(deps) - 5} more dependencies")