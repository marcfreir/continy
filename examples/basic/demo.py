#!/usr/bin/env python3
"""
Example usage of ConTiny framework
"""

from continy import ConTiny
from continy.builder import ContainerBuilder

# All your example functions go here...
# (exact same code you provided)

if __name__ == "__main__":
    # Create sample files first
    create_sample_files()
    
    # Run examples
    container1 = example_programmatic_creation()
    container2 = example_file_based_creation()
    
    # List containers
    print("\n=== Available containers ===")
    ConTiny.list_containers()
    
    print("\nTo run containers:")
    print("continy run --name my-data-env")
    print("continy run --name my-data-env --command 'jupyter notebook --ip=0.0.0.0 --allow-root'")