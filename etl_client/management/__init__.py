import sys
from types import ModuleType
from typing import Any

from etl_client.management.manager import CommandManager


def run_command(registry: ModuleType) -> Any:
    """Single entry point for all commands."""
    command_manager = CommandManager(registry=registry, raw_args=sys.argv[1:])
    command_manager.init_argparser()
    return command_manager.run()
