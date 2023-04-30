#!/bin/bash

set -e

uvicorn examples.todo:app.starlette --log-level=debug --reload