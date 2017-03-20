DOTFILES := $(HOME)/dotfiles

all: browser-wars.png

browser-wars.png: analysis.py chrome.txt firefox.txt safari.txt
	python3.6 ./analysis.py

chrome.txt: log.txt
	cat $< | grep -i chrome > $@

firefox.txt: log.txt
	cat $< | grep -i firefox > $@

safari.txt: log.txt
	cat $< | grep -i safari > $@

log.txt:
	(cd $(DOTFILES) && git log --oneline . | grep -v Revert | grep -i 'firefox\|safari\|chrome' | grep -iE '(switch|use)') > $@

clean:
	@-rm -f chrome.txt firefox.txt safari.txt log.txt 2>/dev/null

.PHONY: log.txt
