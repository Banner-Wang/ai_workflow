#!/bin/bash

# Task Management Platform - Worker Startup Script
echo "Starting Arq Worker..."

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "Virtual environment activated"
fi

# Start the worker
arq src.worker.settings.WorkerSettings

echo "Worker stopped" 