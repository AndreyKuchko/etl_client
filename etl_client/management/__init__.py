import sys
from typing import Any, Dict, List, Optional

from etl_client.management.manager import CommandManager


def run_command(registry: Dict, raw_args: Optional[List] = None) -> Any:
    """Single entry point for all commands."""
    if raw_args is None:
        raw_args = sys.argv[1:]
    command_manager = CommandManager(registry=registry, raw_args=raw_args)
    command_manager.init_argparser()
    return command_manager.run()
