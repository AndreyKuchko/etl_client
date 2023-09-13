from etl_client.management import run_command
from etl_client.management.registry import COMMANDS


def entry_point():
    """Run command from available in registry."""
    run_command(registry=COMMANDS)


if __name__ == "__main__":
    entry_point()
