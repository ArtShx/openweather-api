#!/bin/bash

pip install -r requirements-dev.txt
coverage run -m pytest tests
coverage report -m

