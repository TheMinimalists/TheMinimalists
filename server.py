import socket 
from _thread import *
import sys
from collections import defaultdict as df
import time

print("Initialising......")
print("\n\33[34m\33[1m Welcome to Minimal Chat Room \33[0m\n")

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

            start_new_thread(self.clientThread, (connection,))

        self.server.close()

    
    def clientThread(self, connection):
        user_id = connection.recv(1024).decode().replace("User ", "")
        room_id = connection.recv(1024).decode().replace("Join ", "")

        if room_id not in self.rooms:
            connection.send("New Group Created".encode())
            # connection.send("\nYou Are Admin".encode())
            # admin = user_id

        else:
            connection.send("Welcome to Minimal Chat Room".encode())
            # connection.send(admin + "is Admin".encode())
        self.rooms[room_id].append((connection,user_id))
        print(self.rooms)

        while True:
            try:
                message = connection.recv(1024)
                print(str(message.decode()))
                if message:
                    if str(message.decode()) == "FILE":
                        self.broadcastFile(connection, room_id, user_id)
	                
                    elif (str(message.decode()) == "/All") :
                        all_list = [client[1] for client in self.rooms[room_id]]
                        print(all_list)
                        message_to_send = "<MinimalBot> " + "All user:  " + str(all_list)
                        self.broadcast(message_to_send, connection, room_id)                       
                    else:
                        message_to_send = "<" + str(user_id) + "> " + message.decode()
                        self.broadcast(message_to_send, connection, room_id)

                else:
                    self.remove(connection, room_id)
            except Exception as e:
                message_to_send = "<" + str(user_id) + " left the chat" + "> "
                self.broadcast(message_to_send, connection, room_id)
                print("Client disconnected")
                print(e)
                break
    
    
    def broadcastFile(self, connection, room_id, user_id):
        file_name = connection.recv(1024).decode()
        lenOfFile = connection.recv(1024).decode()
        for client in self.rooms[room_id]:
            if client != connection:
                try: 
                    client.send("FILE".encode())
                    time.sleep(0.1)
                    client.send(file_name.encode())
                    time.sleep(0.1)
                    client.send(lenOfFile.encode())
                    time.sleep(0.1)
                    client.send(user_id.encode())
                except:
                    client.close()
                    self.remove(client, room_id)

        total = 0
        print(file_name, lenOfFile)
        while str(total) != lenOfFile:
            data = connection.recv(1024)
            total = total + len(data)
            for client in self.rooms[room_id]:
                if client != connection:
                    try: 
                        client.send(data)
                        # time.sleep(0.1)
                    except:
                        client.close()
                        self.remove(client, room_id)
        print("Sent")



    def broadcast(self, message_to_send, connection, room_id):
        for client in self.rooms[room_id]:
            print(client)
            if client[0] != connection:
                try:
                    client[0].send(message_to_send.encode())
                except:
                    client[0].close()
                    self.remove(client, room_id)

    
    def remove(self, connection, room_id):
        if connection in self.rooms[room_id]:
            self.rooms[room_id].remove(connection)



if __name__ == "__main__":
    ip_address = "127.0.0.1"
    port = 12345

    s = Server()
    s.accept_connections(ip_address, port)
