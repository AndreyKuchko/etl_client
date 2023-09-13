import asyncio
import argparse
from datetime import date, timedelta
from time import time
from typing import Any, List, Type

import aiohttp

from etl_client.exceptions import ProcessingError
from etl_client.processing.base import BaseProcessor
from etl_client.settings import get_settings
from etl_client.utils.logging import get_logger


class BaseCommand:
    """Base class for all commands. It contains common logic and common arguments definition."""

    def __init__(
        self,
        args: argparse.Namespace,
        remaining_args: List,
        **_,
    ):
        self.args = args
        self.remaining_args = remaining_args
        self.logger = get_logger(get_settings().log_level, args.logging_prefix)

    @staticmethod
    def prepare_argparser(argparser: argparse.ArgumentParser):
        """Prepare arguments for command."""
        argparser.add_argument(
            "--logging-prefix",
            dest="logging_prefix",
            type=str,
            default=None,
            help="Prefix for all logging records",
        )

    def run(self) -> Any:
        """Run the command."""
        start = time()
        result = asyncio.get_event_loop().run_until_complete(self.async_run())
        self.logger.info("Finished! It took {:.3f} seconds in total".format(time() - start))
        return result

    async def async_run(self):
        """Execute async functional part of command."""
        raise NotImplementedError


class BaseAsyncWorker(BaseCommand):
    """Base class for async worker commands."""

    processor_class: Type[BaseProcessor]

    def __init__(self, *args, **kwargs):
        settings = get_settings()
        super(BaseAsyncWorker, self).__init__(*args, **kwargs)
        timeout = aiohttp.ClientTimeout(total=settings.source_timeout)
        self.session = aiohttp.ClientSession(
            f"{settings.source_schema}://{settings.source_host}:{settings.source_port}",
            timeout=timeout,
            headers=self.processor_class.headers,
        )
        today = date.today()
        self.tasks = [today - timedelta(days=i + 1) for i in range(settings.previous_days_count)]
        self.errors = {}

    async def run_processor(self, number: int):
        """Prepare processor and run active tasks in it."""
        processor = self.processor_class(self.session, self.logger)
        self.logger.debug(f"Starting processor #{number}")
        while self.tasks:
            day = self.tasks.pop()
            try:
                await processor.extract(day)
            except ProcessingError as e:
                self.errors[day] = e
        self.logger.debug(f"Finishing processor #{number}")

    async def async_run(self):
        """Prepare pool of processors and run them together."""
        await asyncio.gather(*[self.run_processor(i) for i in range(get_settings().concurrency)])
        if self.errors:
            self.logger.error("Processing finished with errors for following days:")
            for day, error in self.errors.items():
                self.logger.error(f"{day}: {error}")
        await self.session.close()
