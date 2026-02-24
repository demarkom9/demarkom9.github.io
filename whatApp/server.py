import socket
import threading
import os

HOST = "127.0.0.1"
PORT = 5555

clients = []
usernames = []

def broadcast(message, sender=None):
    for client in clients:
        if client != sender:
            try:
                client.sendall(message)
            except:
                pass

def handle_client(client):
    while True:
        try:
            # Receive header first (terminated by newline)
            header = b""
            while not header.endswith(b"\n"):
                chunk = client.recv(1024)
                if not chunk:
                    raise ConnectionError()
                header += chunk
            header = header.decode().strip()

            if header.startswith("TEXT|"):
                # Forward to all clients
                broadcast((header + "\n").encode("utf-8"), client)
                print(header.replace("TEXT|", "").replace("|", ": ", 1))

            elif header.startswith("IMAGE|"):
                _, sender, filename, filesize = header.split("|")
                filesize = int(filesize)

                image_data = b""
                while len(image_data) < filesize:
                    chunk = client.recv(min(4096, filesize - len(image_data)))
                    if not chunk:
                        raise ConnectionError()
                    image_data += chunk

                os.makedirs("server_received", exist_ok=True)
                with open(f"server_received/{filename}", "wb") as f:
                    f.write(image_data)

                # Broadcast header + image
                broadcast((header + "\n").encode("utf-8"), client)
                broadcast(image_data, client)

                print(f"{sender} sent image: {filename}")

        except:
            if client in clients:
                idx = clients.index(client)
                clients.pop(idx)
                usernames.pop(idx)
            client.close()
            break

def receive_connections():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print("Server running...")

    while True:
        client, addr = server.accept()
        client.send(b"USERNAME\n")
        username = client.recv(1024).decode().strip()

        clients.append(client)
        usernames.append(username)
        print(f"{username} joined the chat")
        broadcast(f"TEXT|Server|{username} joined\n".encode("utf-8"))

        threading.Thread(target=handle_client, args=(client,), daemon=True).start()

receive_connections()