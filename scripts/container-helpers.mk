# standard commands for containerized services, makefiles including
# this file must only define SERVICE_TARGET.
PWD ?= pwd_unknown

.PHONY: help build up down attach log test test_ help_

help:
	@echo 'Usage: make [TARGET]'
	@echo 'Targets:'
	@echo '  build    	build docker image'
	@echo '  up		run as container in the background'
	@echo '  down   	stop container'
	@echo '  attach    	attach to running container'
	@echo '  log    	follow container logs'
	@echo '  test    	run tests in container'
	@$(MAKE) -s help_

build:
	docker-compose build $(SERVICE_TARGET)

up:
	docker-compose up -d $(SERVICE_TARGET)

down:
	docker-compose rm -sf $(SERVICE_TARGET)

attach: up
	docker-compose exec $(SERVICE_TARGET) bash

log:
	docker-compose logs -f $(SERVICE_TARGET)

test:
	@$(MAKE) -s up
	@$(MAKE) -s test_
