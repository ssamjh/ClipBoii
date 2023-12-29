# Clipboii App

Hey there! Welcome to the Clipboii app. This little project lets you share your clipboard stuff between a server and a client. Cool, right? It's all done with Python and Docker.

## What's Inside

1. `client.py`: This is where the magic happens on the client side.
2. `server.py`: This is the server part that catches what the client sends.
3. `docker-compose.yaml`: Makes it super easy to run everything with Docker.

## Getting Started

It's pretty easy to get started:

1. Make sure you've got Docker on your computer.
2. Get these files onto your computer (maybe download or clone them?).
3. Run `docker-compose up -d` in your terminal, and the server will start.

## How to Use

Once your server is up and running, just start the client script on a different machine. It'll connect to the server and start sharing clipboard content. Make sure you specify unique usernames for each client.

## Stuff You Need

- Python 3
- Docker and Docker Compose
- Both the server and client need to be connected to a network etc