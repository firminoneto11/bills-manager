#!/bin/bash

alembic upgrade head;

uvicorn conf.asgi:application --port 8000 --host 0.0.0.0;
