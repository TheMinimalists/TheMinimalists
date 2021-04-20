import socket
import time
import threading
import os

print("Initialising....\n")

class Client:
    
    def __init__(self, ip_address, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((ip_address, port))
        self.userEntryName=input("Enter username:")
        self.roomEntryName=input("Enter Room name:")
        self.goAhead(self.userEntryName, self.roomEntryName)

        self.receive()
        # self.sendMessage()
            
        

    def goAhead(self, username, room_id=0):
        self.name = username
        self.server.send(str.encode(username))
        time.sleep(0.1)
        self.server.send(str.encode(room_id))
        
        self.login.destroy()
        self.layout()

        rcv = threading.Thread(target=self.receive) 
        rcv.start()
        
    def receive(self):
        while True:
            message = self.server.recv(1024).decode()
            print(message)
            self.msg=input("me:")
            self.msg= self.name+ self.msg
            self.server.send(self.msg.encode())

    # def sendMessage(self): 
    #     while True:  
    #         self.msg=input("me:")
    #         self.msg= self.name+ self.msg
    #         self.server.send(self.msg.encode())
    #         # print(self.name, ":", self.msg)
    #         break
        
        
if __name__ == "__main__":
    host = socket.gethostname()
    ip_address = socket.gethostbyname(host)
    port = enter_port()
    c = Client(ip_address, port)
