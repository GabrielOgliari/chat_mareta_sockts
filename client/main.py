import socketio

sio = socketio.Client()

connected_clients = []  # Lista de IDs de clientes conectados

@sio.event
def connect():
    print("Connected to server")
    # sio.emit('client_message', 'Hello, server!')
    # sio.emit('get_clients')  # Solicita lista de clientes conectados
    menu()

@sio.event
def client_list(data):
    print("Connected clients:")
    global connected_clients
    connected_clients = data
    for idx, client_id in enumerate(connected_clients):
        print(f"{idx + 1}. {client_id}")
    if connected_clients:
        print("concted client?:")
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
        client_index = int(input("Select a client by number: ")) - 1
        if 0 <= client_index < len(connected_clients):
            selected_client = connected_clients[client_index]
        
        print("1. Send message")
        print("2. video call")
        print("3.pranks")
        print("4. Return to menu")
        option = int(input("Select an option: "))
        match option:
            case 1:
                send_mensagem(selected_client)
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
    print(f"Private message from {data['from']}: {data['message']}")

@sio.event
def broadcast_message(data):
    print(f"Received: {data}")

@sio.event
def disconnect():
    print("Disconnected from server")

# def select_and_send_message():
#     try:
#         # Permite ao usuário selecionar um cliente
#         client_index = int(input("Select a client by number: ")) - 1
#         if 0 <= client_index < len(connected_clients):
#             selected_client = connected_clients[client_index]
#             print("Type 'exit' to return to the menu.")
#             input("Press Enter to continue...")
#             while True:
#                 if message == "exit":
#                     break
#                 message = input(f"Enter the message for {selected_client}: ")
#                 sio.emit('private_message', {'to': selected_client, 'message': message})
#         else:
#             print("Invalid selection. Please try again.")
#             select_and_send_message()
#     except ValueError:
#         print("Invalid input. Please enter a valid number.")
#         select_and_send_message()

def send_mensagem(cliente):
    message = ""
    print("Type 'exit' to return to the menu.")
    input("Press Enter to continue...")
    while True:
        if message == "exit":
            break
        message = input(f"Enter the message for {cliente}: ")
        sio.emit('private_message', {'to': cliente, 'message': message})

def menu():
    print("1. Send broadcast message")
    print("2. Get connected clients")
    print("3. Exit")
    try:
        option = int(input("Select an option: "))
        if option == 1:
            message = input("Enter the broadcast message: ")
            sio.emit('broadcast_message', message)
        elif option == 2:
            sio.emit('get_clients')
            
        elif option == 3:
            sio.disconnect()
        else:
            print("Invalid option. Please try again.")
            menu()
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        menu()

sio.connect('https://zany-xylophone-6664p9vgwj63r4rr-3000.app.github.dev')  # Certifique-se de usar o endereço correto do servidor
sio.wait()
menu()

