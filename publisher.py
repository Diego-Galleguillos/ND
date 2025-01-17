import socket
import threading

# Function to handle each client connection
def handle_client(client_socket):
    try:
        # Receive and respond to the client
        while True:
            request = client_socket.recv(1024)
            if not request:
                break
            print(f"Received: {request.decode()}")
            client_socket.send(b'ACK')
    finally:
        client_socket.close()

def main():
    # Set up the server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 9999))
    server.listen(6)
    print("Server listening on port 9999")

    # Accept and handle clients
    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    main()
