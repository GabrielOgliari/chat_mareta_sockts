import socketio

sio = socketio.Client()

@sio.event
def connect():
    print("Conectado ao servidor.")

@sio.event
def message(data):
    print(f"Mensagem recebida: {data}")
    
@sio.event
def disconnect():
    print("Desconectado do servidor.")
try:

    sio.connect('http://localhost:3000')
    print("Conexão bem-sucedida!")

    sio.emit('custom_event', {'message': 'Olá do cliente Python!'})

    sio.wait()

except Exception as e:
    print(f"Erro ao conectar: {e}")
