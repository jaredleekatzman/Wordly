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

// connect sockets to it
var io = require('socket.io')(http);

// Get config variables
// var port = 8080;
var host = process.env.IP;

// Start the server
http.listen(port, function() {

    // We're running, print the port number.
    console.log('Your app is running on PORT ', port);
  
});

// Dependencies
var Firebase = require("firebase");
var crowdsDB = new Firebase('https://crowdsound-cpsc439.firebaseio.com/crowds');
var playlistsDB = new Firebase('https://crowdsound-cpsc439.firebaseio.com/playlist');
var pendingsDB = new Firebase('https://crowdsound-cpsc439.firebaseio.com/pending');

// Controllers
var crowds = require('./controllers/crowds.js');
var sl = require('./controllers/songlist.js');

// If a socket is connected to:
io.on('connection', function(socket){
    console.log("A socket was activated");
    // keep socket active. 

    // Test code with chat messages:
    socket.on('chat message', function(msg){
        console.log("message received:"+msg);
        io.emit('chat message', msg);
        sl.test(msg);
    }); 

    // Process downVotes
    socket.on('upVote', function(jsonObj){
        console.log("new upvote:"+ jsonObj.toString());
        sl.upvote(jsonObj);
    });

    // Process newPending songs added
    socket.on('newPending', function(jsonObj){
        console.log("new pending song received: "+jsonObj.toString()+"\nNow trying to add it...");
        sl.addsong(jsonObj);
    });

    // Process newCrowd added
    socket.on('newCrowd', function(jsonObj){
        console.log("new crowd created"+jsonObj.toString());
        crowds.make(jsonObj);
    });
    
    crowdsDB.once('value', function(childSnapshot, prevChildName) {
        console.log('init load of crowds');
        socket.emit('updated crowds', childSnapshot.val());
    });

    pendingsDB.once('value', function(childSnapshot, prevChildName) {
        console.log('init load of pending');
        socket.emit('updated pendings', childSnapshot.val());
    });

    playlistsDB.once('value', function(childSnapshot, prevChildName) {
        console.log('init load of playlists');
        socket.emit('updated playlists', childSnapshot.val());
    });
});

crowdsDB.on('value', function(childSnapshot, prevChildName) {
    console.log('crowd child callback');
    io.emit('updated crowds', childSnapshot.val());
});

pendingsDB.orderByChild("upvotes").limitToLast(50).on('value', function(childSnapshot, prevChildName) {
    console.log('pendings callback');
    console.log('\nORDER BY VOTE:\n');
    console.log(childSnapshot.val());
    io.emit('updated pendings', childSnapshot.val());
});

playlistsDB.orderByKey().limitToLast(50).on('value', function(childSnapshot, prevChildName) {
    console.log('playlist callback');
    console.log('\nORDER CHRONOLOGICALLY:\n');
    console.log(childSnapshot.val());
    io.emit('updated playlists', childSnapshot.val());
});

