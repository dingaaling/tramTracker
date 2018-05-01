/*
server.js
*/

var express = require('express'); // web server application
var bodyParser = require('body-parser');
var app = express(); // webapp
var http = require('http').Server(app); // connects http library to server
var io = require('socket.io')(http); // connect websocket library to server
var serverPort = 8000;

//---------------------- WEBAPP SERVER SETUP ---------------------------------//
// use express to create the simple webapp
app.use(express.static('public')); // find pages in public directory
app.use(bodyParser.json({ type: 'application/json' }));

// start the server and say what port it is on
http.listen(serverPort, function() {
  console.log('listening on *:%s', serverPort);
});
//----------------------------------------------------------------------------//

//---------------------- REST API COMMUNICATION (web browser)----------------//
// Our handler function is passed a request and response object
app.post('/update', function(req, res) {
  console.log('update route called');
  console.log(req.body)

  var status = req.body.status;
  var value = parseInt(req.body.value);

  if (status == 'UNKNOWN') {
    // TODO:
  }
  else if (status == 'NOW') {
    // TODO:
  }
  else if (status == 'ESTIMATE') {
    // TODO:
  }
  else {
    res.end();
    return;
  }

  io.emit('update',
    status,
    value);

  res.end();
});
//----------------------------------------------------------------------------//

//---------------------- WEBSOCKET COMMUNICATION (web browser)----------------//
// this is the websocket event handler and say if someone connects
// as long as someone is connected, listen for messages
io.on('connect', function(socket) {
  console.log('a user connected');

  // //-- Addition: This function is called when the client clicks on the `Take a picture` button.
  // socket.on('takePicture', function() {
  //   takePicture();
  // });

  // if you get the 'disconnect' message, say the user disconnected
  socket.on('disconnect', function() {
    console.log('user disconnected');
  });
});

function takePicture() {
  // /// First, we create a name for the new picture.
  // /// The .replace() function removes all special characters from the date.
  // /// This way we can use it as the filename.
  // var imageName = new Date().toString().replace(/[&\/\\#,+()$~%.'":*?<>{}\s-]/g, '');
  // var imagePath = 'public/' + imageName;
  // var imageLocation = __dirname + '/' + imagePath + '.jpg';

  // console.log('making a making a picture at ' + imageName); // Second, the name is logged to the console.

  // io.emit('newPicture', (imageName + '.jpg')); /// Lastly, the new name is send to the client web browser.
}
//----------------------------------------------------------------------------//

function calculateCountdown(value) {
  var minutes = Math.floor(value / 60);
  value -= minutes * 60;

  var seconds = value;

  return minutes + " minutes, " + seconds + " seconds";
}