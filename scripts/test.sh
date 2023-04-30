#!/bin/bash
set -e

isort -s env -c .
black redmage/. --check


pycodestyle --max-line-length=100 --ignore=E742,W503 redmage/
retVal=$?
if [ $retVal -ne 0 ]; then
    echo "Python Lint Error"
    exit $retVal
fi

python -m mypy redmage/ --exclude env/ --disallow-untyped-defs
retVal=$?
if [ $retVal -ne 0 ]; then
    echo "Python Type Checking Error"
    exit $retVal
fi

python -m pytest --cov-report term-missing --cov=redmage/ tests/
retVal=$?
if [ $retVal -ne 0 ]; then
    echo "Python Test Error"
    exit $retVal
fi