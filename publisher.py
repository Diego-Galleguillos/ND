import socket
import threading
import time

class client_manager:
    def __init__(self, id):
        self.id = id
        self.message = "Initial message from server."
        self.old_message = ""

    def modify_message(self, new_message):
        self.message = new_message + str(time.time)
    
    def handle_client(self, client_socket):
        client_socket.settimeout(1.0)  # Set a timeout for the recv method
        try:
            while True:
                try:
                    request = client_socket.recv(1024)
                    if request:
                        print(f"Received from client {self.id}: {request.decode()}")
                        response = f"{self.message} - {request.decode()}"
                        if self.message != self.old_message:
                            client_socket.send(self.message.encode())
                except socket.timeout:
                    # Timeout reached, send a message even if no request received
                        if self.message != self.old_message:
                            client_socket.send(self.message.encode())
                self.old_message = self.message
                time.sleep(1)  # Add a small delay to avoid busy-waiting
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            client_socket.close()

def main():
    con = int(input("Enter the number of connections: "))
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 9999))
    server.listen(6)
    print("Server listening on port 9999")

    clients = []
    client_id = 0
    while client_id < con:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")
        
        client = client_manager(client_id)
        clients.append(client)

        client_handler = threading.Thread(target=client.handle_client, args=(client_socket,))
        client_handler.start()
        client_id += 1
    
    message = input("Enter the new message: ")

    while message != "exit":

        for client in clients:
            message = input(f"Enter the new message for client {client.id}: ")
            client.modify_message(message)
        

if __name__ == "__main__":
    main()

