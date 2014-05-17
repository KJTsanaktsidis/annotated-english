#makefile!
all:
	cd src/ruleset ; \
	foma -l build.foma
	mv src/ruleset/*.fst fst

test:
	cd src/test ; \
	python3 test.py
