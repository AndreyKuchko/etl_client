import pytest

from typing import List, Optional

from etl_client.processing.base import BaseProcessor


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

    def __init__(self, content):
        self.content = content

    async def read(self):
        return self.content


class TestRequestContextManager:
    def __init__(self, content):
        self.content = content

    async def __aenter__(self):
        return TestResponse(self.content)

    async def __aexit__(self, *args, **kwargs):
        pass


class TestSession:
    def get(self, url, params):
        content = JSON_RESPONSE_DATA
        if url.endswith(".csv"):
            content = CSV_RESPONSE_DATA
        return TestRequestContextManager(content)


class TestFile:
    _instance = None

    def __init__(self):
        self.path: Optional[str] = None
        self.written_data: List = []
        self.closed: bool = False

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    async def write(self, data):
        self.written_data.append(data)

    async def close(self):
        self.closed = True


async def aiofiles_open(path, mode):
    test_file = TestFile.get_instance()
    test_file.path = path
    test_file.closed = False
    test_file.written_data = []
    return test_file


@pytest.fixture
def mock_aiohttp_session():
    return TestSession()


@pytest.fixture
def mock_aiofiles_open():
    return aiofiles_open


@pytest.fixture
def mocked_file():
    return TestFile.get_instance()
