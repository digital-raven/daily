SHELL := /usr/bin/env bash

SRC = $(wildcard *.1.rst)

all: $(SRC:.1.rst=.1.gz)

%.1.gz: %.1.rst
	@gzip <<< `rst2man $<` > $@

clean:
	@rm -f *.1.gz
