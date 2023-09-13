from unittest.mock import patch

import pytest

from typing import List, Optional


CSV_RESPONSE_DATA = b"""Naive_Timestamp , Variable,value,Last Modified utc
2023-09-12 05:00:00+00:00,850,40.9958961662297,2023-09-12 05:00:00+00:00
2023-09-12 05:05:00+00:00,636,-45.693311143179585,2023-09-12 05:00:00+00:00
2023-09-12 05:10:00+00:00,511,32.27062801815019,2023-09-12 05:00:00+00:00"""

JSON_RESPONSE_DATA = (
    b'[{"Naive_Timestamp ":1694546483485," Variable":137,"value":31.5852872231,"Last Modified utc":1694546483485},'
    b'{"Naive_Timestamp ":1694546493485," Variable":971,"value":20.7331970691,"Last Modified utc":1694546483485},'
    b'{"Naive_Timestamp ":1694546503485," Variable":799,"value":-25.1563529597,"Last Modified utc":1694546483485}]'
)


class TestResponse:
    status = 200
    headers = {"Date": "Tue,12 Sep 2023 08:20:38 CET"}

    def __init__(self, content):
        self.content = content

    async def read(self):
        return self.content

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args, **kwargs):
        pass


class TestSession:
    def get(self, url, params=None):
        if url.endswith(".csv"):
            content = CSV_RESPONSE_DATA
        elif url.endswith(".json"):
            content = JSON_RESPONSE_DATA
        else:
            content = '{"status": "ok"}'
        return TestResponse(content)

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args, **kwargs):
        pass

    async def close(self):
        pass


class TestFile:
    def __init__(self):
        self.path: Optional[str] = None
        self.written_data: List = []
        self.closed: bool = False

    async def open(self, path, mode):
        self.path = path
        self.closed = False
        self.written_data = []
        return self

    async def write(self, data):
        self.written_data.append(data)

    async def close(self):
        self.closed = True


@pytest.fixture
def mock_aiohttp_session():
    return TestSession()


@pytest.fixture
def mock_file():
    return TestFile()


@pytest.fixture(autouse=True, scope="session")
def mock_status_check():
    with patch("etl_client.settings.aiohttp.ClientSession", return_value=TestSession()):
        yield
