import asyncio

from etl_client.management.base import BaseCommand


class Command(BaseCommand):
    """Run both csv and json consumers."""

    @staticmethod
    async def consumer(*arguments):
        """Run subprocess to execute single command."""
        process = await asyncio.create_subprocess_exec("etl_client", *arguments)
        await process.wait()

    async def async_run(self):
        """Run csv and json consumers as a separate processes."""
        await asyncio.gather(
            self.consumer("json_consumer", "--logging-prefix", "JSON"),
            self.consumer("csv_consumer", "--logging-prefix", "CSV"),
        )
