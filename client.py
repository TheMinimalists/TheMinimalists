# client.py
import time, socket, sys

print("\nWelcome to Chat Room\n")
print("Initialising....\n")
time.sleep(1)

listensocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
shost = socket.gethostname()
ip = socket.gethostbyname(shost)
print(shost, "(", ip, ")\n")
host = input(str("Enter server address: "))
name = input(str("\nEnter your name: "))
port = int(input("Enter Port Number: "))
print("\nTrying to connect to ", host, "(", port, ")\n")
time.sleep(1)
listensocket.connect((host, port))
print("Connected...\n")

listensocket.send(name.encode())
s_name = listensocket.recv(1024)
s_name = s_name.decode()
print(s_name, "has joined the chat room\nEnter [exit] to exit chat room\n")
while True:
    message = listensocket.recv(1024)
    message = message.decode()
    print(s_name, ":", message)
    message = input(str("Me : "))
    if message == "[e]":
        message = "Left chat room!"
        listensocket.send(message.encode())
        print("\n")
        break
    listensocket.send(message.encode())