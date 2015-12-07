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


  // Based on this model, define rendering engine
  // from: http://stackoverflow.com/questions/16111386/node-js-cannot-find-module-html
  // var engines = require('consolidate');
  // app.set('views', __dirname + '/views');
  // app.engine('html', engines.mustache);
  // app.set('view engine', 'html');
  yourApp.set('views', __dirname + '/views');

  nunjucks.configure('views', {
    autoescape: true,
    express   : yourApp
  });

  // Parse the body of incoming requests by default.
  // This means we can access the parameters of submitted
  // forms and such.
  yourApp.use(bodyParser.urlencoded({extended: true}));
  yourApp.use(bodyParser.json());
};



