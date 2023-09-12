import argparse
import inspect
from types import ModuleType
from typing import Any, List

from etl_client.exceptions import CommandNotFound
from etl_client.management.base import BaseCommand


class CommandManager:
    """Wrapper around commands that makes available choosing of commands from
    common parent command(etl_client)
    """

    def __init__(self, registry: ModuleType, raw_args: List):
        self.registry = registry
        self.argparser = argparse.ArgumentParser()
        self.subparsers = self.argparser.add_subparsers(
            dest="command_name",
            description="Command name to run",
            title="command_name",
        )
        self.subparsers.required = True

        self.raw_args = raw_args
        self.args: argparse.Namespace
        self.remaining_args: List

    @property
    def command_name(self) -> str:
        """Get command name."""
        return self.args.command_name

    def init_argparser(self):
        """Initialise root argparser."""
        for attribute_name in filter(lambda attr: not attr.startswith("_"), dir(self.registry)):
            attribute = getattr(self.registry, attribute_name)
            if self.is_command(attribute):
                subparser = self.subparsers.add_parser(
                    attribute_name,
                    description=attribute.Command.__doc__,
                    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                )
                attribute.Command.prepare_argparser(subparser)

        self.args, self.remaining_args = self.argparser.parse_known_args(self.raw_args)

    def prepare_command(self) -> BaseCommand:
        """Find command in registry."""
        command_module = getattr(self.registry, self.command_name)
        if self.is_command(command_module):
            return command_module.Command(
                args=self.args,
                remaining_args=self.remaining_args,
                argparser=self.argparser,
            )
        raise CommandNotFound("Command with name '{}' was not found".format(self.command_name))

    def run(self) -> Any:
        """Prepare command and run it."""
        command = self.prepare_command()
        return command.run()

    @staticmethod
    def is_command(command: Any) -> bool:
        """Check that given parameter is command."""
        return (
            command
            and hasattr(command, "Command")
            and inspect.isclass(command.Command)
            and issubclass(command.Command, BaseCommand)
        )
