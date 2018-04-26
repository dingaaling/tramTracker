/*
client.js
*/

// WebSocket connection setup
var socket = io();

socket.on('update', function(departingTime, departingCountdown, arrivingTime, arrivingCountdown) {
  console.log("indexjs-update")

  document.getElementById('departingTime').textContent = departingTime;
  document.getElementById('departingCountdown').textContent = departingCountdown;

  document.getElementById('arrivingTime').textContent = arrivingTime;
  document.getElementById('arrivingCountdown').textContent = arrivingCountdown;
});