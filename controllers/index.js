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
var io = require('socket.io')(8000);
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

  // Phase 1
  var result;

  rnn = cp.spawn('python', ['Word_Model/Model/Wordly_Init.py', request.body.query], {
   detached: true,
   stdio:[null, null, null, 'ipc']
 });

  rnn.stderr.on('data',
    function (data) {
        console.log('err data: ' + data);
    }
  );

  io.sockets.on('connection', function (socket) {
    socket.on('test', function(data) {
          console.log('socket: ' + data);
    });

    socket.on('result', function(data) {
          console.log('socket: ' + data);
          var result = JSON.parse(data)
/////////////////////////////////////////////////////////
            var contextData = {
              'title': 'Wordly',
              'homeActive': true,
              'query': request.body.query,
              'result': result.best,
              'explain': result,
              'display': (request.body.query == "") ? "hide" : ""
            };
            console.log("DATA: " + typeof data);
            console.log("DATA: " + data);
            console.log("Query: " + contextData.query);
            console.log("Result: " + contextData.result);
            console.log("Show Results? " + contextData.display);
            response.render('index.html', contextData);
/////////////////////////////////////////////////////////
    
    });
  });

  rnn.on('close', function (code) {
      console.log('child process exited with code ' + code);
  });

  rnn.stdout.on('data',
    function (data) {
      result = data;
      console.log('out data: ' + data);
  });

  // var contextData = {
  //   'title': 'Wordly',
  //   'homeActive': true,
  //   'query': request.body.query,
  //   'result': result,
  //   'display': (request.body.query == "") ? "hide" : ""
  // };
  // console.log("Query: " + contextData.query);
  // console.log("Result: " + contextData.result);
  // console.log("Show Results? " + contextData.display);
  // response.render('index.html', contextData);
}

// Phase 2
function init (request, response) {

  console.log("sending");

  rnn = cp.spawn('python', ['-i','Word_Model/Model/Wordly_Init.py'], {
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
      console.log('out data: ' + data);
  });

    var contextData = {
      'title': 'Wordly',
      'homeActive': true,
      'display': "hide" 
    };
    response.render('index.html', contextData);      
}

module.exports = {
  "index": index,
  "query": query,
  "init": init
};