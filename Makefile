all: version clean

RED := "\033[0;31m"
GREEN := "\033[0;32m"
ORANGE := "\033[0;33m"
BLUE := "\033[0;34m"
CLOSE := "\033[0m"

clean:
	@echo $(RED)"Clean extra files and folders:"
	@echo $(BLUE)" - Remove extra files and folders"$(CLOSE)
	@$(shell rm -rf .pytest_cache dist rad_data.egg-info)
	@$(shell find . -type f -name "*.py[co]" -delete -o -type d -name __pycache__ -delete)

setup:
	@echo $(RED)"Setup base crawler:"$(CLOSE)
	@$(shell python setup.py sdist --formats=gztar,zip)
