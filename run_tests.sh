#!/bin/bash

# Run tests with coverage
python -m pytest tests/test_token_tongs.py --cov=token_tongs --cov-report term-missing

# Generate HTML coverage report (optional)
# python -m pytest tests/test_token_tongs.py --cov=token_tongs --cov-report html

echo "Tests completed!"
