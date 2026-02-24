import socket
import threading
import os

HOST = "127.0.0.1"
PORT = 5555
IMAGE_EXTENSIONS = [".png", ".jpg", ".jpeg", ".gif", ".bmp"]

username = input("Choose your username: ")
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

def receive_messages():
    while True:
        try:
            header = b""
            while not header.endswith(b"\n"):
                chunk = client.recv(1024)
                if not chunk:
                    raise ConnectionError()
                header += chunk
            header = header.decode().strip()

            if header == "USERNAME":
                client.send(username.encode())

            elif header.startswith("TEXT|"):
                _, sender, message = header.split("|", 2)
                print(f"{sender}: {message}")

            elif header.startswith("IMAGE|"):
                _, sender, filename, filesize = header.split("|")
                filesize = int(filesize)

                image_data = b""
                while len(image_data) < filesize:
                    chunk = client.recv(min(4096, filesize - len(image_data)))
                    image_data += chunk

                os.makedirs("received_images", exist_ok=True)
                path = f"received_images/{filename}"
                with open(path, "wb") as f:
                    f.write(image_data)

                print(f"{sender} sent an image: {path}")
                os.system(f"open '{path}'")

        except:
            print("Connection closed")
            client.close()
            break

def write_messages():
    while True:
        msg = input()
        if os.path.isfile(msg) and any(msg.lower().endswith(ext) for ext in IMAGE_EXTENSIONS):
            filesize = os.path.getsize(msg)
            filename = os.path.basename(msg)
            header = f"IMAGE|{username}|{filename}|{filesize}\n"
            client.sendall(header.encode())
            with open(msg, "rb") as f:
                while chunk := f.read(4096):
                    client.sendall(chunk)
            print("Image sent!")
        else:
            client.sendall(f"TEXT|{username}|{msg}\n".encode())

threading.Thread(target=receive_messages, daemon=True).start()
threading.Thread(target=write_messages, daemon=True).start()

# Keep main thread alive without hogging CPU
import time
while True:
    time.sleep(1)