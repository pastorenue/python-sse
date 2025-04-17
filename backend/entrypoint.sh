#!/bin/bash

echo "Starting the Uvicorn application..."
poetry run uvicorn main:app --app-dir /app/src --host 0.0.0.0 --port 5400 --log-level debug