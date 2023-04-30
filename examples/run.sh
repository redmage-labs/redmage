#!/bin/bash

set -e

uvicorn examples.$1:app.starlette --log-level=debug --reload