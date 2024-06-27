.PHONY: start stop

COMPOSE_FILE=docker/docker-compose.yml

build:
	@docker-compose -f $(COMPOSE_FILE) build

start:
	@docker-compose -f $(COMPOSE_FILE) up -d

stop:
	@docker-compose -f $(COMPOSE_FILE) down