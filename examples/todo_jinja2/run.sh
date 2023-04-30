#!/bin/bash

set -e

uvicorn examples.todo_jinja2:app.starlette --log-level=debug --reload