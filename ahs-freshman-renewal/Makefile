all:
	mkdir deployment
	mkdir deployment/js
	jsx js deployment/js
	#browserify deployment/js/app.js -o deployment/js/app.js
	cp -r img deployment/img
	cp -r css deployment/css
	cp index.html deployment/index.html

clean:
	rm -r deployment
