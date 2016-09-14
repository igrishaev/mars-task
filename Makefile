
.DEFAULT_GOAL = all

.PHONY: test
test:
	python mars.py test

.PHONY: sample
sample:
	cat sample.txt | python mars.py

.PHONY: all
all: test sample
