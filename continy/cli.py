import click
from .core import ConTiny
from .builder import ContainerBuilder


@click.group()
def cli():
    """ConTiny - A minimal container framework"""
    pass


@cli.command()
@click.option("--file", "-f", help="Container configuration file")
@click.option("--name", "-n", help="Container name")
def create(file, name):
    """Create a new container"""
    if file:
        container = ContainerBuilder.from_file(file)
    else:
        container = ConTiny(name)
    container.create()


@cli.command()
@click.option("--file", "-f", help="Container configuration file")
@click.option("--name", "-n", help="Container name")
def build(file, name):
    """Build a container"""
    if file:
        container = ContainerBuilder.from_file(file)
    else:
        container = ConTiny(name)
        container.load_config()
    container.build()


@cli.command()
@click.option("--name", "-n", required=True, help="Container name")
@click.option("--command", "-c", help="Command to run")
def run(name, command):
    """Run a container"""
    container = ConTiny(name)
    container.load_config()
    cmd = command.split() if command else None
    container.run(cmd)


@cli.command()
def list():
    """List all containers"""
    ConTiny.list_containers()


def main():
    cli()
