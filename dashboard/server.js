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
  console.log(req.body);

  var status = req.body.status;
  var countdownValue = parseInt(req.body.countdown);
  var countdown = '';

  if (status == 'UNKNOWN') {
    countdown = '';
  }
  else if (status == 'DOCKED') {
    countdown = formatSeconds(countdownValue);
    status = 'Now';
  }
  else if (status == 'ESTIMATE') {
    countdown = formatSeconds(countdownValue);
    status = 'Next Arrival';
  }
  else {
    res.end();
    return;
  }

  io.emit('update', status, countdown);

  res.end();
});

app.post('/image', function(req, res) {
  console.log('image route called');
  console.log(req.body)

  var name = req.body.name;
  var time = req.body.time;
  var direction = req.body.direction;

  io.emit('image', name, time, direction);

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
//----------------------------------------------------------------------------//

function formatSeconds(value) {
  var sign = '';
  if (value < 0) {
    sign = 'Delayed: ';
  }

  value = Math.abs(value);

  // Calculate minutes
  var minutes = Math.floor(value / 60);
  value -= minutes * 60;

  // Calculate seconds
  var seconds = value;

  return sign + minutes + " minutes, " + seconds + " seconds";
}