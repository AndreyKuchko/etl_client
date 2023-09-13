from etl_client.management.commands import csv_consumer
from etl_client.management.commands import json_consumer
from etl_client.management.commands import run_all

COMMANDS = {
    "csv_consumer": csv_consumer.Command,
    "json_consumer": json_consumer.Command,
    "run_all": run_all.Command,
}
