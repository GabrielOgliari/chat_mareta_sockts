import socketio

sio = socketio.Client()

@sio.event
def connect():
    print("Connected to server")
    sio.emit('client_message', 'Hello, server!')

@sio.event
def broadcast_message(data):
    print(f"Received: {data}")

@sio.event
def disconnect():
    print("Disconnected from server")
    
sio.connect('https://literate-space-journey-px46pw6w9grh6j5j-3000.app.github.dev/')
sio.wait()