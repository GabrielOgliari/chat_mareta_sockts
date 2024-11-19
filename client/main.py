import socket

def main():
    # Configurações do servidor
    host = 'localhost'  # Endereço do servidor
    port = 3000        # Porta do servidor

    # Cria um socket TCP/IP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Conecta ao servidor
        client_socket.connect((host, port))
        print("Conectado ao servidor.")

        while True:
            # Recebe dados do servidor
            data = client_socket.recv(1024)
            if not data:
                break
            print(f"Mensagem recebida: {data.decode()}")

    except Exception as e:
        print(f"Erro: {e}")

    finally:
        # Fecha a conexão
        client_socket.close()
        print("Desconectado do servidor.")

if __name__ == "__main__":
    main()