# ConTiny
ConTiny is a simple containerization system for rapid development.

## Key Features:

1. **Simple Configuration**: Two file formats - human-readable `.conf` and JSON
2. **Python + Jupyter Ready**: Automatically sets up Python virtual environments and Jupyter
3. **Minimal Dependencies**: Uses basic Linux tools and Python
4. **Two-File Setup**: Just the main framework file and a config file
5. **Easy CLI**: Simple commands like `create`, `build`, `run`, `list`

## How It Works:

The framework creates isolated environments using:
- Directory-based containers (simpler than full namespaces)
- Python virtual environments for isolation
- Configuration-driven setup
- Built-in support for Jupyter notebooks

## Usage Examples:

```bash
# Create from config file
python3 continy.py create --file container.conf
python3 continy.py build --file container.conf

# Run container
python3 continy.py run --name my-python-env

# Start Jupyter in container
python3 continy.py run --name my-python-env --command "jupyter notebook --ip=0.0.0.0 --allow-root"

# List containers
python3 continy.py list
```

## Key Advantages Over Docker/Singularity:

1. **Simpler**: No complex daemon or root privileges needed
2. **Readable**: Human-friendly configuration files
3. **Lightweight**: Uses existing OS instead of full virtualization
4. **Python-First**: Built specifically for Python/Jupyter workflows
5. **Educational**: Easy to understand and modify

ConTiny gives you a solid starting point that's much simpler than Docker while still providing the core containerization benefits you need for Python development and Jupyter notebooks!
