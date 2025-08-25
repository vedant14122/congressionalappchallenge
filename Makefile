.PHONY: help setup dev build test clean db-up db-down db-migrate db-seed

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

setup: ## Initial setup - install deps, start DB, run migrations and seed
	pnpm install
	pnpm db:up
	sleep 5
	pnpm db:migrate
	pnpm db:seed

dev: ## Start all apps in development mode
	pnpm dev

build: ## Build all apps
	pnpm build

test: ## Run tests
	pnpm test

clean: ## Clean all build artifacts
	pnpm clean

db-up: ## Start database
	pnpm db:up

db-down: ## Stop database
	pnpm db:down

db-migrate: ## Run database migrations
	pnpm db:migrate

db-seed: ## Seed database with sample data
	pnpm db:seed

db-reset: ## Reset database (drop and recreate)
	pnpm db:down
	pnpm db:up
	sleep 5
	pnpm db:migrate
	pnpm db:seed
