import socketio

sio = socketio.Client()

@sio.event
def connect():
    print("Connected to server")
    sio.emit('client_message', 'Hello, server!')

@sio.event
def server_message(data):
    print(f"Received: {data}")

@sio.event
def disconnect():
    print("Disconnected from server")

sio.connect('http://localhost:3000')
sio.wait()