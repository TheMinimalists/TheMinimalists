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
        self.admins = df(list)
        self.wait_list=df(list)
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
    
    def Accept_client(self, username,room_id):
        for client in self.wait_list[room_id]:
             if(username == client[1]):
                 self.wait_list[room_id].remove(client)
                 self.rooms[room_id].append(client)
                 client[0].send("$Accepted".encode())
            

    
    def clientThread(self, connection):

        user_id = connection.recv(1024).decode()
        room_id = connection.recv(1024).decode()

        if room_id not in self.rooms:
            connection.send("$Accepted".encode())
            time.sleep(2)
            connection.send("New Group Created".encode())
            connection.send("You Are Admin!".encode())
            connection.send("\nTo view options type '/Options'".encode())
            self.admins[room_id].append((connection,user_id))
            self.rooms[room_id].append((connection,user_id))

        else:
            self.wait_list[room_id].append((connection,user_id))
            self.broadcast_to_admins("New User Request Detected",connection,room_id)
            connection.send("$wait".encode())
        print(self.rooms)

        while True:
            try:
                message = connection.recv(1024)
                message= str(message.decode())
                if message:
                    if message == "FILE":
                        self.broadcastFile(connection, room_id, user_id)
	                
                    elif message == "/All" :
                        all_list = [client[1] for client in self.rooms[room_id]]
                        print(all_list)
                        message_to_send = "<MinimalBot> " + "All users:  " + str(all_list)
                        if(connection in self.admins[room_id][0]):
                            self.broadcast_to_admins(message_to_send, connection, room_id)
                        else:
                            self.send_to_user(message_to_send,connection,room_id) 

                    elif (message.split()[0] == "/Accept") :
                        if(connection in self.admins[room_id][0]):
                            self.Accept_client(message.split()[1],room_id)
                        else:
                            msg="You are not an admin"
                            print(msg)
                            self.send_to_user(msg,connection,room_id)                             
                    elif message == "/Viewadmin" :
                        print("admins printed ")
                        admin_list=[client[1] for client in self.admins[room_id]]
                        msg = "<MinimalBot> " + "Admin of the group is:  " + str(admin_list)
                        print(msg)
                        self.send_to_user(msg,connection,room_id) 
                    elif message == "/Waitlist":
                        waiting_list=[client[1] for client in self.wait_list[room_id]]
                        msg = "<MinimalBot> " + "All Requests:  " + str(waiting_list)
                        print(msg)
                        self.send_to_user(msg,connection,room_id)

                    elif message == "/Options" :                        
                        if(connection in self.admins[room_id][0]):                            
                            mesg = "<MinimalBot> " + ''' /All - To view all members in the group
                        /Remove - To remove any member from the group
                        /TransferAdmin - To transfer the adminship
                        /Accept - To Accept joining request
                        /Waitlist - To view the waiting list of clients'''                            
                            self.broadcast_to_admins(mesg, connection, room_id)                        
                        else:                            
                            mesg = "<MinimalBot> " + ''' /All - To view all members in the group
                        /Viewadmin - To view admin of the group'''                            
                            self.send_to_user(mesg,connection,room_id)  

                    elif(message.split()[0] == "/Remove"):
                        if(connection in self.admins[room_id][0]):
                            for client in self.rooms[room_id]:
                                if(message.split()[1] == client[1]):
                                    self.rooms[room_id].remove(client)
                                    client[0].send("$Removed".encode())
                                    client[0].close()
                                    self.remove(client[0], room_id)
                        else:
                            msg="You are not an admin"
                            print(msg)
                            self.send_to_user(msg,connection,room_id) 

                    elif (message.split()[0] == "/TransferAdmin") :
                        if(connection in self.admins[room_id][0]):
                            for client in self.rooms[room_id]:
                                if(message.split()[1] == client[1]):
                                    self.admins[room_id].remove(self.admins[room_id][0])
                                    self.admins[room_id].append(client)
                                    client[0].send("$You are admin now!".encode())

                        else:
                            msg="You are not an admin"
                            print(msg)
                            self.send_to_user(msg,connection,room_id)
                         
                    else:
                        message_to_send = "<" + str(user_id) + "> " + message
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
            if client[0] != connection:
                try: 
                    client[0].send("FILE".encode())
                    time.sleep(0.1)
                    client[0].send(file_name.encode())
                    time.sleep(0.1)
                    client[0].send(lenOfFile.encode())
                    time.sleep(0.1)
                    client[0].send(user_id.encode())
                except:
                    client[0].close()
                    self.remove(client, room_id)

        total = 0
        print(file_name, lenOfFile)
        while str(total) != lenOfFile:
            data = connection.recv(1024)
            total = total + len(data)
            for client in self.rooms[room_id]:
                if client[0] != connection:
                    try: 
                        client[0].send(data)
                        # time.sleep(0.1)
                    except:
                        client[0].close()
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

    def send_to_user(self, message_to_send, connection, room_id):
        try:
            connection.send(message_to_send.encode())
        except:
            connection.close()
            self.remove(connection, room_id)

    def broadcast_to_admins(self, message_to_send,connection, room_id):
        for client in self.admins[room_id]:
            print(client)
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
