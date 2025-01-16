import socket
import threading

clients = []

# Function to handle client connections
def handle_client(conn, addr):
    print(f"Connection from {addr} has been established.")
    
    # Keep the connection open
    while True:
        try:
            # Receive data from the client
            data = conn.recv(1024).decode()
            if not data:
                break
            print(f"Received data from {addr}: {data}")
        except:
            break
    
    # Close the connection when done
    conn.close()
    clients.remove(conn)
    print(f"Connection from {addr} closed.")

# Function to send messages to all connected clients
def send_messages():
    while True:
        message = input("Enter message to send to all clients: ")
        for conn in clients:
            try:
                conn.send(message.encode())
            except:
                pass

# Set up the server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 12345))  # Bind to all interfaces on port 12345
server_socket.listen(6)  # Allow up to 6 connections

print("Server is listening for connections...")

# Start a thread to handle sending messages from the console
sending_thread = threading.Thread(target=send_messages)
sending_thread.start()

while True:
    # Accept a new connection
    conn, addr = server_socket.accept()
    clients.append(conn)

    # Create a new thread to handle the client
    client_thread = threading.Thread(target=handle_client, args=(conn, addr))
    client_thread.start()
