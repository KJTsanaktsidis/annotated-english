#makefile!
all:
	cd src/ruleset ; \
	foma -l build.foma
	mv src/ruleset/*.fst fst

clean:
	rm fst/*

test:
	cd src/test ; \
	python3 test.py

test-dickens:
	xargs -0 -n 1 -d "\n" ./speak --att < testcases/dickens	

test-un:
	xargs -0 -n 1 -d "\n" ./speak --att < testcases/un
