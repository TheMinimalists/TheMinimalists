import time, socket, sys

print("\nWelcome to Minimal Chat Room\n")
print("Initialising....\n")
time.sleep(1)

listensocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
ip = socket.gethostbyname(host)
port = int(input("Enter Port Number: "))
listensocket.bind((host, port))
print(host, "(", ip, ")\n")
name = input(str("Enter your name: "))
           
listensocket.listen(1)
print("Waiting for client")
conn, addr = listensocket.accept()
print("Received connection from ", addr[0], "(", addr[1], ")\n")

s_name = conn.recv(1024)
s_name = s_name.decode()
print(s_name, "has connected to the Minimal Chat Room\nEnter exit$ to exit Minimal Chat Room\n")
conn.send(name.encode())
while True:
    message = input(str("Me : "))
    if message == "exit$":
        message = s_name + " left chat room!"
        conn.send(message.encode())
        print("\n")
        break
    conn.send(message.encode())
    message = conn.recv(1024)
    message = message.decode()
    print(s_name, ":", message)
