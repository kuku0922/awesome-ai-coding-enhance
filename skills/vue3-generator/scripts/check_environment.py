#!/usr/bin/env python3
"""
Environment checking utilities for Vue 3 project generator.

This module provides functions to check Node.js version,
pnpm installation, and other development tools.
"""

import subprocess
import sys
import json
import re
from typing import Dict, Optional, Tuple, List
from pathlib import Path


def run_command(command: List[str], timeout: int = 30) -> Tuple[bool, str, str]:
    """
    Run a shell command and return success, stdout, and stderr.

    Args:
        command: Command to run as list of strings
        timeout: Timeout in seconds

    Returns:
        Tuple of (success, stdout, stderr)
    """
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=True
        )
        return True, result.stdout.strip(), result.stderr.strip()
    except subprocess.TimeoutExpired:
        return False, "", f"Command timed out after {timeout} seconds"
    except subprocess.CalledProcessError as e:
        return False, e.stdout.strip() or "", e.stderr.strip() or f"Command failed with exit code {e.returncode}"
    except Exception as e:
        return False, "", str(e)


def check_node_version_manager() -> Tuple[str, Optional[str], bool]:
    """
    Check for Node.js version managers in priority order: fnm -> nvm -> none.

    Returns:
        Tuple of (manager_name, version, is_available)
    """
    # Check for fnm (Fast Node Manager)
    success, stdout, _ = run_command(["fnm", "--version"])
    if success:
        return "fnm", stdout, True

    # Check for nvm (Node Version Manager)
    # nvm is typically sourced in shell, so we need to check if NVM_DIR exists
    import os
    nvm_dir = os.environ.get("NVM_DIR")
    if nvm_dir and Path(nvm_dir).exists():
        # Try to run nvm command
        success, stdout, _ = run_command(["bash", "-lc", "nvm --version 2>/dev/null"])
        if success:
            return "nvm", stdout, True

    # No version manager found
    return "none", None, False


def check_node_version() -> Tuple[bool, Optional[str], str]:
    """
    Check Node.js version and compatibility with Vue 3.

    Returns:
        Tuple of (is_compatible, version, message)
    """
    # First try to get Node.js version directly
    success, stdout, stderr = run_command(["node", "--version"])
    if not success:
        return False, None, f"Node.js not found: {stderr}"

    node_version = stdout
    if node_version.startswith('v'):
        node_version = node_version[1:]

    # Check if Node.js version meets Vue 3 requirements (>= 18.0.0)
    version_parts = node_version.split('.')
    if len(version_parts) >= 2:
        major = int(version_parts[0])
        minor = int(version_parts[1])

        if major > 18:
            return True, node_version, f"Node.js {node_version} is compatible with Vue 3"
        elif major == 18 and minor >= 0:
            return True, node_version, f"Node.js {node_version} is compatible with Vue 3"
        else:
            return False, node_version, f"Node.js {node_version} is too old. Vue 3 requires Node.js >= 18.0.0"

    return False, node_version, f"Unable to parse Node.js version: {node_version}"


def check_pnpm_installation() -> Tuple[bool, Optional[str], str]:
    """
    Check if pnpm is installed and get its version.

    Returns:
        Tuple of (is_installed, version, message)
    """
    success, stdout, stderr = run_command(["pnpm", "--version"])
    if not success:
        return False, None, f"pnpm not found: {stderr}"

    pnpm_version = stdout
    return True, pnpm_version, f"pnpm {pnpm_version} is installed and ready"


def check_npm_installation() -> Tuple[bool, Optional[str], str]:
    """
    Check if npm is installed (fallback for pnpm).

    Returns:
        Tuple of (is_installed, version, message)
    """
    success, stdout, stderr = run_command(["npm", "--version"])
    if not success:
        return False, None, f"npm not found: {stderr}"

    npm_version = stdout
    return True, npm_version, f"npm {npm_version} is installed"


def check_vue_cli_tools() -> Dict[str, Tuple[bool, str]]:
    """
    Check for Vue.js CLI tools and create-vue availability.

    Returns:
        Dictionary of tool names and their availability status
    """
    tools = {}

    # Check for create-vue (official Vue 3 project scaffolding tool)
    success, stdout, stderr = run_command(["npm", "show", "create-vue", "version"])
    if success:
        tools["create-vue"] = (True, f"create-vue@{stdout} is available")
    else:
        tools["create-vue"] = (False, f"create-vue not available: {stderr}")

    # Check for @vue/cli (legacy Vue CLI)
    success, stdout, stderr = run_command(["vue", "--version"], timeout=10)
    if success:
        tools["@vue/cli"] = (True, f"@vue/cli {stdout} is installed")
    else:
        # Check if it's available via npx
        success, stdout, stderr = run_command(["npx", "@vue/cli", "--version"], timeout=15)
        if success:
            tools["@vue/cli"] = (True, f"@vue/cli available via npx")
        else:
            tools["@vue/cli"] = (False, "@vue/cli not available")

    return tools


def check_git_installation() -> Tuple[bool, Optional[str], str]:
    """
    Check if Git is installed and configured.

    Returns:
        Tuple of (is_installed, version, message)
    """
    success, stdout, stderr = run_command(["git", "--version"])
    if not success:
        return False, None, f"Git not found: {stderr}"

    git_version = stdout
    return True, git_version, f"Git is installed: {git_version}"


def check_system_compatibility() -> Dict[str, any]:
    """
    Check overall system compatibility for Vue 3 development.

    Returns:
        Dictionary containing compatibility information
    """
    compatibility = {
        "platform": sys.platform,
        "python_version": sys.version,
        "checks": {}
    }

    # Check Node.js version manager
    manager_name, manager_version, manager_available = check_node_version_manager()
    compatibility["checks"]["version_manager"] = {
        "name": manager_name,
        "version": manager_version,
        "available": manager_available,
        "recommended": manager_name != "none"
    }

    # Check Node.js version
    node_compatible, node_version, node_message = check_node_version()
    compatibility["checks"]["nodejs"] = {
        "version": node_version,
        "compatible": node_compatible,
        "message": node_message,
        "recommended": node_compatible
    }

    # Check pnpm
    pnpm_installed, pnpm_version, pnpm_message = check_pnpm_installation()
    compatibility["checks"]["pnpm"] = {
        "installed": pnpm_installed,
        "version": pnpm_version,
        "message": pnpm_message,
        "recommended": pnpm_installed
    }

    # Check npm as fallback
    npm_installed, npm_version, npm_message = check_npm_installation()
    compatibility["checks"]["npm"] = {
        "installed": npm_installed,
        "version": npm_version,
        "message": npm_message
    }

    # Check Vue tools
    compatibility["checks"]["vue_tools"] = check_vue_cli_tools()

    # Check Git
    git_installed, git_version, git_message = check_git_installation()
    compatibility["checks"]["git"] = {
        "installed": git_installed,
        "version": git_version,
        "message": git_message,
        "recommended": git_installed
    }

    # Overall compatibility assessment
    compatibility["overall_compatible"] = (
        node_compatible and
        (pnpm_installed or npm_installed) and
        git_installed
    )

    compatibility["ready_for_development"] = (
        compatibility["overall_compatible"] and
        any(tool[0] for tool in compatibility["checks"]["vue_tools"].values())
    )

    return compatibility


def suggest_package_manager() -> str:
    """
    Suggest the best package manager to use based on availability.

    Returns:
        Recommended package manager command
    """
    pnpm_installed, _, _ = check_pnpm_installation()
    npm_installed, _, _ = check_npm_installation()

    if pnpm_installed:
        return "pnpm"
    elif npm_installed:
        return "npm"
    else:
        return "pnpm"  # Default recommendation


def get_installation_commands() -> Dict[str, List[str]]:
    """
    Get commands to install missing tools.

    Returns:
        Dictionary of tool names and their installation commands
    """
    commands = {}

    # Check OS type
    is_windows = sys.platform.startswith("win")
    is_mac = sys.platform == "darwin"
    is_linux = sys.platform.startswith("linux")

    # pnpm installation
    if not check_pnpm_installation()[0]:
        if is_windows:
            commands["pnpm"] = ["iwr", "https://get.pnpm.io/install.ps1", "|", "iex"]
        else:
            commands["pnpm"] = ["curl", "-fsSL", "https://get.pnpm.io/install.sh", "|", "sh", "-"]

    # fnm installation (if no version manager)
    manager_name, _, manager_available = check_node_version_manager()
    if not manager_available:
        if is_mac:
            commands["fnm"] = ["brew", "install", "fnm"]
        elif is_linux:
            commands["fnm"] = ["curl", "-fsSL", "https://fnm.vercel.app/install", "|", "bash"]
        elif is_windows:
            commands["fnm"] = ["winget", "install", "Schniz.fnm"]

    # Node.js installation (if no Node.js)
    node_compatible, node_version, _ = check_node_version()
    if not node_compatible:
        if manager_name == "fnm":
            commands["nodejs"] = ["fnm", "install", "--lts"]
        elif manager_name == "nvm":
            commands["nodejs"] = ["bash", "-lc", "nvm install --lts"]
        else:
            if is_mac:
                commands["nodejs"] = ["brew", "install", "node"]
            elif is_windows:
                commands["nodejs"] = ["winget", "install", "OpenJS.NodeJS"]
            elif is_linux:
                commands["nodejs"] = ["curl", "-fsSL", "https://deb.nodesource.com/setup_lts.x", "|", "sudo", "-E", "bash", "-", "&&", "sudo", "apt-get", "install", "-y", "nodejs"]

    return commands


def main():
    """
    Main function to run environment checks.
    """
    print("Vue 3 Project Generator - Environment Check")
    print("=" * 50)

    compatibility = check_system_compatibility()

    print(f"Platform: {compatibility['platform']}")
    print(f"Python Version: {compatibility['python_version'].split()[0]}")
    print()

    # Version Manager
    vm = compatibility["checks"]["version_manager"]
    print(f"Version Manager: {vm['name']} {'✅' if vm['available'] else '❌'}")
    if vm['version']:
        print(f"  Version: {vm['version']}")
    print()

    # Node.js
    node = compatibility["checks"]["nodejs"]
    print(f"Node.js: {node['version'] or 'Not found'} {'✅' if node['compatible'] else '❌'}")
    print(f"  {node['message']}")
    print()

    # Package Managers
    pnpm = compatibility["checks"]["pnpm"]
    print(f"pnpm: {pnpm['version'] or 'Not installed'} {'✅' if pnpm['installed'] else '❌'}")
    print(f"  {pnpm['message']}")
    print()

    npm = compatibility["checks"]["npm"]
    print(f"npm: {npm['version'] or 'Not installed'} {'✅' if npm['installed'] else '❌'}")
    print(f"  {npm['message']}")
    print()

    # Vue Tools
    print("Vue Tools:")
    for tool, (available, message) in compatibility["checks"]["vue_tools"].items():
        print(f"  {tool}: {'✅' if available else '❌'}")
        print(f"    {message}")
    print()

    # Git
    git = compatibility["checks"]["git"]
    print(f"Git: {git['version'] or 'Not found'} {'✅' if git['installed'] else '❌'}")
    print(f"  {git['message']}")
    print()

    # Overall Status
    print("Overall Status:")
    print(f"  Compatible: {'✅' if compatibility['overall_compatible'] else '❌'}")
    print(f"  Ready for Development: {'✅' if compatibility['ready_for_development'] else '❌'}")

    if not compatibility['overall_compatible']:
        print("\nSuggested Installation Commands:")
        commands = get_installation_commands()
        for tool, cmd in commands.items():
            print(f"  {tool}: {' '.join(cmd)}")

    print(f"\nRecommended Package Manager: {suggest_package_manager()}")


if __name__ == "__main__":
    main()