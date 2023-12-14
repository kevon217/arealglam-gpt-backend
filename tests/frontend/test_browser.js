// Create a WebSocket Connection:
// In the JavaScript console, enter the following command to create a new WebSocket connection:

var ws = new WebSocket("ws://localhost:8000/ws");

// Set Up Event Listeners:
// Add event listeners to handle incoming messages and connection errors:
ws.onmessage = function(event) {
    console.log("Received message: " + event.data);
};

ws.onerror = function(error) {
    console.error("WebSocket Error: " + error);
};

ws.onopen = function(event) {
    console.log("WebSocket connection established");
};

ws.onclose = function(event) {
    console.log("WebSocket connection closed");
};

// Send a Test Message:
// Once the WebSocket connection is established ("WebSocket connection established" message appears), send a test message:
ws.send("Hello, WebSocket!");

// Close the Connection:
// When you're done testing, close the WebSocket connection:

ws.close();
