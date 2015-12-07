/*
 * CrowdSound - controllers/index.js
 *    Implementation by Eli Block based on source code by Kyle Jensen
 *    (c) 2015
 *
 *    Renders index page
 */
 'use strict';

/*
 * Controller that renders our index (home) page.
 */
function index (request, response) {
  var now = new Date();
  var contextData = {
    'title': 'Wordly',
    'homeActive': true
  };
  response.render('index.html', contextData);
}

module.exports = {
  index: index,
};