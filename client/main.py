import socketio
import cv2
import base64
import numpy as np
import threading
import time

sio = socketio.Client()

connected_clients = []  # Lista de IDs de clientes conectados
image_queue = []  # Lista para armazenar as imagens recebidas
lock = threading.Lock()  # Para proteger o acesso à lista em threads

def stop_running():
    global running
    running = False

@sio.event
def connect():
    print("Connected to server")
    # sio.emit('get_clients')  # Solicita lista de clientes conectados
    menu()

@sio.event
def receive_image(data):
    """
    Evento chamado ao receber uma imagem.
    """
    img_base64 = data['image']
    with lock:  # Protege o acesso à fila de imagens
        image_queue.append(img_base64)
    print(f"Imagem adicionada à fila. Total na fila: {len(image_queue)}")



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
                frame_share(selected_client)
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

def frame_share(cliente):
    cap = cv2.VideoCapture(0)

    print("Press Q to stop...")
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Codifica a imagem em formato JPEG
        _, buffer = cv2.imencode('.jpg', frame)

        # Converte a imagem para base64
        img_base64 = base64.b64encode(buffer).decode('utf-8')

        # Envia a imagem para o servidor
        sio.emit('send_image', {'to': cliente,'image': img_base64})

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    cap.release()
    cv2.destroyAllWindows()

def process_images():
    """
    Thread que monitora a fila de imagens, decodifica e exibe.
    """
    while True:
        if image_queue:
            with lock:  # Garante que apenas uma thread acesse a fila
                image_data = image_queue.pop(0)  # Remove a imagem mais antiga da fila

            # Decodifica a imagem
            img_buffer = base64.b64decode(image_data)
            img_array = np.frombuffer(img_buffer, dtype=np.uint8)
            img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

            if img is not None:
                cv2.imshow('Recebendo imagens', img)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                print("Erro ao decodificar imagem")
        else:
            time.sleep(0.1)  # Aguarda um pouco se não houver imagens

    cv2.destroyAllWindows()

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

thread = threading.Thread(target=process_images, daemon=True)
thread.start()


sio.connect('https://zany-xylophone-6664p9vgwj63r4rr-3000.app.github.dev/')  # Certifique-se de usar o endereço correto do servidor
sio.wait()



