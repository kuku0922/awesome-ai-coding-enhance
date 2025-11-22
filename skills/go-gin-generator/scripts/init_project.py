#!/usr/bin/env python3
"""
Main project initialization script for Go Gin project generator.

This script orchestrates the complete creation of a Go Gin web application
with all necessary directories, files, dependencies, and configurations.
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, Any, Optional
import subprocess
import shutil

from create_structure import GoProjectStructure
from setup_dependencies import GoDependencyManager
from query_versions import get_gin_framework_info, get_go_version_info


class GoGinProjectGenerator:
    """Main class for generating Go Gin projects."""

    def __init__(self):
        self.project_types = ["api", "web", "microservice", "grpc"]
        self.default_config = self._get_default_config()

    def _get_default_config(self) -> Dict[str, Any]:
        """Get default project configuration."""
        return {
            "module_path": "",  # Will be set based on project name
            "project_type": "api",
            "database": {
                "enabled": True,
                "type": "postgres",
                "connection_string": ""
            },
            "auth": {
                "enabled": True,
                "type": "jwt",
                "secret": ""
            },
            "config": {
                "type": "yaml",
                "env_file": True
            },
            "logging": {
                "library": "logrus",
                "level": "info",
                "format": "json"
            },
            "validation": {
                "enabled": True,
                "library": "go-playground"
            },
            "cors": {
                "enabled": True,
                "allowed_origins": ["*"]
            },
            "docs": {
                "type": "swagger",
                "enabled": True
            },
            "testing": {
                "enhanced": True,
                "coverage": True
            },
            "docker": {
                "enabled": True,
                "multi_stage": True
            },
            "metrics": {
                "enabled": False,
                "prometheus": False
            },
            "grpc": {
                "enabled": False,
                "gateway": True
            },
            "cache": {
                "enabled": False,
                "type": "redis"
            },
            "message_queue": {
                "enabled": False,
                "type": "rabbitmq"
            },
            "rate_limiting": {
                "enabled": False,
                "rate": "100/minute"
            }
        }

    def get_user_input(self) -> Dict[str, Any]:
        """
        Get project configuration from user input.

        Returns:
            Dictionary with project configuration
        """
        print("🚀 Go Gin Project Generator")
        print("=" * 50)

        # Project name
        project_name = input("Project name: ").strip()
        if not project_name:
            print("❌ Project name is required")
            sys.exit(1)

        # Project type
        print(f"\nProject types: {', '.join(self.project_types)}")
        project_type = input("Project type (api): ").strip().lower()
        if not project_type:
            project_type = "api"
        if project_type not in self.project_types:
            print(f"❌ Invalid project type. Must be one of: {', '.join(self.project_types)}")
            sys.exit(1)

        # Module path
        default_module_path = f"github.com/username/{project_name}"
        module_path = input(f"Go module path ({default_module_path}): ").strip()
        if not module_path:
            module_path = default_module_path

        # Configuration
        config = self.default_config.copy()
        config["project_name"] = project_name
        config["module_path"] = module_path
        config["project_type"] = project_type

        # Database
        print("\n📊 Database Configuration")
        db_enabled = input("Enable database? (Y/n): ").strip().lower()
        if db_enabled != 'n':
            config["database"]["enabled"] = True
            db_type = input("Database type (postgres/mysql/sqlite) [postgres]: ").strip().lower()
            if db_type in ["mysql", "sqlite"]:
                config["database"]["type"] = db_type
        else:
            config["database"]["enabled"] = False

        # Authentication
        print("\n🔐 Authentication")
        auth_enabled = input("Enable authentication? (Y/n): ").strip().lower()
        if auth_enabled != 'n':
            config["auth"]["enabled"] = True
        else:
            config["auth"]["enabled"] = False

        # Advanced options
        print("\n⚙️  Advanced Options")
        advanced = input("Configure advanced options? (y/N): ").strip().lower()
        if advanced == 'y':
            self._configure_advanced_options(config)

        return config

    def _configure_advanced_options(self, config: Dict[str, Any]) -> None:
        """Configure advanced project options."""
        # Logging
        logging_lib = input("Logging library (logrus/zap) [logrus]: ").strip().lower()
        if logging_lib == "zap":
            config["logging"]["library"] = "zap"

        # Documentation
        docs_type = input("Documentation type (swagger/none) [swagger]: ").strip().lower()
        if docs_type == "none":
            config["docs"]["enabled"] = False

        # Testing
        testing = input("Enhanced testing setup? (Y/n): ").strip().lower()
        if testing == 'n':
            config["testing"]["enhanced"] = False

        # Metrics (for microservices)
        if config["project_type"] == "microservice":
            metrics = input("Enable metrics? (Y/n): ").strip().lower()
            if metrics != 'n':
                config["metrics"]["enabled"] = True

        # gRPC (for gRPC projects)
        if config["project_type"] == "grpc":
            config["grpc"]["enabled"] = True

    def generate_project(self, config: Dict[str, Any], output_path: str = ".") -> str:
        """
        Generate a complete Go Gin project.

        Args:
            config: Project configuration dictionary
            output_path: Path where project should be created

        Returns:
            Path to generated project
        """
        project_name = config["project_name"]
        project_type = config["project_type"]
        module_path = config["module_path"]

        print(f"\n🏗️  Generating {project_type} project: {project_name}")
        print(f"📦 Module: {module_path}")

        # Create project structure
        print("\n📁 Creating project structure...")
        structure_creator = GoProjectStructure(project_name, output_path)
        structure_creator.set_module_path(module_path)

        # Create directories and files
        structure_creator.create_directory_structure(project_type)
        structure_creator.create_main_file(project_type)
        structure_creator.create_config_files(project_type)
        structure_creator.create_basic_handlers(project_type)
        structure_creator.create_basic_middleware()
        structure_creator.create_docker_files(project_type)
        structure_creator.create_gitignore()
        structure_creator.create_makefile()
        structure_creator.create_readme(project_type)

        project_path = structure_creator.project_path
        print(f"✅ Project structure created at: {project_path}")

        # Set up dependencies
        print("\n📚 Setting up dependencies...")
        dep_manager = GoDependencyManager(str(project_path))
        dep_manager.setup_project_deps(module_path, config)

        # Additional setup based on project type
        if project_type == "web":
            self._setup_web_project(project_path)
        elif project_type == "microservice":
            self._setup_microservice_project(project_path)
        elif project_type == "grpc":
            self._setup_grpc_project(project_path)

        # Create templates if needed
        if project_type == "web":
            self._create_web_templates(project_path)

        # Post-generation steps
        print("\n🔄 Post-generation setup...")
        self._run_post_generation_steps(project_path)

        print(f"\n🎉 Project '{project_name}' generated successfully!")
        print(f"📍 Location: {project_path}")

        return str(project_path)

    def _setup_web_project(self, project_path: Path) -> None:
        """Set up web project specific files."""
        # Create basic HTML templates
        templates_dir = project_path / "web" / "templates"
        templates_dir.mkdir(exist_ok=True)

        # Basic layout template
        layout_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{.title}}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="/static/css/style.css">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="/">{{.title}}</a>
            <div class="navbar-nav">
                <a class="nav-link" href="/">Home</a>
                <a class="nav-link" href="/about">About</a>
                <a class="nav-link" href="/api/v1/examples">API</a>
            </div>
        </div>
    </nav>

    <main class="container mt-4">
        {{.LayoutContent}}
    </main>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script src="/static/js/app.js"></script>
</body>
</html>
'''

        layout_file = templates_dir / "layout.html"
        layout_file.write_text(layout_content)

        # Index template
        index_content = '''{{define "content"}}
<div class="row">
    <div class="col-md-8">
        <h1>Welcome to {{.title}}</h1>
        <p class="lead">A modern Go web application built with Gin framework.</p>

        <div class="row mt-4">
            <div class="col-md-4">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">🚀 Fast</h5>
                        <p class="card-text">Built with Gin for maximum performance.</p>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">🏗️  Clean</h5>
                        <p class="card-text">Follows Go best practices and clean architecture.</p>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">🔧 Ready</h5>
                        <p class="card-text">Production-ready with Docker and CI/CD.</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div class="col-md-4">
        <div class="card">
            <div class="card-header">
                <h5>API Endpoints</h5>
            </div>
            <div class="card-body">
                <ul class="list-group list-group-flush">
                    <li class="list-group-item">
                        <strong>GET</strong> /api/v1/health
                    </li>
                    <li class="list-group-item">
                        <strong>GET</strong> /api/v1/examples
                    </li>
                    <li class="list-group-item">
                        <strong>POST</strong> /api/v1/examples
                    </li>
                </ul>
            </div>
        </div>
    </div>
</div>
{{end}}
'''

        index_file = templates_dir / "index.html"
        index_file.write_text(index_content)

        # About template
        about_content = '''{{define "content"}}
<div class="row">
    <div class="col-md-8">
        <h1>About {{.title}}</h1>
        <p>This is a modern Go web application demonstrating:</p>
        <ul>
            <li>Gin HTTP framework</li>
            <li>Clean architecture patterns</li>
            <li>Configuration management</li>
            <li>Structured logging</li>
            <li>Docker containerization</li>
            <li>API documentation</li>
        </ul>
    </div>
</div>
{{end}}
'''

        about_file = templates_dir / "about.html"
        about_file.write_text(about_content)

    def _setup_microservice_project(self, project_path: Path) -> None:
        """Set up microservice specific files."""
        # Create health check implementation
        health_service = '''package health

import (
	"context"
	"time"

	"github.com/sirupsen/logrus"
)

type Checker interface {
	CheckHealth(ctx context.Context) error
}

type Service struct {
	checkers map[string]Checker
	logger   *logrus.Logger
}

func NewChecker() *Service {
	logger := logrus.New()
	return &Service{
		checkers: make(map[string]Checker),
		logger:   logger,
	}
}

func (s *Service) AddChecker(name string, checker Checker) {
	s.checkers[name] = checker
}

func (s *Service) CheckHealth(ctx context.Context) map[string]string {
	results := make(map[string]string)

	// Check each component
	for name, checker := range s.checkers {
		select {
		case <-ctx.Done():
			results[name] = "timeout"
		default:
			if err := checker.CheckHealth(ctx); err != nil {
				s.logger.WithError(err).Warnf("Health check failed for %s", name)
				results[name] = "unhealthy"
			} else {
				results[name] = "healthy"
			}
		}
	}

	return results
}

type DatabaseChecker struct {
	// Add database connection here
}

func (dc *DatabaseChecker) CheckHealth(ctx context.Context) error {
	// Implement database health check
	// Example: ping database
	return nil
}

type RedisChecker struct {
	// Add Redis connection here
}

func (rc *RedisChecker) CheckHealth(ctx context.Context) error {
	// Implement Redis health check
	// Example: ping Redis
	return nil
}
'''

        health_file = project_path / "internal" / "health" / "service.go"
        health_file.write_text(health_service)

    def _setup_grpc_project(self, project_path: Path) -> None:
        """Set up gRPC project specific files."""
        # Create proto directory structure
        proto_dir = project_path / "proto"
        proto_dir.mkdir(exist_ok=True)

        # Basic proto file
        proto_content = '''syntax = "proto3";

package example;
option go_package = "github.com/username/project/proto/example";

service ExampleService {
  rpc GetExample(GetExampleRequest) returns (GetExampleResponse);
  rpc ListExamples(ListExamplesRequest) returns (ListExamplesResponse);
}

message Example {
  int32 id = 1;
  string name = 2;
  string value = 3;
}

message GetExampleRequest {
  int32 id = 1;
}

message GetExampleResponse {
  Example example = 1;
}

message ListExamplesRequest {
  int32 page = 1;
  int32 limit = 2;
}

message ListExamplesResponse {
  repeated Example examples = 1;
  int32 total = 2;
}
'''

        proto_file = proto_dir / "example.proto"
        proto_file.write_text(proto_content)

        # Create Makefile target for proto generation
        makefile_path = project_path / "Makefile"
        if makefile_path.exists():
            with open(makefile_path, 'a') as f:
                f.write('''
# Protocol Buffers
proto-gen: ## Generate protocol buffer files
	protoc --go_out=. --go_opt=paths=source_relative \\
		--go-grpc_out=. --go-grpc_opt=paths=source_relative \\
		proto/*.proto

.PHONY: proto-gen
''')

    def _create_web_templates(self, project_path: Path) -> None:
        """Create web templates and static files."""
        # Create static files
        static_dir = project_path / "web" / "static"
        css_dir = static_dir / "css"
        js_dir = static_dir / "js"

        css_dir.mkdir(exist_ok=True)
        js_dir.mkdir(exist_ok=True)

        # Basic CSS
        css_content = '''
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background-color: #f8f9fa;
}

.navbar-brand {
    font-weight: bold;
}

.card {
    box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
    border: 1px solid rgba(0, 0, 0, 0.125);
}

.card-header {
    background-color: #f8f9fa;
    border-bottom: 1px solid rgba(0, 0, 0, 0.125);
    font-weight: 600;
}

.list-group-item {
    border: 1px solid rgba(0, 0, 0, 0.125);
}

.jumbotron {
    background-color: #e9ecef;
    padding: 2rem 1rem;
    border-radius: 0.3rem;
}
'''

        css_file = css_dir / "style.css"
        css_file.write_text(css_content)

        # Basic JavaScript
        js_content = '''
// Basic JavaScript functionality
document.addEventListener('DOMContentLoaded', function() {
    console.log('Application loaded');

    // Add any client-side functionality here
    fetch('/api/v1/health')
        .then(response => response.json())
        .then(data => {
            console.log('Health check:', data);
        })
        .catch(error => {
            console.error('Health check failed:', error);
        });
});
'''

        js_file = js_dir / "app.js"
        js_file.write_text(js_content)

    def _run_post_generation_steps(self, project_path: Path) -> None:
        """Run post-generation setup steps."""
        try:
            # Initialize git repository
            subprocess.run(["git", "init"], cwd=project_path, capture_output=True, check=True)
            print("✅ Git repository initialized")

            # Create initial commit
            subprocess.run(["git", "add", "."], cwd=project_path, capture_output=True, check=True)
            subprocess.run(["git", "commit", "-m", "Initial commit: Go Gin project generated"],
                         cwd=project_path, capture_output=True, check=True)
            print("✅ Initial git commit created")

        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            print(f"⚠️  Git setup failed: {e}")

    def load_config_from_file(self, config_file: str) -> Dict[str, Any]:
        """
        Load project configuration from JSON file.

        Args:
            config_file: Path to configuration file

        Returns:
            Configuration dictionary
        """
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)

            # Merge with defaults
            merged_config = self.default_config.copy()
            merged_config.update(config)

            return merged_config
        except FileNotFoundError:
            print(f"❌ Configuration file not found: {config_file}")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON in configuration file: {e}")
            sys.exit(1)

    def save_config_to_file(self, config: Dict[str, Any], config_file: str) -> None:
        """
        Save project configuration to JSON file.

        Args:
            config: Configuration dictionary
            config_file: Path to save configuration
        """
        try:
            with open(config_file, 'w') as f:
                json.dump(config, f, indent=2)
            print(f"✅ Configuration saved to: {config_file}")
        except Exception as e:
            print(f"❌ Failed to save configuration: {e}")

    def print_next_steps(self, project_path: str, config: Dict[str, Any]) -> None:
        """Print next steps for the user."""
        project_name = config["project_name"]

        print(f"""
🎯 Next Steps for {project_name}:

1. Navigate to project:
   cd {project_path}

2. Review configuration:
   - Edit configs/config.yaml for your environment
   - Set environment variables as needed

3. Install dependencies:
   go mod download

4. Run the application:
   go run cmd/server/main.go

   # Or with live reload:
   make install-deps
   make dev

5. Run tests:
   make test

6. Build for production:
   make build

7. Run with Docker:
   docker-compose up -d

📚 Useful Commands:
   make help              # Show all available commands
   make test-coverage     # Run tests with coverage
   make lint              # Run linter
   make docker-build      # Build Docker image
   make clean             # Clean build artifacts

🔗 API Documentation:
   http://localhost:8080/swagger/index.html

🏥 Health Check:
   http://localhost:8080/api/v1/health

📊 Metrics (if enabled):
   http://localhost:9090/metrics

Happy coding! 🚀
""")


def main():
    """Main entry point for the project generator."""
    parser = argparse.ArgumentParser(description="Go Gin Project Generator")
    parser.add_argument("name", nargs="?", help="Project name")
    parser.add_argument("-t", "--type", choices=["api", "web", "microservice", "grpc"],
                       default="api", help="Project type")
    parser.add_argument("-m", "--module", help="Go module path")
    parser.add_argument("-c", "--config", help="Configuration file (JSON)")
    parser.add_argument("-o", "--output", default=".", help="Output directory")
    parser.add_argument("--interactive", action="store_true", help="Interactive mode")
    parser.add_argument("--save-config", help="Save configuration to file")

    args = parser.parse_args()

    generator = GoGinProjectGenerator()

    # Get configuration
    if args.interactive or not args.name:
        config = generator.get_user_input()
    elif args.config:
        config = generator.load_config_from_file(args.config)
        if args.name:
            config["project_name"] = args.name
        if args.type != "api":
            config["project_type"] = args.type
        if args.module:
            config["module_path"] = args.module
    else:
        # Use command line arguments
        config = generator.default_config.copy()
        config["project_name"] = args.name
        config["project_type"] = args.type
        if args.module:
            config["module_path"] = args.module
        else:
            config["module_path"] = f"github.com/username/{args.name}"

    # Save configuration if requested
    if args.save_config:
        generator.save_config_to_file(config, args.save_config)

    # Generate project
    try:
        project_path = generator.generate_project(config, args.output)
        generator.print_next_steps(project_path, config)
    except Exception as e:
        print(f"❌ Failed to generate project: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()