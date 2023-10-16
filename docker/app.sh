#!/bin/bash

alembic upgrade head

cd app

uvicorn myapp:app --host=0.0.0.0 --port=8000
