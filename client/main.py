import socketio
import threading

# Cria um cliente Socket.IO
sio = socketio.Client()

# Identificador do cliente
client_id = None

# Conecta ao servidor
@sio.event
def connect():
    global client_id
    print("Conectado ao servidor!")
    client_id = sio.sid

# Lida com mensagens recebidas
@sio.on('message')
def on_message(data):
    print(f"Mensagem recebida: {data}")

# Lida com mensagens de chat
@sio.on('chat')
def on_chat(data):
    print(f"{data['sender']} diz: {data['message']}")

# Lida com comandos recebidos
@sio.on('command')
def on_command(data):
    print(f"Comando recebido de {data['sender']}: {data['command']}")

# Lida com Easter Eggs
@sio.on('easter_egg')
def on_easter_egg(data):
    print(f"Ação de Easter Egg recebida: {data['action']}")

# Lida com streams de webcam
@sio.on('webcam')
def on_webcam(data):
    print(f"Stream de webcam recebido de {data['sender']} (dados omitidos)")

# Lida com erro
@sio.on('error')
def on_error(data):
    print(f"Erro: {data}")

# Conecta ao servidor
sio.connect('http://localhost:3000')

# Função para enviar mensagens
def send_message():
    while True:
        target = input("Enviar para (all ou ID do cliente): ")
        message = input("Mensagem: ")
        sio.emit('chat', {"target": target, "message": message})

# Função para enviar comandos
def send_command():
    while True:
        target = input("Enviar comando para (ID do cliente): ")
        command = input("Comando: ")
        sio.emit('command', {"target": target, "command": command})

# Menu de opções para o cliente
def menu():
    while True:
        print("\nEscolha uma opção:")
        print("1. Enviar mensagem")
        print("2. Enviar comando")
        print("3. Sair")
        opcao = input("Opção: ")

        if opcao == '1':
            send_message()
        elif opcao == '2':
            send_command()
        elif opcao == '3':
            sio.disconnect()
            break
        else:
            print("Opção inválida. Tente novamente.")

# Executa o menu em uma thread separada
thread = threading.Thread(target=menu)
thread.start()
