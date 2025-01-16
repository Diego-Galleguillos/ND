import socket

# Set up the client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('192.168.86.211', 12345))  # Replace 'server_ip_address' with the server's IP

# Send data to the server
client_socket.send("Hello from the client!".encode())

# Receive a response from the server
data = client_socket.recv(1024).decode()
print(f"Received data: {data}")

# Close the connection
client_socket.close()
