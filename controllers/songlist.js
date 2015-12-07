/*
 * CrowdSound - controllers/songlist.js
 * 
 *
 *
 */


/* 
 * Set up database stuff:
 */
var crowdcontrol = require('./crowds.js');
var Firebase = require("firebase");
var pendingDB = new Firebase('https://crowdsound-cpsc439.firebaseio.com/pending');
var playlistDB = new Firebase('https://crowdsound-cpsc439.firebaseio.com/playlist');

/* Handles upvotes (from websocket) */
function upvote(jsonObj) {  


  var thiscrowd = pendingDB.child(jsonObj.crowd_uid);
  var votes = pendingDB.child(jsonObj.crowd_uid).child(jsonObj.song_uid).child("upvotes");
  var oldvotes=0;

  var threshold = crowdcontrol.checkThresh(jsonObj.crowd_uid);


  votes.once('value', function(dataSnapshot){
    oldvotes = dataSnapshot.val();
    votes.set(oldvotes+1);
    if (threshold<=oldvotes+1) {
      console.log("We must move a song!");
      addSongToPlaylist(jsonObj.crowd_uid,jsonObj.song_uid);
      dropSongFromPending(jsonObj.crowd_uid,jsonObj.song_uid);
    }
  });
}

function addSongToPlaylist(crowdUID, songUID) {

  pendingDB.child(crowdUID).child(songUID).once('value', function(nameSnapshot) {
    var val = nameSnapshot.val();
    console.log(val);

    // playlistDB.child(crowdUID).child(songUID).child("uid").set(val.uid);
    // playlistDB.child(crowdUID).child(songUID).child("spotifyURI").set(val.spotifyURI);
    // playlistDB.child(crowdUID).child(songUID).child("image").set(val.image);
    // playlistDB.child(crowdUID).child(songUID).child("name").set(val.name);
    // playlistDB.child(crowdUID).child(songUID).child("artist").set(val.artist);

      var newSong = {
        uid:val.uid,
        spotifyURI:val.spotifyURI,
        image:val.image,
        name:val.name,
        artist:val.artist
      }

      playlistDB.child(crowdUID).push(newSong);
  });
}

function dropSongFromPending(crowdUID, songUID) {
  pendingDB.child(crowdUID).child(songUID).remove();
}

/* Handles new songs */
function addSong(jsonObj) {



  // Get the proper crowd
  var newChild = pendingDB.child(jsonObj.crowd_uid).child(jsonObj.song_uid);
  // Create a child, it will be the song
  // var newChild = thiscrowd.push();
  console.log("data");
  console.log(jsonObj.song_uid);
  console.log(jsonObj.song_name);
  console.log(jsonObj.song_uri);
  console.log(jsonObj.song_artist);
  console.log(jsonObj.song_albumArtURI);
  
  // Parse the new song info, and create a JSON object
  var uid = jsonObj.song_uid;
  var name = jsonObj.song_name;
  var spotifyURI = jsonObj.song_uri;
  var artist = jsonObj.song_artist;
  var image = jsonObj.song_albumArtURI;
  var newentry = {"uid":uid, "upvotes":1, "name":name, "spotifyURI":spotifyURI, "artist":artist, "image":image};
  
  // Set the entry as the new object
  newChild.set(newentry);

  console.log("Song: "+name+" added to crowd "+jsonObj.crowd_uid);
}

/*
 * Export all our functions (controllers in this case, because they
 * handles requests and render responses).
 */
module.exports = {
  'addSong':addSong,
  'upvote':upvote,
  'addsong':addSong
};