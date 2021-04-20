import socket, sys
from collections import defaultdict as df

print("\n\33[34m\33[1m Welcome to Minimal Chat Room \33[0m\n")
print("Initialising....\n")

def check_port(port):
    if(port>3000):
        return True
    else:
        print("Others might be using this.Why not use above 3000?")
        return enter_port()
def enter_port():
    port = int(input("Enter Port Number: "))
    if(check_port(port)):
        return port

class Server:
    def __init__(self):
        self.rooms = df(list)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        


    def accept_connections(self, ip_address, port):
        self.ip_address = ip_address
        self.port = port
        self.server.bind((self.ip_address, int(self.port)))
        self.server.listen(100)

        while True:
            connection, address = self.server.accept()
            print(str(address[0]) + ":" + str(address[1]) + " Connected")
            self.Clients(connection)
            
        self.server.close()

    
    def Clients(self, connection):
        user_id = connection.recv(1024).decode()
        room_id = connection.recv(1024).decode()
        print(user_id,room_id)
        # welcome=f"{user_id} welcome to{room_id}"
        # self.broadcast(welcome, connection, room_id)
        if room_id not in self.rooms:
            connection.send("New Group created".encode())
        else:
            connection.send("Welcome to Minimal Chat Room".encode())

        self.rooms[room_id].append(connection)

        while True:
            try:
                message = connection.recv(1024)
                print(str(message.decode()))
                if message:
                    message_to_send = "<" + str(user_id) + "> " + message.decode()
                    self.broadcast(message_to_send, connection, room_id)

                else:
                    print("No message here")
            except Exception as e:
                message_to_send = "<" + str(user_id) + " left the chat" + "> "
                self.broadcast(message_to_send, connection, room_id)
                print("Client disconnected")
                break


    def broadcast(self, message_to_send, connection, room_id):
        for client in self.rooms[room_id]:
            if client != connection:
                try:
                    client.send(message_to_send.encode())
                except:
                    client.close()


if __name__ == "__main__":
    host = socket.gethostname()
    ip_address = socket.gethostbyname(host)
    port = enter_port()
    
    s = Server()
    s.accept_connections(ip_address, port)
