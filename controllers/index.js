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
require

function index (request, response) {
  var now = new Date();
  var contextData = {
    'title': 'Wordly',
    'homeActive': true,
    'display': "hide"
  };
  response.render('index.html', contextData);
}

function query (request, response) {
  var contextData = {
    'title': 'Wordly',
    'homeActive': true,
    'query': request.body.query,
    'display': (request.body.query == "") ? "hide" : ""
  };
  console.log("Query: " + contextData.query);
  console.log("Show Results? " + contextData.display);
  response.render('index.html', contextData);
}

module.exports = {
  "index": index,
  "query": query
};