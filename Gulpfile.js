/*
 * CrowdSound - Gulpfile.js
 *    Implementation based on source code by Kyle Jensen
 *    (c) 2015
 *
 *    Renders about page
 */
 // Gulpfile.js - We use Gulp to monitor our files and
// do two things when we make changes to the code:
// 1) check it for errors ("lint it") and 2) restart
// the application.

'use strict';

var gulp = require('gulp');
var nodemon = require('gulp-nodemon');
var jshint = require('gulp-jshint');

gulp.task('lint', function () {
  gulp.src(['*.js', 'controllers/**/*.js', 'models/**/*.js', '!./node_modules/**', '!./.*'])
    .pipe(jshint())
    .pipe(jshint.reporter('jshint-stylish'));
});

gulp.task('default', function () {
  nodemon({
      script: 'start-app.js',
      ext: 'js html',
      ignore: ['node_modules/**', '.c9/*']
    })
    .on('change', ['lint'])
    .on('restart', function () {
      console.log('restarted!');
    });
});

