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

// var PythonShell = require('python-shell');

var cp = require('child_process');
var rnn;

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

function init (request, response) {

  console.log("sending");

  rnn = cp.spawn('python', ['Word_Model/Model/Wordly_Init.py'], {
    stdio:[null, null, null, 'ipc']
  });

  console.log("waiting");

  rnn.stderr.on('data',
    function (data) {
        console.log('err data: ' + data);
    }
);

  rnn.stdout.on('data',
    function (data) {
    var contextData = {
      'title': 'Wordly',
      'homeActive': true
      // 'query': data
    };
    console.log("Query: " + contextData.query);
    response.render('index.html', contextData);      
        console.log('out data: ' + data);
    }
);

  // rnn.on('message', function(message) {
  //   var contextData = {
  //     'title': 'Wordly',
  //     'homeActive': true,
  //     'query': message,
  //   };
  //   console.log("Query: " + contextData.query);
  //   response.render('index.html', contextData);
  // });

}

module.exports = {
  "index": index,
  "query": query,
  "init": init
};