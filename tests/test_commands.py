import argparse
from datetime import date
from typing import List
from unittest.mock import patch

import pytest

from etl_client.management.base import BaseAsyncWorker
from etl_client.processing.base import BaseProcessor
from etl_client.settings import settings


class ProcessorForTests(BaseProcessor):
    days: List[date] = []
    instances_count: int = 0

    def __init__(self, *args, **kwargs):
        super(ProcessorForTests, self).__init__(*args, **kwargs)
        ProcessorForTests.instances_count += 1

    async def extract(self, day):
        ProcessorForTests.days.append(day)


class Command(BaseAsyncWorker):
    processor_class = ProcessorForTests


def test_worker_command():
    parser = argparse.ArgumentParser()
    args, remaining_args = parser.parse_known_args([])
    with patch(
        "etl_client.management.manager.CommandManager.prepare_command", return_value=Command
    ):
        command = Command(args, remaining_args, parser)
        command.run()
    assert ProcessorForTests.instances_count == settings.concurrency
    assert len(ProcessorForTests.days) == settings.previous_days_count
