# Check all prerequites are OK
check-prerequisites:
ifeq (, $(shell which docker))
	$(error "No docker in $(PATH), consider install docker package")
endif


# Get or set SSH vars
check-ssh-vars:
SSH_PRIVATE_KEY ?= $(HOME)/.ssh/id_rsa
SSH_PUBLIC_KEY ?= $(HOME)/.ssh/id_rsa.pub


# Clean test environments
clean-test:
	rm -fr .tox/
	rm -f .coverage
	rm -fr reports/


# Target used to execute tests on all tox environments
test-all: check-prerequisites check-ssh-vars
test-all: export SSH_PRIVATE_KEY_PATH = $(SSH_PRIVATE_KEY)
test-all: export SSH_PUBLIC_KEY_PATH = $(SSH_PUBLIC_KEY)
test-all:
	tox


# Target used to execute tests on one tox environment
test-env: check-prerequisites check-ssh-vars
test-env: export SSH_PRIVATE_KEY_PATH = $(SSH_PRIVATE_KEY)
test-env: export SSH_PUBLIC_KEY_PATH = $(SSH_PUBLIC_KEY)
test-env:
ifndef TOXENV
	$(error TOXENV is undefined)
endif
	tox -e "${TOXENV}"
