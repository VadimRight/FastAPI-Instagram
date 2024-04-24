#!/bin/bash
alembic upgrade head


uvicorn src.main:app --reload

