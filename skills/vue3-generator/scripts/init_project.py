#!/usr/bin/env python3
"""
Main project initialization script for Vue 3 project generator.

This script orchestrates the complete creation of a Vue 3 frontend application
with all necessary directories, files, dependencies, and configurations.
"""

import os
import sys
import json
import argparse
import subprocess
import shutil
from pathlib import Path
from typing import Dict, Any, Optional, List

from query_versions import (
    get_all_vue3_dependencies,
    get_dev_dependencies_info,
    generate_package_json_content
)
from check_environment import (
    check_system_compatibility,
    suggest_package_manager,
    get_installation_commands,
    run_command
)


class Vue3ProjectGenerator:
    """Main class for generating Vue 3 projects."""

    def __init__(self):
        self.project_types = ["spa", "pwa", "component-lib", "admin-dashboard"]
        self.css_frameworks = ["none", "tailwindcss", "bootstrap", "bulma"]
        self.default_config = self._get_default_config()

    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration for Vue 3 projects."""
        return {
            "project_name": "my-vue-app",
            "project_description": "A Vue 3 project",
            "project_type": "spa",
            "css_framework": "none",
            "typescript": True,
            "router": True,
            "pinia": True,
            "vitest": True,
            "eslint": True,
            "prettier": True,
            "author": "",
            "license": "MIT"
        }

    def check_prerequisites(self) -> bool:
        """Check if all prerequisites are met for Vue 3 development."""
        print("🔍 Checking prerequisites...")

        compatibility = check_system_compatibility()

        if not compatibility["overall_compatible"]:
            print("❌ Prerequisites check failed:")

            if not compatibility["checks"]["nodejs"]["compatible"]:
                print(f"  - Node.js issue: {compatibility['checks']['nodejs']['message']}")

            if not compatibility["checks"]["pnpm"]["installed"] and not compatibility["checks"]["npm"]["installed"]:
                print("  - No package manager found (pnpm or npm required)")

            if not compatibility["checks"]["git"]["installed"]:
                print("  - Git not found (recommended for version control)")

            print("\n💡 Suggested installation commands:")
            commands = get_installation_commands()
            for tool, cmd in commands.items():
                print(f"  {tool}: {' '.join(cmd)}")

            return False

        print("✅ All prerequisites met!")
        return True

    def setup_environment(self) -> str:
        """Setup the development environment and return package manager command."""
        print("🔧 Setting up development environment...")

        package_manager = suggest_package_manager()
        print(f"📦 Using {package_manager} as package manager")

        # Check if create-vue is available
        success, stdout, stderr = run_command([package_manager, "show", "create-vue", "version"])
        if not success:
            print(f"⚠️  create-vue not found, will install it...")
            success, _, error = run_command([package_manager, "add", "-g", "create-vue"])
            if not success:
                print(f"❌ Failed to install create-vue: {error}")
                return None

        print(f"✅ Environment setup complete!")
        return package_manager

    def create_vue_project(self, config: Dict[str, Any], package_manager: str) -> bool:
        """Create Vue 3 project using create-vue."""
        print(f"🚀 Creating Vue 3 project '{config['project_name']}'...")

        project_path = Path(config["project_name"])

        # Remove existing directory if it exists
        if project_path.exists():
            print(f"⚠️  Directory '{config['project_name']}' already exists")
            response = input("  Delete existing directory? (y/N): ")
            if response.lower() in ['y', 'yes']:
                shutil.rmtree(project_path)
                print(f"  🗑️  Removed existing directory")
            else:
                print("  ❌ Project creation cancelled")
                return False

        # Prepare create-vue command
        cmd = [package_manager, "create", "vue@latest", config["project_name"]]

        # Prepare responses for interactive prompts
        responses = []
        responses.append("yes" if config.get("typescript", True) else "no")  # TypeScript
        responses.append("yes" if config.get("router", True) else "no")     # Router
        responses.append("yes" if config.get("pinia", True) else "no")      # Pinia
        responses.append("yes" if config.get("vitest", True) else "no")     # Vitest
        responses.append("yes" if config.get("eslint", True) else "no")     # ESLint
        responses.append("yes" if config.get("prettier", True) else "no")   # Prettier

        # For PWA projects, add additional prompt
        if config["project_type"] == "pwa":
            responses.append("yes")  # PWA support

        # Run create-vue with responses
        try:
            process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=Path.cwd()
            )

            # Send responses to prompts
            input_text = "\n".join(responses) + "\n"
            stdout, stderr = process.communicate(input=input_text, timeout=120)

            if process.returncode == 0:
                print("✅ Vue 3 project created successfully!")
                return True
            else:
                print(f"❌ Failed to create Vue 3 project: {stderr}")
                return False

        except subprocess.TimeoutExpired:
            print("❌ Project creation timed out")
            process.kill()
            return False
        except Exception as e:
            print(f"❌ Error creating project: {e}")
            return False

    def install_dependencies(self, config: Dict[str, Any], package_manager: str) -> bool:
        """Install project dependencies."""
        print("📦 Installing dependencies...")

        project_path = Path(config["project_name"])

        try:
            # Change to project directory
            os.chdir(project_path)

            # Install dependencies
            success, stdout, stderr = run_command([package_manager, "install"], timeout=300)
            if not success:
                print(f"❌ Failed to install dependencies: {stderr}")
                return False

            # Add CSS framework if specified
            if config.get("css_framework") and config["css_framework"] != "none":
                print(f"🎨 Installing {config['css_framework']}...")
                if config["css_framework"] == "tailwindcss":
                    success, _, error = run_command([
                        package_manager, "add", "-D", "tailwindcss", "postcss", "autoprefixer"
                    ])
                    if success:
                        run_command(["npx", "tailwindcss", "init", "-p"])
                    else:
                        print(f"⚠️  Failed to install Tailwind CSS: {error}")

                elif config["css_framework"] == "bootstrap":
                    success, _, error = run_command([
                        package_manager, "add", "bootstrap", "@popperjs/core"
                    ])
                    if not success:
                        print(f"⚠️  Failed to install Bootstrap: {error}")

                elif config["css_framework"] == "bulma":
                    success, _, error = run_command([package_manager, "add", "bulma"])
                    if not success:
                        print(f"⚠️  Failed to install Bulma: {error}")

            print("✅ Dependencies installed successfully!")
            return True

        except Exception as e:
            print(f"❌ Error installing dependencies: {e}")
            return False
        finally:
            # Return to original directory
            os.chdir("..")

    def configure_project(self, config: Dict[str, Any]) -> bool:
        """Configure project settings and files."""
        print("⚙️  Configuring project...")

        project_path = Path(config["project_name"])

        try:
            # Update package.json with custom information
            package_json_path = project_path / "package.json"
            if package_json_path.exists():
                with open(package_json_path, 'r') as f:
                    package_data = json.load(f)

                # Update custom fields
                package_data["description"] = config.get("project_description", package_data["description"])
                package_data["author"] = config.get("author", "")
                package_data["license"] = config.get("license", "MIT")

                with open(package_json_path, 'w') as f:
                    json.dump(package_data, f, indent=2)

                print("  📝 Updated package.json")

            # Create .env file
            env_content = f"""# Environment variables for {config['project_name']}

VITE_APP_TITLE={config.get('project_name', 'Vue App')}
VITE_APP_VERSION=0.1.0
VITE_API_BASE_URL=http://localhost:3000/api
"""

            env_path = project_path / ".env"
            with open(env_path, 'w') as f:
                f.write(env_content)

            print("  📝 Created .env file")

            # Update README.md
            readme_path = project_path / "README.md"
            if readme_path.exists():
                # Build helper variables
                router_info = ', Vue Router' if config.get('router') else ''
                pinia_info = ', Pinia' if config.get('pinia') else ''
                css_framework_line = f"- {config['css_framework']}" if config.get('css_framework') and config['css_framework'] != 'none' else ''

                readme_content = f"""# {config['project_name']}

{config.get('project_description', 'A Vue 3 application')}

## Recommended IDE Setup

[VSCode](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur) + [TypeScript Vue Plugin (Volar)](https://marketplace.visualstudio.com/items?itemName=Vue.vscode-typescript-vue-plugin).

## Project Setup

```sh
{suggest_package_manager()} install
```

## Development Server

```sh
{suggest_package_manager()} dev
```

## Build for Production

```sh
{suggest_package_manager()} build
```

## Run Tests

```sh
{suggest_package_manager()} test
```

## Lint and Format

```sh
{suggest_package_manager()} lint
{suggest_package_manager()} format
```

## Project Type

This is a **{config['project_type'].upper()}** project built with:
- Vue 3 with Composition API
- TypeScript{router_info}{pinia_info}
- Vite for build tooling
{css_framework_line}
"""

                with open(readme_path, 'w') as f:
                    f.write(readme_content)

                print("  📝 Updated README.md")

            print("✅ Project configured successfully!")
            return True

        except Exception as e:
            print(f"❌ Error configuring project: {e}")
            return False

    def generate_project(self, config: Dict[str, Any]) -> bool:
        """Generate complete Vue 3 project."""
        print(f"🎯 Starting Vue 3 project generation...")
        print(f"  Project: {config['project_name']}")
        print(f"  Type: {config['project_type']}")
        print(f"  CSS Framework: {config.get('css_framework', 'none')}")
        print()

        # Check prerequisites
        if not self.check_prerequisites():
            return False

        # Setup environment
        package_manager = self.setup_environment()
        if not package_manager:
            return False

        # Create Vue project
        if not self.create_vue_project(config, package_manager):
            return False

        # Install dependencies
        if not self.install_dependencies(config, package_manager):
            return False

        # Configure project
        if not self.configure_project(config):
            return False

        print("\n🎉 Vue 3 project generated successfully!")
        print(f"📁 Project location: {Path(config['project_name']).absolute()}")
        print(f"🚀 Get started with: cd {config['project_name']} && {package_manager} dev")

        return True

    def interactive_mode(self) -> Dict[str, Any]:
        """Run interactive configuration mode."""
        print("🎯 Vue 3 Project Generator - Interactive Mode")
        print("=" * 50)

        config = self.default_config.copy()

        # Project name
        project_name = input(f"Project name [{config['project_name']}: ").strip()
        if project_name:
            config["project_name"] = project_name

        # Project description
        description = input(f"Project description [{config['project_description']}: ").strip()
        if description:
            config["project_description"] = description

        # Project type
        print(f"\nProject types:")
        for i, pt in enumerate(self.project_types, 1):
            print(f"  {i}. {pt}")

        while True:
            try:
                choice = input(f"Select project type [1-{len(self.project_types)}, default={self.project_types.index(config['project_type']) + 1}]: ").strip()
                if not choice:
                    break
                choice = int(choice)
                if 1 <= choice <= len(self.project_types):
                    config["project_type"] = self.project_types[choice - 1]
                    break
                else:
                    print("  Invalid choice. Please try again.")
            except ValueError:
                print("  Please enter a number.")

        # CSS Framework
        print(f"\nCSS frameworks:")
        for i, cf in enumerate(self.css_frameworks, 1):
            print(f"  {i}. {cf}")

        while True:
            try:
                choice = input(f"Select CSS framework [1-{len(self.css_frameworks)}, default={self.css_frameworks.index(config['css_framework']) + 1}]: ").strip()
                if not choice:
                    break
                choice = int(choice)
                if 1 <= choice <= len(self.css_frameworks):
                    config["css_framework"] = self.css_frameworks[choice - 1]
                    break
                else:
                    print("  Invalid choice. Please try again.")
            except ValueError:
                print("  Please enter a number.")

        # Features (yes/no)
        features = [
            ("typescript", "Add TypeScript?"),
            ("router", "Add Vue Router?"),
            ("pinia", "Add Pinia for state management?"),
            ("vitest", "Add Vitest for testing?"),
            ("eslint", "Add ESLint for code linting?"),
            ("prettier", "Add Prettier for code formatting?")
        ]

        for feature, question in features:
            response = input(f"{question} [Y/n]: ").strip().lower()
            config[feature] = not response.startswith('n')

        # Author
        author = input("Author name: ").strip()
        if author:
            config["author"] = author

        return config


def main():
    """Main function to run the Vue 3 project generator."""
    parser = argparse.ArgumentParser(
        description="Generate Vue 3 projects with modern tooling",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                                    # Interactive mode
  %(prog)s --project-name my-app              # Quick project creation
  %(prog)s my-app --project-type pwa          # PWA project
  %(prog)s --list-types                       # List available project types
        """
    )

    parser.add_argument(
        "project_name",
        nargs="?",
        help="Name of the project to create"
    )

    parser.add_argument(
        "--project-type",
        choices=["spa", "pwa", "component-lib", "admin-dashboard"],
        default="spa",
        help="Type of project to create (default: spa)"
    )

    parser.add_argument(
        "--css-framework",
        choices=["none", "tailwindcss", "bootstrap", "bulma"],
        default="none",
        help="CSS framework to use (default: none)"
    )

    parser.add_argument(
        "--typescript",
        action="store_true",
        default=True,
        help="Add TypeScript support (default: enabled)"
    )

    parser.add_argument(
        "--no-typescript",
        dest="typescript",
        action="store_false",
        help="Disable TypeScript support"
    )

    parser.add_argument(
        "--router",
        action="store_true",
        default=True,
        help="Add Vue Router (default: enabled)"
    )

    parser.add_argument(
        "--no-router",
        dest="router",
        action="store_false",
        help="Disable Vue Router"
    )

    parser.add_argument(
        "--pinia",
        action="store_true",
        default=True,
        help="Add Pinia state management (default: enabled)"
    )

    parser.add_argument(
        "--no-pinia",
        dest="pinia",
        action="store_false",
        help="Disable Pinia state management"
    )

    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Run in interactive mode"
    )

    parser.add_argument(
        "--list-types",
        action="store_true",
        help="List available project types and exit"
    )

    args = parser.parse_args()

    # List project types and exit
    if args.list_types:
        generator = Vue3ProjectGenerator()
        print("Available project types:")
        for pt in generator.project_types:
            print(f"  - {pt}")
        return

    # Create generator instance
    generator = Vue3ProjectGenerator()

    # Interactive mode
    if args.interactive or not args.project_name:
        config = generator.interactive_mode()
    else:
        # Command line mode
        config = generator.default_config.copy()
        config.update({
            "project_name": args.project_name,
            "project_type": args.project_type,
            "css_framework": args.css_framework,
            "typescript": args.typescript,
            "router": args.router,
            "pinia": args.pinia
        })

    # Generate project
    success = generator.generate_project(config)

    if success:
        print("\n✨ Happy coding! ✨")
    else:
        print("\n❌ Project generation failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()