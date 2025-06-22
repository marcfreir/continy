import json
from typing import Dict, List, Optional
from .core import ConTiny

from .config import ConfigParser, ContainerConfig


class ContainerBuilder:
    """Helper class to build containers from configuration files"""

    @staticmethod
    def from_file(container_file: str) -> ConTiny:
        """Create container from configuration file"""
        with open(container_file, "r") as f:
            if container_file.endswith(".json"):
                config = json.load(f)
            else:
                # ConTiny text format
                config = ContainerBuilder._parse_continy_format(f.read())

        container = ConTiny(config["name"])
        container.config.update(config)
        return container

    @staticmethod
    def _parse_continy_format(content: str) -> Dict:
        """Parse ConTiny container format"""
        config = {
            "name": "default",
            "base_distro": "ubuntu:20.04",
            "python_version": "3.9",
            "packages": [],
            "files": {},
            "environment": {},
            "working_dir": "/workspace",
            "entrypoint": ["/bin/bash"],
        }

        for line in content.strip().split("\n"):
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            if line.startswith("NAME:"):
                config["name"] = line.split(":", 1)[1].strip()
            elif line.startswith("BASE:"):
                config["base_distro"] = line.split(":", 1)[1].strip()
            elif line.startswith("PYTHON:"):
                config["python_version"] = line.split(":", 1)[1].strip()
            elif line.startswith("PACKAGE:"):
                config["packages"].append(line.split(":", 1)[1].strip())
            elif line.startswith("FILE:"):
                parts = line.split(":", 2)
                if len(parts) == 3:
                    config["files"][parts[1].strip()] = parts[2].strip()
            elif line.startswith("ENV:"):
                parts = line.split(":", 2)
                if len(parts) == 3:
                    config["environment"][parts[1].strip()] = parts[2].strip()

        return config
