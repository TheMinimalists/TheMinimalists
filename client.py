import socket, sys, time

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