/*
client.js
*/

// WebSocket connection setup
var socket = io();

socket.on('update', function(departingStatus, departingValue) {
  console.log("indexjs-update")

  document.getElementById('departingStatus').textContent = departingStatus;
  document.getElementById('departingValue').textContent = departingValue;
});