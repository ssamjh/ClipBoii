import socket
import keyboard
import time
import pyperclip
import pickle
import os

CONFIG_FILE = "config.pkl"

# Initial values
HOST = ""
PORT = 0
USER = ""
COPY_KEYBIND = ""
PASTE_KEYBIND = ""

# Global socket definition
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Function to load config file if exists


def load_config():
    global HOST, PORT, USER, COPY_KEYBIND, PASTE_KEYBIND
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'rb') as handle:
                config = pickle.load(handle)

            HOST, PORT, USER, COPY_KEYBIND, PASTE_KEYBIND = config['HOST'], config[
                'PORT'], config['USER'], config['COPY_KEYBIND'], config['PASTE_KEYBIND']

            return True
        except:
            # Handle corrupted file
            return False
    else:
        return False

# Functions to ask user for config details


def ask_config_details():
    global HOST, PORT, USER, COPY_KEYBIND, PASTE_KEYBIND

    HOST = input("Enter host:")
    PORT = int(input("Enter port:"))
    USER = input("Enter user name:")
    COPY_KEYBIND = input("Enter copy keybind:")
    PASTE_KEYBIND = input("Enter paste keybind:")

    save_config()

# Function to save config details


def save_config():
    global HOST, PORT, USER, COPY_KEYBIND, PASTE_KEYBIND

    config = {'HOST': HOST, 'PORT': PORT, 'USER': USER,
              'COPY_KEYBIND': COPY_KEYBIND, 'PASTE_KEYBIND': PASTE_KEYBIND}

    with open(CONFIG_FILE, 'wb') as handle:
        pickle.dump(config, handle)

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
    if not load_config():
        ask_config_details()

    client_socket.connect((HOST, PORT))
    print(f"Connected to clipboard server on {HOST}:{PORT}")
    keyboard.add_hotkey(COPY_KEYBIND, perform_set_clipboard)
    keyboard.add_hotkey(PASTE_KEYBIND, perform_get_clipboard_and_paste)
    keyboard.wait('esc')  # Keep waiting for keybinds press


if __name__ == "__main__":
    connect_to_server()
    # Close the socket when done
    client_socket.close()
