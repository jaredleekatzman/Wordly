// Build into useable dependency with:
// browserify public/scripts/autosizeNodes.js -o public/scripts/bundle.js

var autosize = require('autosize');

window.onload = function(e){ 
	console.log(document.querySelectorAll('textarea'));
	autosize(document.querySelectorAll('textarea'));
}