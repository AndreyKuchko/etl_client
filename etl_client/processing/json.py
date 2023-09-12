import io
from datetime import date
from typing import Dict

import aiohttp
import pandas as pd

from etl_client.processing.base import BaseProcessor
from etl_client.settings import settings


class JsonProcessor(BaseProcessor):
    headers: Dict = {"Accept": "application/json"}
    name: str = "solar"
    url: str = "/{}/renewables/solargen.json"

    async def transform(self, day: date, response: aiohttp.ClientResponse):
        """Transform the whole json source(chunks aren't supported)."""
        destination = await self.open_destination_file(day)
        with io.BytesIO(await response.read()) as bytes_io:
            df = pd.read_json(bytes_io, orient="records")
            self.normalize_timestamps(df)
            await self.load(df, destination, add_headers=True)
        await destination.close()

    def normalize_timestamps(self, df: pd.DataFrame):
        """Convert naive timestamps to timezone aware UTC format."""
        self.normalize_headers(df)
        df["Timestamp"] = (
            pd.to_datetime(df["Timestamp"], unit="ms")
            .dt.tz_localize(settings.default_server_timezone)
            .dt.tz_convert("UTC")
        )
        df["Last_modified_utc"] = pd.to_datetime(df["Last_modified_utc"], unit="ms").dt.tz_localize(
            "UTC"
        )
