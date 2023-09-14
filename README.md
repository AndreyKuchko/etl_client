# This document describes how to deal with ETL client

[![tests](https://github.com/AndreyKuchko/etl_client/actions/workflows/tests.yml/badge.svg)](https://github.com/AndreyKuchko/etl_client/actions/workflows/tests.yml)
[![codecov](https://codecov.io/gh/AndreyKuchko/etl_client/graph/badge.svg?token=OJQ9EP50Q6)](https://codecov.io/gh/AndreyKuchko/etl_client)

## Prerequisites

You will need Python 3.8+ with virtualenv.

## Preparation

1. Create python virtual environment and install the application
```shell
make install
```
2. Activate virtual environment
```shell
source .venv/bin/activate
```

## Usage

To process data from json endpoint, you can run following command:
```shell
etl_client json_consumer
```
To process data from csv endpoint, you can run following command:
```shell
etl_client csv_consumer
```
To run csv and json consumers together, you can run following command:
```shell
etl_client run_all
```

## Useful commands

Clean output directory from result data files:
```shell
make clean_output
```
Clean application from temporary and service files:
```shell
make clean
```

## Application settings

Application can be configured using environment variables, there is a full table of
available settings:

Name                           | Type | Default         | Description
-------------------------------|------|-----------------|-----------------------------------------------------------------
ETL_CLIENT_SOURCE_SCHEMA       | str  | http            | Schema of source url
ETL_CLIENT_SOURCE_HOST         | str  | localhost       | Source host
ETL_CLIENT_SOURCE_PORT         | int  | 8000            | Source port
ETL_CLIENT_SOURCE_TIMEOUT      | int  | 2               | Timeout for source requests(in seconds)
ETL_CLIENT_SOURCE_API_KEY      | str  | ADU8S67Ddy!d7f? | Api key for source requests
ETL_CLIENT_SOURCE_TIMEZONE     | str  | UTC             | Timezone of source server. Used as a fallback
ETL_CLIENT_PREVIOUS_DAYS_COUNT | int  | 7               | How many days with date to get
ETL_CLIENT_CONCURRENCY         | int  | 5               | How many processors should work in parallel
ETL_CLIENT_RETRY_INTERVAL      | int  | 1               | How long does it wait to retry failed request(in seconds)
ETL_CLIENT_READ_CHUNK_SIZE     | int  | 100             | How many line to use per iteration over document(only for csv)
ETL_CLIENT_LOG_LEVEL           | str  | INFO            | Logging level

## How to run tests
```shell
make tests
```
