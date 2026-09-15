# Always prefer the local `.venv`
export PATH := .venv/bin:$(PATH)

.PHONY: html livehtml clean

html:
	sphinx-build -b html "source/" "build/"

livehtml: clean
	sphinx-autobuild --open-browser --delay 1 "source/" "build/html"

clean:
	rm -rf "build"
