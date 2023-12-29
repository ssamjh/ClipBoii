import socket
import keyboard
import time
import pyperclip

# Define the server address
HOST = "172.16.2.20"
PORT = 23156

# Define the user
USER = "Sam"

# Define the keybinds
COPY_KEYBIND = "ctrl+<"
PASTE_KEYBIND = "ctrl+b"

# Global socket definition
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Set up a reusable function to send requests to the server
def send_request_to_server(command, value=""):
    request = f"{command} {USER} {value}"
    client_socket.sendall(request.encode("utf-8"))
    response = client_socket.recv(1024).decode("utf-8")
    return response

def perform_set_clipboard():
    keyboard.press_and_release('ctrl+c')
    time.sleep(0.05)
    clipboard_content = pyperclip.paste()
    send_request_to_server("SetClipboard", clipboard_content)
    print("Sent clipboard contents to server.")

def send_get_request():
    return send_request_to_server("GetClipboard ")

def perform_get_clipboard_and_paste():
    clipboard_content = send_get_request()
    if clipboard_content:
        pyperclip.copy(clipboard_content)
        keyboard.press_and_release('ctrl+v')
        print("Retrieved clipboard contents from the server.")
    else:
        print("No content to paste available.")

def connect_to_server():
    client_socket.connect((HOST, PORT))
    print(f"Connected to clipboard server on {HOST}:{PORT}")
    keyboard.add_hotkey(COPY_KEYBIND, perform_set_clipboard)
    keyboard.add_hotkey(PASTE_KEYBIND, perform_get_clipboard_and_paste)
    keyboard.wait('esc')  # Keep waiting for keybinds press

if __name__ == "__main__":
    connect_to_server()
    # Close the socket when done
    client_socket.close()
