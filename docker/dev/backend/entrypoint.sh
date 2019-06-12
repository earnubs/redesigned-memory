#!/usr/bin/env bash

# packages are installed at the entrypoint to ease development. At
# production containers we bake in Python packages installation as
# part of the build step.
pipenv install Pipfile --dev

pipenv run python manage.py migrate
pipenv run python manage.py runserver 0:8000
