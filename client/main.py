import socketio
import cv2
import base64

sio = socketio.Client()

connected_clients = []  # Lista de IDs de clientes conectados

@sio.event
def connect():
    print("Connected to server")
    # sio.emit('get_clients')  # Solicita lista de clientes conectados
    menu()
    
@sio.event
def client_list(data):
    print("\nConnected clients:")
    global connected_clients
    connected_clients = data
    for idx, client_id in enumerate(connected_clients):
        print(f"{idx + 1}. {client_id}")
    if connected_clients:
        print("\nDo you want to conect to an client?:")
        print("1. Yes")
        print("2. Return to menu")
        print("3. Refrash")
        response = int(input("Select an option: "))
        match response:
            case 1:
                pass
            case 2:
                menu()
            case 3:
                sio.emit('get_clients')
        client_index = int(input("\nSelect a client by number: ")) - 1
        if 0 <= client_index < len(connected_clients):
            selected_client = connected_clients[client_index]
        
        print("\nOptions: ")
        print("1. send message")
        print("2. Video call")
        print("3. Pranks")
        print("4. Return to menu")
        option = int(input("Select an option: "))
        match option:
            case 1:
                send_message(selected_client)
            case 2:
                print("video call")
            case 3:
                print("pranks")
            case 4:
                menu()
    else:
        print("No clients connected.")

@sio.event
def private_message(data):
    print(f"\nPrivate message from {data['from']}: {data['message']}")

@sio.event
def broadcast_message(data):
    print(f"Received: {data}")

@sio.event
def disconnect():
    print("Disconnected from server")


def send_message(cliente):
    message = ""
    print("Type 'exit' to return to the menu.")
    input("Press Enter to continue...")
    while True:
        message = input(f"Enter the message for {cliente}: ")
        if message == "exit":
            break
        sio.emit('private_message', {'to': cliente, 'message': message})

def menu():
    print("1. Send broadcast message")
    print("2. Get connected clients")
    print("3. Exit")
    try:
        option = int(input("Select an option: "))
        match option:
            case 1:
                message = input("Enter the broadcast message: ")
                sio.emit('broadcast_message', message)
            case 2:
                sio.emit('get_clients')       
            case 3:
                sio.disconnect()
            case _:
                print("Invalid option. Please try again.\n")
                menu()
            
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        menu()

sio.connect('https://zany-xylophone-6664p9vgwj63r4rr-3000.app.github.dev/')  # Certifique-se de usar o endereço correto do servidor
sio.wait()
menu()

