SERVICE_TARGET := $(notdir $(PWD))
MANAGE := docker-compose exec $(SERVICE_TARGET) pipenv run python manage.py

include ../scripts/container-helpers.mk

test_:
	$(MANAGE) test $(ARGS)

# only lint files changed
lint:
	FILES="$(shell git diff --cached --name-only | grep ^backend/.*\.py$ | sed s:^backend/::g)"; \
	docker-compose exec $(SERVICE_TARGET) pipenv run black $$FILES

help_:
	@echo '  manage   	call manage.py with ARGS'
	@echo '  migrations	shortcut for makemigrations'
	@echo '  migrate    	apply all migrations'
	@echo '  shell    	run the django shell'

manage:
	$(MANAGE) $(ARGS)

migrations:
	$(MANAGE) makemigrations $(ARGS)

migrate:
	$(MANAGE) migrate $(ARGS)

shell:
	$(MANAGE) shell $(ARGS)

.PHONY: manage migrations migrate shell
