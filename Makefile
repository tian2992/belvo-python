.DEFAULT_GOAL := help

.PHONY: help
help:  ## Shows this help message
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target> <arg=value>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m  %s\033[0m\n\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

##@ 🛠  Testing and development

.PHONY: test
test: ## Run all or specific tests. Arguments: name=NAME-OF-TEST will run a specific test
	./scripts/run-tests.sh $(name)

.PHONY: linting
linting: ## Check of fix code linting using black and isort. Arguments: fix=yes will force changes
	./scripts/run-linting.sh $(fix)

##@ 🚀 Releasing

.PHONY: new-version
new-version: ## Bump version and add commit message. Arguments: type=major|minor|patch
	./scripts/bump-version.sh $(type)
