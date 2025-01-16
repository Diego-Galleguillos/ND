import socket

# Set up the server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 12345))  # Bind to all interfaces on port 12345
server_socket.listen(1)

print("Server is listening for connections...")

# Accept a connection
conn, addr = server_socket.accept()
print(f"Connection from {addr} has been established.")

# Receive data from the client
data = conn.recv(1024).decode()
print(f"Received data: {data}")

# Send a response back to the client
conn.send("Hello from the server!".encode())

# Close the connection
conn.close()
