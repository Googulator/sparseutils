all: doc

.PHONY: doc
doc: README

README: README.md
	pandoc --from=markdown --to=rst --output=$@ $<

.PHONY: clean
clean:
	rm -f README
