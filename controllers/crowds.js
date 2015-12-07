/*
 * CrowdSound - crowds.js
 *    Implementation by Eli Block and Tim Follo, based on source code by Kyle Jensen
 *    (c) 2015
 *
 *    sets up methods to controll crowds and their lists
 */

/* 
 * set up database stuff:
 */
var Firebase = require("firebase");
var crowdsDB = new Firebase('https://crowdsound-cpsc439.firebaseio.com/crowds');
var pendingDB = new Firebase('https://crowdsound-cpsc439.firebaseio.com/pending');
var playlistDB = new Firebase('https://crowdsound-cpsc439.firebaseio.com/playlist');

// get handle for songlist controller
var songlistc = require('./songlist.js');

// push to db
function toDB(newCrowd){
  var thiscrowd = crowdsDB.child(newCrowd.crowdUID);
  thiscrowd.set(JSON.parse(JSON.stringify(newCrowd)));
}

// used by socket
function makeCrowd(jsonObj){

  var newCrowd = {
    crowdUID: jsonObj["crowd_uid"],
    name: jsonObj["crowd_name"],
    hostUID: jsonObj["crowd_host"],
    password: jsonObj["crowd_password"],
    is_private: jsonObj["crowd_isPrivate"],
    threshold: jsonObj["crowd_threshold"]
  };

  console.log("crowd Creation");
  console.log(newCrowd);

  /* When a new CROWD is created, a new songlist should also be created */
  // The below code is hacky (and doesn't fit our scheme) 
  // Logic could be separated in future ???

  var thiscrowd = pendingDB.child(newCrowd.crowdUID);
  thiscrowd.set({ "crowdUID":newCrowd.crowdUID} );

  var thiscrowd = playlistDB.child(newCrowd.crowdUID);
  thiscrowd.set({ "crowdUID":newCrowd.crowdUID} );

  toDB(newCrowd);
}

function checkThresh(crowdUID) {
  console.log("Checking the threshold in crowd "+crowdUID);
  var thisThreshold = crowdsDB.child(crowdUID).child("threshold");
  var thresh=0;
  thisThreshold.once('value', function(dataSnapshot){
    thresh = dataSnapshot.val();
    return thresh;
  });
  return thresh;

}

/*
 * Export all our functions (controllers in this case, because they
 * handles requests and render responses).
 */
module.exports = {
  'make':makeCrowd,
  'checkThresh':checkThresh
};