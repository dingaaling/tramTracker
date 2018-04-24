/*
client.js
*/

// WebSocket connection setup
var socket = io();

socket.on('update', function(data) {
  console.log("indexjs-update")
  document.getElementById('box1Text').textContent = data;
});