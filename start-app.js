/*
 * CrowdSound - start-app.js
 *    Implementation by Eli Block and Tim Follo, based on source code by Kyle Jensen
 *    (c) 2015
 *
 *    Starts app, and defines socket methods
 */

 'use strict';

// configure application routes
// make application availiable in this context
var app = require('./app.js');
var port = require('./port.js');

// setup http server
var http = require('http').Server(app);

// Get config variables
// var port = 8080;
var host = process.env.IP;

// Start the server
http.listen(port, function() {

    // We're running, print the port number.
    console.log('Your app is running on PORT ', port);
  
});

