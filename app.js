/*
 * CrowdSound - app.js
 *    Implementation by Eli Block and Tim Follo, based on source code by Kyle Jensen
 *    (c) 2015
 *
 *    Defines http app configuration
 */

'use strict';

// Import our express and our configuration
var express = require('express');
var configure = require('./config.js');
var apn = require('apn');

// Create our express app
var app = express();

// Configure it
configure(app);

// ADD ROUTES LIKE THIS
//var purger = require('./controllers/datapurge.js');
//app.get('/database/purgedatabase/yes',purger.purge);

module.exports = app;
