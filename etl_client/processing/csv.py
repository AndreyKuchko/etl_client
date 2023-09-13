import io
from datetime import date
from typing import Dict

import aiohttp
import pandas as pd

from etl_client.processing.base import BaseProcessor
from etl_client.settings import get_settings


class CsvProcessor(BaseProcessor):
    """ETL processor for csv endpoint."""

    headers: Dict = {"Accept": "text/csv"}
    name: str = "wind"
    url: str = "/{}/renewables/windgen.csv"

    async def transform(self, day: date, response: aiohttp.ClientResponse):
        """Transform csv source by chunks."""
        destination = await self.open_destination_file(day)
        # TODO: analyse possibility of iterating over chunks
        with io.BytesIO(await response.read()) as bytes_io:
            with pd.read_csv(bytes_io, chunksize=100) as reader:
                first_chunk = next(reader)
                self.normalize_timestamps(first_chunk)
                await self.load(first_chunk, destination, add_headers=True)
                for chunk in reader:
                    self.normalize_timestamps(chunk)
                    await self.load(chunk, destination)
        await destination.close()

    def normalize_timestamps(self, df: pd.DataFrame):
        """Convert naive timestamps to timezone aware UTC format."""
        self.normalize_headers(df)
        df["Timestamp"] = (
            pd.to_datetime(df["Timestamp"])
            .dt.tz_localize(None)
            .dt.tz_localize(get_settings().source_timezone)
            .dt.tz_convert("UTC")
        )
