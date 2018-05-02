/*
client.js
*/

// WebSocket connection setup
var socket = io();

socket.on('update', function(status, countdown) {
  console.log("indexjs-update")

  document.getElementById('status').textContent = status;
  document.getElementById('countdown').textContent = countdown;
});

socket.on('image', function(name, time, direction) {
  console.log("indexjs-image")

  document.getElementById('description').textContent = direction + ' - ' + time;
  document.getElementById('imageContainer').src = name;
});