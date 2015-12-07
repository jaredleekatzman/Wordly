'use strict';

// Include all necessary libraries
var path = require('path');
var logger = require('morgan');
var nunjucks = require('nunjucks');
var bodyParser = require('body-parser');
var strftime = require('strftime');
var express = require('express');

/*
 * Function that configures an application
 *
 */
module.exports = exports = function(yourApp){
  
  // Use 'development' level of logging, ie. verbose
  if (process.env.NODE_ENV !== 'testing') {
    yourApp.use(logger('dev'));
  }

  // Serve images, css, and client-side js about of the
  // directory named 'public'
  yourApp.use(express.static(path.join(__dirname, 'public')));

  // Parse the body of incoming requests by default.
  // This means we can access the parameters of submitted
  // forms and such.
  yourApp.use(bodyParser.urlencoded({extended: true}));
  yourApp.use(bodyParser.json());
};



