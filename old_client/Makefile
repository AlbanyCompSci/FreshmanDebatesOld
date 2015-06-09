all: main.html main.css main.jsx
	for f in `ls js/*.jsx`; do \
		fcomp=`echo f | sed 's/\..*//'`.js \
		jsx $f > "js/$(fcomp)"; \
	done
clean:
	rm -rf main.js
