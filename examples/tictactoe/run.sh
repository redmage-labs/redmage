#!/bin/bash

set -e

uvicorn examples.tictactoe:app.starlette --host '0.0.0.0' --log-level=debug --reload