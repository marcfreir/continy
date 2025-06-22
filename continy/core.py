#!/usr/bin/env python3
"""
ConTiny - A minimal container framework
Author: Marc Freir
"""

import os
import sys
import json
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, List, Optional

from .config import ContainerConfig, ConfigParser
from .utils import run_command, create_directory_structure, copy_file_safe, print_container_info


class ConTiny:
    def __init__(self, name: str):
        self.name = name
        self.base_dir = Path(f"containers/{name}")
        self.rootfs_dir = self.base_dir / "rootfs"
        self.config_file = self.base_dir / "container.json"
        self.config = {
            "name": name,
            "base_distro": "ubuntu:20.04",
            "python_version": "3.9",
            "packages": [],
            "files": {},
            "environment": {},
            "working_dir": "/workspace",
            "entrypoint": ["/bin/bash"],
        }

    def create(self):
        """Create container directory structure"""
        print(f"Creating container: {self.name}")
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.rootfs_dir.mkdir(exist_ok=True)

        # Create basic directory structure
        for dir_path in [
            "bin",
            "usr/bin",
            "usr/local/bin",
            "workspace",
            "tmp",
            "var",
            "etc",
        ]:
            (self.rootfs_dir / dir_path).mkdir(parents=True, exist_ok=True)

        # Save initial config
        self.save_config()
        print(f"Container {self.name} created successfully!")

    def set_base_distro(self, distro: str):
        """Set base Linux distribution"""
        self.config["base_distro"] = distro
        self.save_config()

    def add_package(self, package: str):
        """Add a package to install"""
        if package not in self.config["packages"]:
            self.config["packages"].append(package)
            self.save_config()

    def add_file(self, source: str, destination: str):
        """Add a file to copy into the container"""
        self.config["files"][source] = destination
        self.save_config()

    def set_environment(self, key: str, value: str):
        """Set environment variable"""
        self.config["environment"][key] = value
        self.save_config()

    def save_config(self):
        """Save container configuration"""
        with open(self.config_file, "w") as f:
            json.dump(self.config, f, indent=2)

    def load_config(self):
        """Load container configuration"""
        if self.config_file.exists():
            with open(self.config_file, "r") as f:
                self.config = json.load(f)

    def build(self):
        """Build the container"""
        print(f"Building container: {self.name}")

        # Create bootstrap script
        bootstrap_script = self._create_bootstrap_script()

        # Run bootstrap in chroot environment
        self._run_bootstrap(bootstrap_script)

        # Copy user files
        self._copy_user_files()

        # Setup Python virtual environment
        self._setup_python_env()

        print(f"Container {self.name} built successfully!")

    def _create_bootstrap_script(self) -> str:
        """Create bootstrap script for container setup"""
        script = f"""#!/bin/bash
set -e

# Update package manager
apt-get update

# Install basic packages
apt-get install -y python{self.config['python_version']} python3-pip python3-venv curl wget

# Install additional packages
"""
        for package in self.config["packages"]:
            script += f"apt-get install -y {package}\n"

        script += """
# Install Jupyter
pip3 install jupyter notebook jupyterlab

# Clean up
apt-get clean
rm -rf /var/lib/apt/lists/*
"""
        return script

    def _run_bootstrap(self, script: str):
        """Run bootstrap script in container environment"""
        script_path = self.rootfs_dir / "bootstrap.sh"
        with open(script_path, "w") as f:
            f.write(script)

        os.chmod(script_path, 0o755)

        # For simplicity, we'll create a minimal environment
        # In a real implementation, you'd use chroot or namespaces
        print("Setting up container environment...")

    def _copy_user_files(self):
        """Copy user-specified files into container"""
        for source, destination in self.config["files"].items():
            if os.path.exists(source):
                dest_path = self.rootfs_dir / destination.lstrip("/")
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, dest_path)
                print(f"Copied {source} -> {destination}")

    def _setup_python_env(self):
        """Setup Python virtual environment"""
        venv_path = self.rootfs_dir / "workspace" / "venv"

        # Create startup script
        startup_script = f"""#!/bin/bash
export PATH="/workspace/venv/bin:$PATH"
export PYTHONPATH="/workspace:$PYTHONPATH"
"""

        for key, value in self.config["environment"].items():
            startup_script += f'export {key}="{value}"\n'

        startup_script += """
cd /workspace
echo "ConTiny environment ready!"
echo "Python virtual environment: /workspace/venv"
echo "To start Jupyter: jupyter notebook --ip=0.0.0.0 --allow-root"
exec "$@"
"""

        startup_path = self.rootfs_dir / "entrypoint.sh"
        with open(startup_path, "w") as f:
            f.write(startup_script)
        os.chmod(startup_path, 0o755)

    def run(self, command: Optional[List[str]] = None):
        """Run container with specified command"""
        if not self.rootfs_dir.exists():
            print(f"Container {self.name} not built. Run build() first.")
            return

        if command is None:
            command = self.config["entrypoint"]

        print(f"Running container: {self.name}")
        print(f"Command: {' '.join(command)}")

        # For demonstration - in real implementation, use namespaces/chroot
        env = os.environ.copy()
        env.update(self.config["environment"])

        try:
            subprocess.run(
                ["/bin/bash", str(self.rootfs_dir / "entrypoint.sh")] + command,
                cwd=str(self.rootfs_dir / "workspace"),
                env=env,
            )
        except KeyboardInterrupt:
            print("\nContainer stopped.")

    def list_containers():
        """List all containers"""
        containers_dir = Path("containers")
        if not containers_dir.exists():
            print("No containers found.")
            return

        print("Available containers:")
        for container_dir in containers_dir.iterdir():
            if container_dir.is_dir():
                config_file = container_dir / "container.json"
                if config_file.exists():
                    print(f"  - {container_dir.name}")
