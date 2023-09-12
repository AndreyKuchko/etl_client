from etl_client.management import commands, run_command


def entry_point():
    """Run command from available in registry."""
    run_command(registry=commands)


if __name__ == "__main__":
    entry_point()
