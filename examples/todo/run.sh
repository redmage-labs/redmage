#!/bin/bash

set -e

uvicorn examples.todo:app.starlette --host '0.0.0.0' --log-level=debug --reload