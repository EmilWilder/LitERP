# LitERP Makefile
.PHONY: help build up down dev logs clean

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Production commands
build: ## Build production Docker images
	docker-compose build

up: ## Start production containers
	docker-compose up -d

down: ## Stop production containers
	docker-compose down

logs: ## View production logs
	docker-compose logs -f

restart: ## Restart production containers
	docker-compose restart

# Development commands
dev-build: ## Build development Docker images
	docker-compose -f docker-compose.dev.yml build

dev-up: ## Start development containers with hot reload
	docker-compose -f docker-compose.dev.yml up -d

dev-down: ## Stop development containers
	docker-compose -f docker-compose.dev.yml down

dev-logs: ## View development logs
	docker-compose -f docker-compose.dev.yml logs -f

# Utility commands
clean: ## Remove all containers, images, and volumes
	docker-compose down -v --rmi all
	docker-compose -f docker-compose.dev.yml down -v --rmi all

shell-backend: ## Open shell in backend container
	docker-compose exec backend /bin/bash

shell-frontend: ## Open shell in frontend container
	docker-compose exec frontend /bin/sh

# Database commands
db-reset: ## Reset database (delete and recreate)
	docker-compose exec backend rm -f /app/data/literp.db
	docker-compose restart backend
