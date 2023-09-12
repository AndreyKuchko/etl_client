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

## How to run tests
```shell
make tests
```
