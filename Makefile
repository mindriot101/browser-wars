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
	(cd $(HOME)/dotfiles && git log --oneline . | grep -v Revert | grep -i 'firefox\|safari\|chrome' | grep -iE '(switch|use)') > $@
