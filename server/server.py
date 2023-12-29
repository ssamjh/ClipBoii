import socket
import threading

# Define the host and port for the server
HOST = "0.0.0.0"
PORT = 23156

# Clipboard value storage
clipboard_value = ""
clip_lock = threading.Lock()

# Function to handle a client connection
def handle_connection(client_socket):
    while True:
        # Receive data from the client
        data = client_socket.recv(1024).decode("utf-8")
        if not data:
            break  # If no data is received, close the connection

        # Split the received data into command, user and value, handling split errors
        try:
            parts = data.split(" ")
            command, user, value = parts[0], parts[1], " ".join(parts[2:])
        except ValueError:
            client_socket.sendall("Invalid command".encode("utf-8"))
            continue

        # Perform the requested operation
        with clip_lock:
            global clipboard_value
            if command == "SetClipboard":
                clipboard_value = value
                truncated_value = (clipboard_value[:20] + '..') if len(clipboard_value) > 20 else clipboard_value
                print(f"{user} set clipboard to: {truncated_value}")
                client_socket.sendall("Clipboard set successfully".encode("utf-8"))
            elif command == "GetClipboard":
                client_socket.sendall(clipboard_value.encode("utf-8"))
            else:
                client_socket.sendall("Invalid command".encode("utf-8"))

    # Close the client connection
    client_socket.close()

# Function to accept incoming connections
def accept_connections(server_socket):
    while True:
        # Accept a client connection
        client_socket, addr = server_socket.accept()
        print(f"Connected by: {addr}")

        # Handle the connection in a separate thread
        client_thread = threading.Thread(target=handle_connection, args=(client_socket,))
        client_thread.start()

# Start server function
def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))    
        server_socket.listen(5)
        print(f"Clipboard server is running on {HOST}:{PORT}")   

        try:
            accept_connections(server_socket)
        except KeyboardInterrupt:
            server_socket.close()

if __name__ == "__main__":
    start_server()
