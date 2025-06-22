#!/usr/bin/env python3
"""
Utility functions for ConTiny
"""

import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import List, Optional, Dict

def run_command(command: List[str], cwd: Optional[str] = None, env: Optional[Dict[str, str]] = None) -> subprocess.CompletedProcess:
    """Run a command and return the result"""
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            env=env,
            capture_output=True,
            text=True,
            check=True
        )
        return result
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {' '.join(command)}")
        print(f"Error: {e.stderr}")
        raise

def create_directory_structure(base_path: Path, directories: List[str]):
    """Create directory structure"""
    for directory in directories:
        (base_path / directory).mkdir(parents=True, exist_ok=True)

def copy_file_safe(source: str, destination: Path):
    """Safely copy a file with error handling"""
    try:
        if os.path.isdir(source):
            if destination.exists():
                shutil.rmtree(destination)
            shutil.copytree(source, destination)
        else:
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
        return True
    except Exception as e:
        print(f"Error copying {source} to {destination}: {e}")
        return False

def format_size(size_bytes: int) -> str:
    """Format file size in human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"

def get_directory_size(path: Path) -> int:
    """Get total size of directory"""
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            if os.path.exists(filepath):
                total_size += os.path.getsize(filepath)
    return total_size

def validate_name(name: str) -> bool:
    """Validate container name"""
    if not name:
        return False
    
    # Container names should be alphanumeric with hyphens and underscores
    allowed_chars = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_')
    return all(c in allowed_chars for c in name) and len(name) <= 64

def create_bootstrap_script(config) -> str:
    """Create bootstrap script for container setup"""
    script = f"""#!/bin/bash
set -e

# Update package manager
apt-get update

# Install basic packages
apt-get install -y python{config.python_version} python3-pip python3-venv curl wget

# Install additional packages
"""
    for package in config.packages:
        script += f"apt-get install -y {package}\n"
    
    script += """
# Install Jupyter
pip3 install jupyter notebook jupyterlab

# Clean up
apt-get clean
rm -rf /var/lib/apt/lists/*
"""
    return script

def create_entrypoint_script(config) -> str:
    """Create entrypoint script for container"""
    script = f"""#!/bin/bash
export PATH="/workspace/venv/bin:$PATH"
export PYTHONPATH="/workspace:$PYTHONPATH"
"""
    
    for key, value in config.environment.items():
        script += f'export {key}="{value}"\n'
    
    script += f"""
cd {config.working_dir}
echo "ConTiny environment ready!"
echo "Python virtual environment: /workspace/venv"
echo "To start Jupyter: jupyter notebook --ip=0.0.0.0 --allow-root"
exec "$@"
"""
    return script

def print_container_info(container):
    """Print container information"""
    print(f"Container: {container.name}")
    print(f"Base: {container.config['base_distro']}")
    print(f"Python: {container.config['python_version']}")
    print(f"Packages: {', '.join(container.config['packages']) if container.config['packages'] else 'None'}")
    
    if container.base_dir.exists():
        size = get_directory_size(container.base_dir)
        print(f"Size: {format_size(size)}")
    
    print(f"Location: {container.base_dir}")