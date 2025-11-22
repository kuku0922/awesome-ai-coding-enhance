#!/usr/bin/env python3
"""
Go dependency management utilities.

This module provides functions to manage Go module dependencies using go mod commands,
avoiding direct editing of go.mod and go.sum files.
"""

import subprocess
import os
from pathlib import Path
from typing import Dict, List, Optional, Set
from dataclasses import dataclass
import json

from query_versions import get_gin_framework_info, get_common_dependency_versions, get_go_version_info


@dataclass
class Dependency:
    """Represents a Go dependency."""
    name: str
    module_path: str
    version: Optional[str] = None
    import_path: Optional[str] = None
    description: str = ""
    category: str = "general"  # web, database, auth, logging, testing, etc.


class GoDependencyManager:
    """Manages Go project dependencies using go mod commands."""

    def __init__(self, project_path: str):
        """
        Initialize dependency manager.

        Args:
            project_path: Path to the Go project
        """
        self.project_path = Path(project_path)
        self.go_mod_path = self.project_path / "go.mod"
        self.go_sum_path = self.project_path / "go.sum"

    def _run_go_command(self, command: List[str], check: bool = True) -> subprocess.CompletedProcess:
        """
        Run a Go command in the project directory.

        Args:
            command: Command to run (as list)
            check: Whether to check return code

        Returns:
            CompletedProcess object
        """
        try:
            env = os.environ.copy()
            # Ensure GOPATH and GOCACHE are set for consistent behavior
            env.setdefault("GOPATH", os.path.expanduser("~/go"))
            env.setdefault("GOCACHE", os.path.expanduser("~/Library/Caches/go-build"))

            result = subprocess.run(
                ["go"] + command,
                cwd=self.project_path,
                capture_output=True,
                text=True,
                env=env,
                check=check
            )
            return result
        except subprocess.CalledProcessError as e:
            print(f"Go command failed: {' '.join(command)}")
            print(f"Error: {e.stderr}")
            raise
        except FileNotFoundError:
            raise RuntimeError("Go is not installed or not in PATH")

    def init_module(self, module_path: str) -> None:
        """
        Initialize a new Go module.

        Args:
            module_path: Module path (e.g., github.com/user/project)
        """
        if self.go_mod_path.exists():
            print(f"go.mod already exists in {self.project_path}")
            return

        print(f"Initializing Go module: {module_path}")
        result = self._run_go_command(["mod", "init", module_path])
        print(f"✅ Go module initialized: {module_path}")

    def add_dependency(self, module_path: str, version: Optional[str] = None) -> None:
        """
        Add a dependency to the project.

        Args:
            module_path: Module path to add
            version: Specific version (optional)
        """
        cmd = ["get", module_path]
        if version:
            if not version.startswith('v'):
                version = 'v' + version
            cmd[-1] = f"{module_path}@{version}"

        print(f"Adding dependency: {cmd[-1]}")
        result = self._run_go_command(cmd)
        print(f"✅ Added: {module_path}")

    def add_dev_dependencies(self, dependencies: List[str]) -> None:
        """
        Add development dependencies.

        Args:
            dependencies: List of module paths to add for development
        """
        for dep in dependencies:
            self.add_dependency(dep)

    def remove_dependency(self, module_path: str) -> None:
        """
        Remove a dependency from the project.

        Args:
            module_path: Module path to remove
        """
        print(f"Removing dependency: {module_path}")
        try:
            result = self._run_go_command(["mod", "edit", "-droprequire", module_path], check=False)
            # Clean up unused dependencies
            self._run_go_command(["mod", "tidy"])
            print(f"✅ Removed: {module_path}")
        except Exception as e:
            print(f"Failed to remove {module_path}: {e}")

    def update_dependencies(self, targets: Optional[List[str]] = None) -> None:
        """
        Update dependencies.

        Args:
            targets: Specific dependencies to update (all if None)
        """
        if targets:
            for target in targets:
                print(f"Updating: {target}")
                self._run_go_command(["get", "-u", target])
        else:
            print("Updating all dependencies...")
            self._run_go_command(["get", "-u", "./..."])

        self._run_go_command(["mod", "tidy"])
        print("✅ Dependencies updated")

    def tidy_dependencies(self) -> None:
        """Clean up and organize dependencies."""
        print("Tidying dependencies...")
        result = self._run_go_command(["mod", "tidy"])
        print("✅ Dependencies tidied")

    def verify_dependencies(self) -> bool:
        """
        Verify that dependencies are consistent.

        Returns:
            True if verification passes
        """
        try:
            print("Verifying dependencies...")
            result = self._run_go_command(["mod", "verify"])
            print("✅ Dependencies verified")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Dependency verification failed: {e}")
            return False

    def download_dependencies(self) -> None:
        """Download all dependencies without installing them."""
        print("Downloading dependencies...")
        result = self._run_go_command(["mod", "download"])
        print("✅ Dependencies downloaded")

    def list_dependencies(self) -> Dict[str, str]:
        """
        List all direct dependencies.

        Returns:
            Dictionary mapping module paths to versions
        """
        result = self._run_go_command(["list", "-m", "-versions", "all"])
        output = result.stdout

        dependencies = {}
        for line in output.split('\n'):
            if line and not line.startswith('#'):
                parts = line.split()
                if len(parts) >= 2:
                    module_path = parts[0]
                    # The second line contains versions, first is usually the latest
                    dependencies[module_path] = parts[1] if len(parts) > 1 else "unknown"

        return dependencies

    def get_dependency_info(self, module_path: str) -> Dict[str, str]:
        """
        Get detailed information about a specific dependency.

        Args:
            module_path: Module path to query

        Returns:
            Dictionary with dependency information
        """
        try:
            result = self._run_go_command(["list", "-m", "-versions", module_path])
            lines = result.stdout.strip().split('\n')

            if len(lines) == 0:
                return {"error": "Module not found"}

            info = {"module_path": module_path}

            # First line contains module info
            first_line = lines[0]
            if ' ' in first_line:
                parts = first_line.split()
                info["current_version"] = parts[1] if len(parts) > 1 else "unknown"

            # Second line contains available versions
            if len(lines) > 1:
                info["available_versions"] = lines[1]

            return info
        except Exception as e:
            return {"error": str(e)}

    def setup_gin_project(self, project_config: Dict[str, any]) -> None:
        """
        Set up a complete Gin project with standard dependencies.

        Args:
            project_config: Dictionary containing project configuration
        """
        # Initialize module if needed
        module_path = project_config.get("module_path")
        if module_path:
            self.init_module(module_path)

        # Get Gin framework info
        gin_info = get_gin_framework_info()
        print(f"Setting up Gin v{gin_info['version']}...")

        # Always add Gin framework
        self.add_dependency(gin_info["module_path"])

        # Add dependencies based on project configuration
        deps_to_add = self._get_dependencies_for_config(project_config)

        for dep in deps_to_add:
            self.add_dependency(dep.module_path, dep.version)

        # Clean up
        self.tidy_dependencies()
        self.download_dependencies()

        print("✅ Gin project dependencies set up successfully!")

    def _get_dependencies_for_config(self, config: Dict[str, any]) -> List[Dependency]:
        """
        Get dependencies list based on project configuration.

        Args:
            config: Project configuration dictionary

        Returns:
            List of Dependency objects
        """
        dependencies = []
        common_deps = get_common_dependency_versions()

        # Database dependencies
        if config.get("database", {}).get("enabled", False):
            db_type = config["database"].get("type", "postgres")
            if db_type == "postgres":
                deps = [
                    Dependency("gorm", "gorm.io/gorm"),
                    Dependency("postgres", "gorm.io/driver/postgres")
                ]
            elif db_type == "mysql":
                deps = [
                    Dependency("gorm", "gorm.io/gorm"),
                    Dependency("mysql", "gorm.io/driver/mysql")
                ]
            elif db_type == "sqlite":
                deps = [
                    Dependency("gorm", "gorm.io/gorm"),
                    Dependency("sqlite", "gorm.io/driver/sqlite")
                ]
            else:
                deps = [Dependency("gorm", "gorm.io/gorm")]
            dependencies.extend(deps)

        # Authentication/Authorization
        if config.get("auth", {}).get("enabled", False):
            dependencies.append(
                Dependency("jwt", "github.com/golang-jwt/jwt")
            )

        # Configuration management
        if config.get("config", {}).get("type", "yaml") in ["yaml", "yml"]:
            dependencies.append(
                Dependency("viper", "github.com/spf13/viper")
            )

        # Logging
        logging_config = config.get("logging", {}).get("library", "logrus")
        if logging_config == "logrus":
            dependencies.append(
                Dependency("logrus", "github.com/sirupsen/logrus")
            )
        elif logging_config == "zap":
            dependencies.append(
                Dependency("zap", "go.uber.org/zap")
            )

        # Validation
        if config.get("validation", {}).get("enabled", True):
            dependencies.append(
                Dependency("validator", "github.com/go-playground/validator")
            )

        # CORS
        if config.get("cors", {}).get("enabled", True):
            dependencies.append(
                Dependency("cors", "github.com/gin-contrib/cors")
            )

        # API Documentation
        if config.get("docs", {}).get("type", "swagger") == "swagger":
            dependencies.extend([
                Dependency("swaggo", "github.com/swaggo/swag"),
                Dependency("swaggo-gin", "github.com/swaggo/gin-swagger"),
                Dependency("swaggo-files", "github.com/swaggo/files")
            ])

        # Testing
        if config.get("testing", {}).get("enhanced", False):
            dependencies.append(
                Dependency("testify", "github.com/stretchr/testify")
            )

        # Metrics (for microservices)
        if config.get("metrics", {}).get("enabled", False):
            dependencies.extend([
                Dependency("prometheus", "github.com/prometheus/client_golang"),
                Dependency("gin-prometheus", "github.com/zsais/go-gin-prometheus")
            ])

        # Rate limiting
        if config.get("rate_limiting", {}).get("enabled", False):
            dependencies.extend([
                Dependency("goredis", "github.com/go-redis/redis/v8"),
                Dependency("rate-limit", "golang.org/x/time/rate")
            ])

        # Cache
        if config.get("cache", {}).get("enabled", False):
            cache_type = config["cache"].get("type", "redis")
            if cache_type == "redis":
                dependencies.append(
                    Dependency("goredis", "github.com/go-redis/redis/v8")
                )

        # Message Queue
        if config.get("message_queue", {}).get("enabled", False):
            mq_type = config["message_queue"].get("type", "rabbitmq")
            if mq_type == "rabbitmq":
                dependencies.append(
                    Dependency("streadway-amqp", "github.com/streadway/amqp")
                )
            elif mq_type == "nats":
                dependencies.append(
                    Dependency("nats", "github.com/nats-io/nats.go")
                )

        # gRPC (for microservices)
        if config.get("grpc", {}).get("enabled", False):
            dependencies.extend([
                Dependency("grpc", "google.golang.org/grpc"),
                Dependency("grpc-gateway", "github.com/grpc-ecosystem/grpc-gateway/v2"),
                Dependency("protoc-gen-go", "google.golang.org/protobuf/cmd/protoc-gen-go"),
                Dependency("protoc-gen-go-grpc", "google.golang.org/grpc/cmd/protoc-gen-go-grpc")
            ])

        # Add version information from common dependencies
        for dep in dependencies:
            if dep.module_path in common_deps:
                dep.version = common_deps[dep.module_path].get("version")

        return dependencies

    def generate_go_mod_content(self, module_path: str, config: Dict[str, any]) -> str:
        """
        Generate go.mod file content based on configuration.

        Args:
            module_path: Go module path
            config: Project configuration

        Returns:
            go.mod file content as string
        """
        go_info = get_go_version_info()
        gin_info = get_gin_framework_info()

        lines = [
            f"module {module_path}",
            "",
            f"go {go_info['version']}",
            "",
            "require (",
            f"\t{gin_info['module_path']} v{gin_info['version']}"
        ]

        # Get dependencies
        dependencies = self._get_dependencies_for_config(config)
        for dep in dependencies:
            if dep.version and dep.version != "latest":
                lines.append(f"\t{dep.module_path} v{dep.version}")
            else:
                lines.append(f"\t{dep.module_path}")

        lines.extend([
            ")",
            ""
        ])

        return "\n".join(lines)

    def create_go_mod_from_config(self, module_path: str, config: Dict[str, any]) -> None:
        """
        Create go.mod file from configuration.

        Args:
            module_path: Go module path
            config: Project configuration
        """
        content = self.generate_go_mod_content(module_path, config)
        self.go_mod_path.write_text(content)
        print(f"✅ Created go.mod with {len(self._get_dependencies_for_config(config))} dependencies")

    def install_go_tools(self) -> None:
        """Install common Go development tools."""
        tools = [
            "github.com/air-verse/air@latest",              # Live reload
            "github.com/swaggo/swag/cmd/swag@latest",       # Swagger generation
            "github.com/golangci/golangci-lint/cmd/golangci-lint@latest",  # Linting
            "golang.org/x/tools/cmd/goimports@latest",     # Import formatting
            "github.com/golang/mock/mockgen@latest",       # Mock generation
            "google.golang.org/protobuf/cmd/protoc-gen-go@latest",  # Protocol buffers
            "google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest",  # gRPC
        ]

        print("Installing Go development tools...")
        for tool in tools:
            try:
                print(f"Installing {tool}...")
                self._run_go_command(["install", tool], check=False)
                print(f"✅ Installed {tool}")
            except Exception as e:
                print(f"❌ Failed to install {tool}: {e}")

    def setup_project_deps(self, module_path: str, config: Dict[str, any]) -> None:
        """
        Complete setup of project dependencies.

        Args:
            module_path: Go module path
            config: Project configuration
        """
        print(f"🚀 Setting up dependencies for {module_path}")

        # Initialize module
        self.init_module(module_path)

        # Create go.mod from config
        self.create_go_mod_from_config(module_path, config)

        # Install dependencies
        self.setup_gin_project(config)

        # Verify setup
        if self.verify_dependencies():
            print("✅ All dependencies installed and verified!")
        else:
            print("⚠️  Dependencies installed but verification failed")

        # Install development tools
        self.install_go_tools()

        print("🎉 Project dependency setup complete!")


def main():
    """Example usage of Go dependency manager."""
    import sys
    import json

    if len(sys.argv) < 2:
        print("Usage: python setup_dependencies.py <project_path> [config_json]")
        sys.exit(1)

    project_path = sys.argv[1]

    # Default configuration
    default_config = {
        "database": {"enabled": True, "type": "postgres"},
        "auth": {"enabled": True},
        "config": {"type": "yaml"},
        "logging": {"library": "logrus"},
        "validation": {"enabled": True},
        "cors": {"enabled": True},
        "docs": {"type": "swagger"},
        "testing": {"enhanced": True}
    }

    # Load config from command line if provided
    config = default_config
    if len(sys.argv) > 2:
        try:
            config = json.loads(sys.argv[2])
        except json.JSONDecodeError:
            print("Invalid JSON config, using defaults")

    # Get module path
    module_path = config.get("module_path", f"github.com/username/{Path(project_path).name}")

    # Setup dependencies
    manager = GoDependencyManager(project_path)
    manager.setup_project_deps(module_path, config)


if __name__ == "__main__":
    main()