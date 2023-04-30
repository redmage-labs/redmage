#!/bin/bash
set -e

black .
isort -s env .