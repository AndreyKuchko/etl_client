import asyncio
import io
from datetime import date, timedelta
from os import path

import aiohttp
import pandas as pd
from aiofiles import open
from aiofiles.threadpool.text import AsyncTextIOWrapper
from aiohttp import ClientSession
from logging import Logger
from typing import Dict

from etl_client.exceptions import ProcessingError
from etl_client.settings import get_settings

RETRY_STATUSES = [429, 500]


class BaseProcessor:
    """Base class for ETL processor."""

    headers: Dict = {}
    name: str
    url: str

    def __init__(self, session: ClientSession, logger: Logger):
        self.session = session
        self.logger = logger

    async def extract(self, day: date):
        """Get data by given url and run transformation."""
        url = self.url.format(day)
        params = {"api_key": get_settings().source_api_key}
        call_required = True
        while call_required:
            async with self.session.get(url, params=params) as response:
                status = response.status
                if status == 200:
                    await self.transform(day, response)
                    call_required = False
                elif status in RETRY_STATUSES:
                    retry_interval = get_settings().retry_interval
                    self.logger.info(
                        f"Source server returned returned {status}. Request will be "
                        f"retried in {retry_interval} second(s)."
                    )
                    await asyncio.sleep(retry_interval)
                else:
                    raise ProcessingError(f"Source server returned {status}.")

    async def transform(self, day: date, response: aiohttp.ClientResponse):
        """Run data transformation."""
        raise NotImplementedError

    async def load(
        self,
        df: pd.DataFrame,
        destination: AsyncTextIOWrapper,
        add_headers: bool = False,
    ):
        """Load data to given destination file."""
        stream = io.StringIO()
        df.to_csv(stream, index=False, header=add_headers)
        await destination.write(stream.getvalue())

    def normalize_headers(self, df: pd.DataFrame):
        """Fix column names."""
        new_headers = {}
        for header in df.columns:
            new_header = header.strip().replace(" ", "_").capitalize()
            if new_header == "Naive_timestamp":
                new_header = "Timestamp"
            new_headers[header] = new_header
        df.rename(columns=new_headers, inplace=True)

    def normalize_timestamps(self, df: pd.DataFrame):
        """Fix timestamp fields."""
        raise NotImplementedError

    async def open_destination_file(self, day: date) -> AsyncTextIOWrapper:
        """Open destination file for writing data."""
        return await open(
            path.join(
                get_settings().destination_dir,
                f"{self.name.upper()}_{day}-00-00_{day + timedelta(days=1)}-00-00.csv",
            ),
            mode="w+",
        )
