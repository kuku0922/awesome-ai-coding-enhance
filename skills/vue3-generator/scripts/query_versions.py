#!/usr/bin/env python3
"""
Version querying utilities for Vue 3 project generator.

This module provides functions to query latest versions of Vue 3
and related packages from npm registry and GitHub API.
"""

import requests
import json
import re
from typing import Dict, Optional, List
from packaging import version


def query_npm_latest_version(package_name: str) -> Optional[str]:
    """
    Query the latest stable version from npm registry.

    Args:
        package_name: npm package name (e.g., "vue", "typescript")

    Returns:
        Latest version string or None if failed
    """
    try:
        url = f"https://registry.npmjs.org/{package_name}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()
        versions = data.get("versions", {})
        dist_tags = data.get("dist-tags", {})

        # Try to get the latest stable version from dist-tags
        latest_version = dist_tags.get("latest")

        if latest_version:
            # Verify it's not a pre-release version
            if not re.search(r'-(alpha|beta|rc|pre|next)', latest_version):
                return latest_version

        # If dist-tags latest is pre-release or not available, find latest stable
        stable_versions = []
        for ver in versions.keys():
            if not re.search(r'-(alpha|beta|rc|pre|next|dev)', ver):
                try:
                    stable_versions.append(version.parse(ver))
                except:
                    continue

        if stable_versions:
            latest = max(stable_versions)
            return str(latest)

        return None
    except Exception as e:
        print(f"Failed to query npm registry for {package_name}: {e}")
        return None


def get_vue3_info() -> Dict[str, str]:
    """
    Get comprehensive information about Vue 3 framework.

    Returns:
        Dictionary containing version info and package names
    """
    vue_info = {
        "package_name": "vue",
        "version": None,
        "peer_dependencies": [],
        "github_repo": "vuejs/vue"
    }

    # Query latest Vue 3 version
    latest_version = query_npm_latest_version("vue")
    vue_info["version"] = latest_version or "3.4.0"  # Known stable fallback

    return vue_info


def get_typescript_info() -> Dict[str, str]:
    """
    Get TypeScript information compatible with Vue 3.

    Returns:
        Dictionary containing TypeScript version info
    """
    ts_info = {
        "package_name": "typescript",
        "version": None,
        "dev": True  # TypeScript is typically a dev dependency
    }

    latest_version = query_npm_latest_version("typescript")
    ts_info["version"] = latest_version or "5.3.0"  # Known stable fallback

    return ts_info


def get_vite_info() -> Dict[str, str]:
    """
    Get Vite information for Vue 3 projects.

    Returns:
        Dictionary containing Vite version info
    """
    vite_info = {
        "package_name": "vite",
        "version": None,
        "dev": True
    }

    latest_version = query_npm_latest_version("vite")
    vite_info["version"] = latest_version or "5.0.0"  # Known stable fallback

    return vite_info


def get_vue_router_info() -> Dict[str, str]:
    """
    Get Vue Router information compatible with Vue 3.

    Returns:
        Dictionary containing Vue Router version info
    """
    router_info = {
        "package_name": "vue-router",
        "version": None
    }

    latest_version = query_npm_latest_version("vue-router")
    router_info["version"] = latest_version or "4.2.0"  # Known stable fallback

    return router_info


def get_pinia_info() -> Dict[str, str]:
    """
    Get Pinia state management information.

    Returns:
        Dictionary containing Pinia version info
    """
    pinia_info = {
        "package_name": "pinia",
        "version": None
    }

    latest_version = query_npm_latest_version("pinia")
    pinia_info["version"] = latest_version or "2.1.0"  # Known stable fallback

    return pinia_info


def get_dev_dependencies_info() -> Dict[str, Dict[str, str]]:
    """
    Get information about common development dependencies for Vue 3 projects.

    Returns:
        Dictionary containing development dependencies version info
    """
    dev_deps = [
        "@vitejs/plugin-vue",
        "@vue/tsconfig",
        "@rushstack/eslint-patch",
        "@vue/eslint-config-typescript",
        "@vue/eslint-config-prettier",
        "eslint",
        "eslint-plugin-vue",
        "prettier",
        "vitest",
        "@vue/test-utils",
        "jsdom",
        "typescript"
    ]

    dev_dependencies = {}

    for dep in dev_deps:
        ver = query_npm_latest_version(dep)
        dev_dependencies[dep] = {
            "version": ver,
            "dev": True
        }

    # Add fallbacks for common dependencies
    fallbacks = {
        "@vitejs/plugin-vue": "4.5.0",
        "@vue/tsconfig": "0.4.0",
        "@rushstack/eslint-patch": "1.3.0",
        "@vue/eslint-config-typescript": "12.0.0",
        "@vue/eslint-config-prettier": "8.0.0",
        "eslint": "8.50.0",
        "eslint-plugin-vue": "9.17.0",
        "prettier": "3.0.0",
        "vitest": "1.0.0",
        "@vue/test-utils": "2.4.0",
        "jsdom": "23.0.0",
        "typescript": "5.3.0"
    }

    for dep, fallback in fallbacks.items():
        if not dev_dependencies[dep]["version"]:
            dev_dependencies[dep]["version"] = fallback

    return dev_dependencies


def get_css_framework_info(framework_name: str = "tailwindcss") -> Optional[Dict[str, str]]:
    """
    Get CSS framework information.

    Args:
        framework_name: CSS framework name (tailwindcss, bootstrap, etc.)

    Returns:
        Dictionary containing CSS framework version info or None if not found
    """
    css_frameworks = {
        "tailwindcss": {
            "package_name": "tailwindcss",
            "autoprefixer": "autoprefixer",
            "postcss": "postcss"
        },
        "bootstrap": {
            "package_name": "bootstrap",
            "package_name_vue": "bootstrap-vue-3"
        },
        "bulma": {
            "package_name": "bulma"
        }
    }

    if framework_name not in css_frameworks:
        return None

    framework_info = css_frameworks[framework_name].copy()

    # Query main package
    main_package = framework_info["package_name"]
    ver = query_npm_latest_version(main_package)
    framework_info["version"] = ver or "latest"

    # Query additional packages if they exist
    for key, package in framework_info.items():
        if key not in ["package_name", "version"] and package != main_package:
            package_ver = query_npm_latest_version(package)
            framework_info[f"{key}_version"] = package_ver or "latest"

    return framework_info


def get_all_vue3_dependencies(include_css_framework: str = None) -> Dict[str, Dict[str, str]]:
    """
    Get all dependencies needed for a Vue 3 project.

    Args:
        include_css_framework: Optional CSS framework to include

    Returns:
        Dictionary containing all dependencies with version info
    """
    dependencies = {
        "vue": get_vue3_info(),
        "vue-router": get_vue_router_info(),
        "pinia": get_pinia_info()
    }

    # Add CSS framework if requested
    if include_css_framework:
        css_info = get_css_framework_info(include_css_framework)
        if css_info:
            dependencies.update(css_info)

    return dependencies


def generate_package_json_content(
    project_name: str,
    project_description: str,
    dependencies: Dict[str, Dict[str, str]],
    dev_dependencies: Dict[str, Dict[str, str]],
    project_type: str = "spa"
) -> str:
    """
    Generate package.json content for Vue 3 project.

    Args:
        project_name: Name of the project
        project_description: Description of the project
        dependencies: Production dependencies
        dev_dependencies: Development dependencies
        project_type: Type of project (spa, pwa, component-lib, admin-dashboard)

    Returns:
        Formatted package.json content as string
    """

    # Filter dependencies by version
    deps = {name: info["version"] for name, info in dependencies.items() if info.get("version")}
    dev_deps = {name: info["version"] for name, info in dev_dependencies.items() if info.get("version")}

    package_json = {
        "name": project_name,
        "version": "0.0.0",
        "description": project_description,
        "type": "module",
        "scripts": {
            "dev": "vite",
            "build": "run-p type-check \"build-only {@}\" --",
            "preview": "vite preview",
            "build-only": "vite build",
            "type-check": "vue-tsc --build --force",
            "lint": "eslint . --ext .vue,.js,.jsx,.cjs,.mjs,.ts,.tsx,.cts,.mts --fix --ignore-path .gitignore",
            "format": "prettier --write src/",
            "test": "vitest"
        },
        "dependencies": deps,
        "devDependencies": dev_deps
    }

    # Add project type specific configurations
    if project_type == "pwa":
        package_json["dependencies"].update({
            "@vite-pwa/vite-plugin": "^0.17.0",
            "workbox-window": "^7.0.0"
        })

    if project_type == "component-lib":
        package_json["scripts"]["build"] = "vite build && vue-tsc --emitDeclarationOnly"
        package_json["main"] = "./dist/index.js"
        package_json["module"] = "./dist/index.js"
        package_json["types"] = "./dist/index.d.ts"
        package_json["exports"] = {
            ".": {
                "import": "./dist/index.js",
                "types": "./dist/index.d.ts"
            }
        }

    return json.dumps(package_json, indent=2)


def main():
    """
    Main function for testing version queries.
    """
    print("Vue 3 Project Generator - Version Query Tool")
    print("=" * 50)

    # Test version queries
    vue_info = get_vue3_info()
    print(f"Vue 3: {vue_info['version']}")

    vite_info = get_vite_info()
    print(f"Vite: {vite_info['version']}")

    router_info = get_vue_router_info()
    print(f"Vue Router: {router_info['version']}")

    pinia_info = get_pinia_info()
    print(f"Pinia: {pinia_info['version']}")

    ts_info = get_typescript_info()
    print(f"TypeScript: {ts_info['version']}")

    print("\nAll dependencies queried successfully!")


if __name__ == "__main__":
    main()