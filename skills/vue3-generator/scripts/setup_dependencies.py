#!/usr/bin/env python3
"""
Dependency management utilities for Vue 3 project generator.

This module provides functions to manage project dependencies using pnpm,
including installation, updates, and version management.
"""

import subprocess
import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional

from query_versions import get_all_vue3_dependencies, get_dev_dependencies_info
from check_environment import run_command, suggest_package_manager


class VueDependencyManager:
    """Manages dependencies for Vue 3 projects."""

    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.package_manager = suggest_package_manager()

    def run_in_project(self, command: List[str], timeout: int = 120) -> Tuple[bool, str, str]:
        """Run a command in the project directory."""
        try:
            # Save current directory
            original_cwd = Path.cwd()

            # Change to project directory
            import os
            os.chdir(self.project_path)

            # Run command
            success, stdout, stderr = run_command(command, timeout)

            return success, stdout, stderr

        except Exception as e:
            return False, "", str(e)
        finally:
            # Restore original directory
            import os
            os.chdir(original_cwd)

    def install_dependencies(self) -> bool:
        """Install all project dependencies."""
        print("📦 Installing dependencies...")

        success, stdout, stderr = self.run_in_project([self.package_manager, "install"])

        if success:
            print("✅ Dependencies installed successfully!")
            return True
        else:
            print(f"❌ Failed to install dependencies: {stderr}")
            return False

    def add_dependency(self, package_name: str, version: Optional[str] = None, dev: bool = False) -> bool:
        """Add a new dependency to the project."""
        version_spec = f"@{version}" if version else ""
        package_spec = f"{package_name}{version_spec}"

        print(f"📦 Adding {package_spec}...")

        cmd = [self.package_manager, "add"]
        if dev:
            cmd.append("-D")
        cmd.append(package_spec)

        success, stdout, stderr = self.run_in_project(cmd)

        if success:
            print(f"✅ {package_spec} added successfully!")
            return True
        else:
            print(f"❌ Failed to add {package_spec}: {stderr}")
            return False

    def remove_dependency(self, package_name: str) -> bool:
        """Remove a dependency from the project."""
        print(f"🗑️  Removing {package_name}...")

        success, stdout, stderr = self.run_in_project([self.package_manager, "remove", package_name])

        if success:
            print(f"✅ {package_name} removed successfully!")
            return True
        else:
            print(f"❌ Failed to remove {package_name}: {stderr}")
            return False

    def update_dependency(self, package_name: str, version: Optional[str] = None) -> bool:
        """Update a dependency to the latest or specified version."""
        version_spec = f"@{version}" if version else ""
        package_spec = f"{package_name}{version_spec}"

        print(f"🔄 Updating {package_spec}...")

        success, stdout, stderr = self.run_in_project([self.package_manager, "update", package_spec])

        if success:
            print(f"✅ {package_spec} updated successfully!")
            return True
        else:
            print(f"❌ Failed to update {package_spec}: {stderr}")
            return False

    def update_all_dependencies(self) -> bool:
        """Update all project dependencies."""
        print("🔄 Updating all dependencies...")

        success, stdout, stderr = self.run_in_project([self.package_manager, "update"])

        if success:
            print("✅ All dependencies updated successfully!")
            return True
        else:
            print(f"❌ Failed to update dependencies: {stderr}")
            return False

    def get_installed_packages(self) -> Dict[str, Dict[str, str]]:
        """Get list of installed packages with their versions."""
        packages = {}

        # Get production dependencies
        success, stdout, stderr = self.run_in_project([self.package_manager, "list", "--prod", "--json"])
        if success:
            try:
                prod_deps = json.loads(stdout)
                for name, info in prod_deps.items():
                    packages[name] = {
                        "version": info.get("version", "unknown"),
                        "type": "production"
                    }
            except json.JSONDecodeError:
                print(f"⚠️  Could not parse production dependencies: {stderr}")

        # Get development dependencies
        success, stdout, stderr = self.run_in_project([self.package_manager, "list", "--dev", "--json"])
        if success:
            try:
                dev_deps = json.loads(stdout)
                for name, info in dev_deps.items():
                    if name not in packages:  # Don't overwrite prod deps
                        packages[name] = {
                            "version": info.get("version", "unknown"),
                            "type": "development"
                        }
            except json.JSONDecodeError:
                print(f"⚠️  Could not parse development dependencies: {stderr}")

        return packages

    def check_outdated_packages(self) -> Dict[str, Dict[str, str]]:
        """Check for outdated packages."""
        print("🔍 Checking for outdated packages...")

        success, stdout, stderr = self.run_in_project([self.package_manager, "outdated", "--json"])

        if not success:
            print(f"⚠️  Could not check outdated packages: {stderr}")
            return {}

        try:
            outdated = json.loads(stdout)
            return outdated
        except json.JSONDecodeError:
            print(f"⚠️  Could not parse outdated packages information")
            return {}

    def setup_vue3_project(self, config: Dict[str, Dict[str, str]]) -> bool:
        """Setup complete Vue 3 project dependencies."""
        print("🔧 Setting up Vue 3 project dependencies...")

        # Check if we're in a valid project directory
        package_json_path = self.project_path / "package.json"
        if not package_json_path.exists():
            print(f"❌ No package.json found in {self.project_path}")
            return False

        # Install core dependencies
        print("\n📦 Installing core Vue 3 dependencies...")
        core_deps = ["vue", "vue-router", "pinia"]
        for dep in core_deps:
            if dep in config:
                version = config[dep].get("version")
                if version:
                    if not self.add_dependency(dep, version):
                        print(f"⚠️  Failed to add {dep}, continuing...")

        # Install development dependencies
        print("\n📦 Installing development dependencies...")
        dev_deps = [
            "@vitejs/plugin-vue",
            "typescript",
            "vue-tsc",
            "vite",
            "@vue/eslint-config-typescript",
            "@vue/eslint-config-prettier",
            "eslint",
            "eslint-plugin-vue",
            "prettier",
            "vitest",
            "@vue/test-utils"
        ]

        for dep in dev_deps:
            if dep in config:
                version = config[dep].get("version")
                if version:
                    if not self.add_dependency(dep, version, dev=True):
                        print(f"⚠️  Failed to add {dep}, continuing...")

        # Install CSS framework if specified
        css_framework = config.get("css_framework")
        if css_framework and css_framework != "none":
            print(f"\n🎨 Installing {css_framework}...")
            if css_framework == "tailwindcss":
                self.add_dependency("tailwindcss", dev=True)
                self.add_dependency("autoprefixer", dev=True)
                self.add_dependency("postcss", dev=True)
            elif css_framework == "bootstrap":
                self.add_dependency("bootstrap")
                self.add_dependency("@popperjs/core")
            elif css_framework == "bulma":
                self.add_dependency("bulma")

        # Final install to resolve all dependencies
        print("\n🔄 Resolving all dependencies...")
        return self.install_dependencies()

    def clean_dependencies(self) -> bool:
        """Clean and optimize dependencies."""
        print("🧹 Cleaning dependencies...")

        success, stdout, stderr = self.run_in_project([self.package_manager, "prune"])

        if success:
            print("✅ Dependencies cleaned successfully!")
            return True
        else:
            print(f"❌ Failed to clean dependencies: {stderr}")
            return False

    def get_dependency_info(self, package_name: str) -> Optional[Dict[str, str]]:
        """Get detailed information about a specific dependency."""
        success, stdout, stderr = self.run_in_project([self.package_manager, "info", package_name, "--json"])

        if not success:
            print(f"❌ Could not get info for {package_name}: {stderr}")
            return None

        try:
            info = json.loads(stdout)
            return info
        except json.JSONDecodeError:
            print(f"❌ Could not parse dependency info for {package_name}")
            return None

    def audit_dependencies(self) -> bool:
        """Check for security vulnerabilities in dependencies."""
        print("🔒 Auditing dependencies for security vulnerabilities...")

        # pnpm uses different commands for auditing
        if self.package_manager == "pnpm":
            success, stdout, stderr = self.run_in_project([self.package_manager, "audit"])
        else:
            success, stdout, stderr = self.run_in_project([self.package_manager, "audit"])

        if success:
            print("✅ Dependency audit completed!")
            print(stdout)
            return True
        else:
            print(f"❌ Dependency audit failed: {stderr}")
            return False

    def generate_dependency_report(self) -> Dict[str, any]:
        """Generate a comprehensive dependency report."""
        print("📊 Generating dependency report...")

        report = {
            "project_path": str(self.project_path),
            "package_manager": self.package_manager,
            "installed_packages": self.get_installed_packages(),
            "outdated_packages": self.check_outdated_packages(),
            "audit_passed": self.audit_dependencies()
        }

        return report


def main():
    """Main function for dependency management."""
    if len(sys.argv) < 2:
        print("Usage: python setup_dependencies.py <project_path> [command]")
        print("Commands:")
        print("  install     - Install all dependencies")
        print("  update      - Update all dependencies")
        print("  clean       - Clean dependencies")
        print("  audit       - Audit dependencies for vulnerabilities")
        print("  report      - Generate dependency report")
        sys.exit(1)

    project_path = sys.argv[1]
    command = sys.argv[2] if len(sys.argv) > 2 else "install"

    manager = VueDependencyManager(project_path)

    if command == "install":
        success = manager.install_dependencies()
    elif command == "update":
        success = manager.update_all_dependencies()
    elif command == "clean":
        success = manager.clean_dependencies()
    elif command == "audit":
        success = manager.audit_dependencies()
    elif command == "report":
        report = manager.generate_dependency_report()
        print(json.dumps(report, indent=2))
        success = True
    else:
        print(f"❌ Unknown command: {command}")
        success = False

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()