from typing import Type

from etl_client.management.base import BaseAsyncWorker
from etl_client.processing.json import JsonProcessor


class Command(BaseAsyncWorker):
    """Consume data from csv endpoint."""

    processor_class: Type[JsonProcessor] = JsonProcessor
