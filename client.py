import socket, sys

def check_port(port):
    if(port>3000):
        return True
    else:
        print("Might be busy.Try above 3000")
        return enter_port()
def enter_port():
    port = int(input("Enter Port Number: "))
    if(check_port(port)):
        return port

print("\n\33[34m\33[1m Welcome to Minimal Chat Room \33[0m\n")
print("Initialising....\n")

listensocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
shost = socket.gethostname()
ip = socket.gethostbyname(shost)
print(shost, "(", ip, ")\n")
host = input(str("Enter server address: "))
port=enter_port()
name = input(str("\nEnter your name: "))
print("\nTrying to connect to ", host, "(", port, ")\n")

listensocket.connect((host, port))
print("Connected...\n")

listensocket.send(name.encode())
s_name = listensocket.recv(1024)
s_name = s_name.decode()
print(s_name, "has joined the Minimal Chat Room\nEnter exit$ to exit Minimal Chat Room\n")
while True:
    message = listensocket.recv(1024)
    message = message.decode()
    print(s_name, ":", message)
    message = input(str("Me : "))
    if message == "exit$":
        message = "\33[31m\33[1m $left chat room!$ \33[0m"
        listensocket.send(message.encode())
        print("\n")
        break
    listensocket.send(message.encode())
