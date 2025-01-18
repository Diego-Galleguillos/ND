import socket

# Set up the client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('192.168.86.203', 12345))  # Connect to the server at 192.168.86.211 on port 12345

message = input("Enter message to send to the server: ")
client_socket.send(message.encode())

while True:
    # Send data to the server

    # Receive a response from the server
    data = client_socket.recv(1024).decode()
    print(f"Received data: {data}")

    if not data:
        break

# Close the connection
client_socket.close()
