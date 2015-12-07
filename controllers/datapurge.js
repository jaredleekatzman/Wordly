/*
 * CrowdSound - controllers/datapurge.js
 *    Implementation by Eli Block
 *    (c) 2015
 *
 *    Purges database and re-seeds
 */

 'use strict'

// Set up DB references
var Firebase = require("firebase");
var crowdsDB = new Firebase('https://crowdsound-cpsc439.firebaseio.com/crowds');
var pendingDB = new Firebase('https://crowdsound-cpsc439.firebaseio.com/pending');
var playlistDB = new Firebase('https://crowdsound-cpsc439.firebaseio.com/playlist');

var sl = require("./songlist.js");
var cs = require("./crowds.js");

function purge(request, response) {

	// Remove the data at the base refs of each table
	pendingDB.remove();	
	playlistDB.remove();
	crowdsDB.remove();

	seed();

	response.json({reset:true});
}

function seed() {
	cs.make({crowd_uid:"first_crowd", crowd_name: "CrowdSound Study Sesh", crowd_host: 123, crowd_password: "", crowd_isPrivate: false, crowd_threshold: 3});
	sl.addSong({"crowd_uid":"first_crowd", "song_uri":"spotify:track:2mpsKeLCbdXkwEpZRNi4XD", "upvotes":3, "song_name":"Jubel", "song_uid":"first_song", "song_artist":"Klingande", "song_albumArtURI":"http://"});
	sl.addSong({"crowd_uid":"first_crowd", "song_uri":"spotify:track:3SaIsrEzrQGDcG1jCeaK8q", "upvotes":2, "song_name":"Bang Bang", "song_uid":"second_song", "song_artist":"Jessie J", "song_albumArtURI":"http://"});
}

module.exports = {"purge":purge};