from datetime import date
from unittest.mock import patch

import pytest

from etl_client.processing.csv import CsvProcessor
from etl_client.processing.json import JsonProcessor
from etl_client.utils.logging import get_logger


EXPECTED_FILENAME_FOR_JSON = "output/SOLAR_2023-09-12-00-00_2023-09-13-00-00.csv"

EXPECTED_CONTENT_FOR_JSON = [
    """Timestamp,Variable,Value,Last_modified_utc
2023-09-12 17:21:23.485000+00:00,137,31.5852872231,2023-09-12 19:21:23.485000+00:00
2023-09-12 17:21:33.485000+00:00,971,20.7331970691,2023-09-12 19:21:23.485000+00:00
2023-09-12 17:21:43.485000+00:00,799,-25.1563529597,2023-09-12 19:21:23.485000+00:00
"""
]

EXPECTED_FILENAME_FOR_CSV = "output/WIND_2023-09-12-00-00_2023-09-13-00-00.csv"

EXPECTED_CONTENT_FOR_CSV = [
    """Timestamp,Variable,Value,Last_modified_utc
2023-09-12 03:00:00+00:00,850,40.9958961662297,2023-09-12 05:00:00+00:00
2023-09-12 03:05:00+00:00,636,-45.69331114317959,2023-09-12 05:00:00+00:00
2023-09-12 03:10:00+00:00,511,32.27062801815019,2023-09-12 05:00:00+00:00
"""
]


@pytest.mark.parametrize(
    "processor_class,expected_filename,expected_content",
    [
        (JsonProcessor, EXPECTED_FILENAME_FOR_JSON, EXPECTED_CONTENT_FOR_JSON),
        (CsvProcessor, EXPECTED_FILENAME_FOR_CSV, EXPECTED_CONTENT_FOR_CSV),
    ],
)
@pytest.mark.asyncio
async def test_json_processor(
    processor_class,
    expected_filename,
    expected_content,
    mock_aiohttp_session,
    mock_file,
):
    processor = processor_class(mock_aiohttp_session, get_logger("ERROR"))
    with patch("etl_client.processing.base.open", mock_file.open):
        await processor.extract(date(2023, 9, 12))
    assert mock_file.path == expected_filename
    assert mock_file.closed
    assert mock_file.written_data == expected_content
