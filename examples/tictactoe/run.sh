#!/bin/bash

set -e

uvicorn examples.tictactoe:app.starlette --log-level=debug --reload