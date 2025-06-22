#!/usr/bin/env python3
"""
Configuration handling for ConTiny
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, field

@dataclass
class ContainerConfig:
    """Container configuration data class"""
    name: str
    base_distro: str = "ubuntu:20.04"
    python_version: str = "3.9"
    packages: list = field(default_factory=list)
    files: dict = field(default_factory=dict)
    environment: dict = field(default_factory=dict)
    working_dir: str = "/workspace"
    entrypoint: list = field(default_factory=lambda: ["/bin/bash"])

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "name": self.name,
            "base_distro": self.base_distro,
            "python_version": self.python_version,
            "packages": self.packages,
            "files": self.files,
            "environment": self.environment,
            "working_dir": self.working_dir,
            "entrypoint": self.entrypoint
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ContainerConfig':
        """Create from dictionary"""
        return cls(
            name=data.get("name", "default"),
            base_distro=data.get("base_distro", "ubuntu:20.04"),
            python_version=data.get("python_version", "3.9"),
            packages=data.get("packages", []),
            files=data.get("files", {}),
            environment=data.get("environment", {}),
            working_dir=data.get("working_dir", "/workspace"),
            entrypoint=data.get("entrypoint", ["/bin/bash"])
        )

class ConfigParser:
    """Configuration file parser"""
    
    @staticmethod
    def parse_continy_format(content: str) -> Dict[str, Any]:
        """Parse ConTiny .conf format"""
        config = {
            "name": "default",
            "base_distro": "ubuntu:20.04",
            "python_version": "3.9",
            "packages": [],
            "files": {},
            "environment": {},
            "working_dir": "/workspace",
            "entrypoint": ["/bin/bash"]
        }
        
        for line in content.strip().split('\n'):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            if line.startswith('NAME:'):
                config["name"] = line.split(':', 1)[1].strip()
            elif line.startswith('BASE:'):
                config["base_distro"] = line.split(':', 1)[1].strip()
            elif line.startswith('PYTHON:'):
                config["python_version"] = line.split(':', 1)[1].strip()
            elif line.startswith('PACKAGE:'):
                config["packages"].append(line.split(':', 1)[1].strip())
            elif line.startswith('FILE:'):
                parts = line.split(':', 2)
                if len(parts) == 3:
                    config["files"][parts[1].strip()] = parts[2].strip()
            elif line.startswith('ENV:'):
                parts = line.split(':', 2)
                if len(parts) == 3:
                    config["environment"][parts[1].strip()] = parts[2].strip()
            elif line.startswith('WORKDIR:'):
                config["working_dir"] = line.split(':', 1)[1].strip()
        
        return config
    
    @staticmethod
    def parse_json_format(content: str) -> Dict[str, Any]:
        """Parse JSON format"""
        return json.loads(content)
    
    @staticmethod
    def load_config_file(file_path: str) -> ContainerConfig:
        """Load configuration from file"""
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"Configuration file not found: {file_path}")
        
        with open(path, 'r') as f:
            content = f.read()
        
        if file_path.endswith('.json'):
            config_dict = ConfigParser.parse_json_format(content)
        else:
            config_dict = ConfigParser.parse_continy_format(content)
        
        return ContainerConfig.from_dict(config_dict)
    
    @staticmethod
    def validate_config(config: ContainerConfig) -> bool:
        """Validate configuration"""
        if not config.name:
            raise ValueError("Container name is required")
        
        if not config.base_distro:
            raise ValueError("Base distribution is required")
        
        # Validate Python version format
        try:
            version_parts = config.python_version.split('.')
            if len(version_parts) < 2:
                raise ValueError("Invalid Python version format")
            major, minor = int(version_parts[0]), int(version_parts[1])
            if major < 3 or (major == 3 and minor < 8):
                raise ValueError("Python version must be 3.8 or higher")
        except (ValueError, IndexError):
            raise ValueError("Invalid Python version format")
        
        # Validate file paths
        for source_path in config.files.keys():
            if not os.path.exists(source_path):
                print(f"Warning: Source file not found: {source_path}")
        
        return True