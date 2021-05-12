import socket
import tkinter as tk
from tkinter import font
from tkinter import ttk
from tkinter import filedialog
import time
import threading
import os

print("\n\33[34m\33[1m Welcome to Minimal Chat Room \33[0m\n")
print("Initialising....\n")

class GUI:
    
    def __init__(self, ip_address, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((ip_address, port))

        self.Window = tk.Tk()
        self.Window.withdraw()

        self.login = tk.Toplevel()

        self.login.title("Login")
        self.login.resizable(width=False, height=False)
        self.login.configure(width=400, height=350, bg="thistle4", highlightthickness=1, highlightcolor= "black")

        self.pls = tk.Label(self.login, 
                            text="Login to a Minimal Chatroom", 
                            justify=tk.CENTER,
                            font="Helvetica 13 bold", bg="thistle4")

        self.pls.place(relheight=0.15, relx=0.2, rely=0.07)

        self.userLabelName = tk.Label(self.login, text="Username: ", font="Helvetica 12 bold", bg="thistle4")
        self.userLabelName.place(relheight=0.2, relx=0.1, rely=0.25)

        self.userEntryName = tk.Entry(self.login, font="Helvetica 12")
        self.userEntryName.place(relwidth=0.4 ,relheight=0.1, relx=0.35, rely=0.30)
        self.userEntryName.focus()

        self.roomLabelName = tk.Label(self.login, text="Room Id: ", font="Helvetica 12 bold", bg="thistle4")
        self.roomLabelName.place(relheight=0.2, relx=0.1, rely=0.40)

        self.roomEntryName = tk.Entry(self.login, font="Helvetica 12")
        self.roomEntryName.place(relwidth=0.4 ,relheight=0.1, relx=0.35, rely=0.45)
        
        self.go = tk.Button(self.login, 
                            text="CONTINUE", 
                            font="Helvetica 12 bold", 
                            command = lambda: self.goAhead(self.userEntryName.get(), self.roomEntryName.get()))
        
        self.go.place(relx=0.35, rely=0.62)
        self.userStatus = tk.Label(self.login, text="", font="Helvetica 12", bg="thistle4")
        self.userStatus.place(relwidth=0.5 ,relheight=0.1, relx=0.35, rely=0.72)
        # self.label.configure(text="Text Updated")
        self.Window.mainloop()


    def goAhead(self, username, room_id=0):
        self.userStatus.configure(text="Waiting to be accepted..")
        self.name = username
        self.room_id=room_id
        self.server.send(str(username).encode())
        time.sleep(0.1)
        self.server.send(str(room_id).encode())
        rcv = threading.Thread(target=self.receive) 
        rcv.start()
        
    def layout(self):
        self.Window.deiconify()
        self.Window.title("MINIMAL CHAT ROOM")
        self.Window.resizable(width=False, height=False)
        self.Window.configure(width=470, height=550, bg="thistle4")
        self.chatBoxHead = tk.Label(self.Window, 
                                    bg = "thistle4", 
                                    fg = "gray1", 
                                    text = "Username : "+self.name+"          Room Name : "+self.room_id+"", 
                                    font = "Helvetica 14", 
                                    pady = 5)

        

        self.chatBoxHead.place(relwidth = 1)

        self.line = tk.Label(self.Window, width = 440, bg = "gainsboro") 
		
        self.line.place(relwidth = 1, rely = 0.07, relheight = 0.012) 
		
        self.textCons = tk.Text(self.Window, 
                                width=20, 
                                height=2, 
                                bg="thistle4", 
                                fg="gray1", 
                                font="Helvetica 11", 
                                padx=5, 
                                pady=5) 
		
        self.textCons.place(relheight=0.745, relwidth=1, rely=0.08) 
		
        self.labelBottom = tk.Label(self.Window, bg="gainsboro", height=55) 
		
        self.labelBottom.place(relwidth = 1, 
							    rely = 0.8) 
		
        self.entryMsg = tk.Entry(self.labelBottom, 
                                bg = "thistle4", 
                                fg = "gray1", 
                                font = "Helvetica 11")
        self.entryMsg.place(relwidth = 0.74, 
							relheight = 0.035, 
							rely = 0.001, 
							relx = 0.011) 
        self.entryMsg.focus()

        self.buttonMsg = tk.Button(self.labelBottom, 
								text = "Send",
								font = "Helvetica 10 bold", 
								width = 20, 
								bg = "thistle4", 
								command = lambda : self.sendButton(self.entryMsg.get())) 
        self.buttonMsg.place(relx = 0.77, 
							rely = 0.001, 
							relheight = 0.035, 
							relwidth = 0.22) 


        self.labelFile = tk.Label(self.Window, bg="gainsboro", height=70) 
		
        self.labelFile.place(relwidth = 1, 
							    rely = 0.86) 
		
        self.fileLocation = tk.Label(self.labelFile, 
                                text = "Choose file to send",
                                bg = "thistle4", 
                                fg = "gray1", 
                                font = "Helvetica 11")
        self.fileLocation.place(relwidth = 0.65, 
                                relheight = 0.028, 
                                rely = 0.001, 
                                relx = 0.011)
        #self.fileLocation.focus()

        self.browse = tk.Button(self.labelFile, 
								text = "Browse", 
								font = "Helvetica 10 bold", 
								width = 13, 
								bg = "thistle4", 
								command = self.browseFile)
        self.browse.place(relx = 0.675, 
							rely = 0.001, 
							relheight = 0.028, 
							relwidth = 0.15) 

        self.sengFileBtn = tk.Button(self.labelFile, 
								text = "Send", 
								font = "Helvetica 10 bold", 
								width = 13, 
								bg = "thistle4", 
								command = self.sendFile)
        self.sengFileBtn.place(relx = 0.84, 
							rely = 0.001, 
							relheight = 0.028, 
							relwidth = 0.15)


        self.buttonLeave = tk.Button(self.labelFile, 
								text = "Leave", 
								font = "Helvetica 10 bold", 
								width = 13, 
								bg = "thistle4", 
								command = lambda: self.Window.destroy())

        self.buttonLeave.place(relx = 0.20, 
							rely = 0.0365, 
							relheight = 0.030, 
							relwidth = 0.60)
    
        self.textCons.config(cursor = "arrow")
        scrollbar = tk.Scrollbar(self.textCons) 
        scrollbar.place(relheight = 1, 
						relx = 0.974)

        scrollbar.config(command = self.textCons.yview)
        self.textCons.config(state = tk.DISABLED)

    def browseFile(self):
        self.filename = filedialog.askopenfilename(initialdir="/", 
                                    title="Select a file",
                                    filetypes = (("Text files", 
                                                "*.txt*"), 
                                                ("all files", 
                                                "*.*")))
        self.fileLocation.configure(text="File Opened: "+ self.filename)


    def sendFile(self):
        self.server.send("FILE".encode())
        time.sleep(0.1)
        self.server.send(str("client_" + os.path.basename(self.filename)).encode())
        time.sleep(0.1)
        self.server.send(str(os.path.getsize(self.filename)).encode())
        time.sleep(0.1)

        file = open(self.filename, "rb")
        data = file.read(1024)
        while data:
            self.server.send(data)
            data = file.read(1024)
        self.textCons.config(state=tk.DISABLED)
        self.textCons.config(state = tk.NORMAL)
        self.textCons.insert(tk.END, "<You> "
                                     + str(os.path.basename(self.filename)) 
                                     + " Sent\n\n")
        self.textCons.config(state = tk.DISABLED) 
        self.textCons.see(tk.END)


    def sendButton(self, msg):
        self.textCons.config(state = tk.DISABLED) 
        self.msg=msg 
        self.entryMsg.delete(0, tk.END) 
        snd= threading.Thread(target = self.sendMessage) 
        snd.start() 

    def receive(self):
        while True:
            try:
                message = self.server.recv(1024).decode()
                print(message)
                if str(message) == "$Accepted":
                    # print("Inside loop")
                    self.login.destroy()
                    self.layout()
                elif str(message) == "$Removed":
                    self.Window.destroy()
                elif str(message)=="$wait":
                    self.receive()
                elif str(message) == "FILE":
                    file_name = self.server.recv(1024).decode()
                    lenOfFile = self.server.recv(1024).decode()
                    send_user = self.server.recv(1024).decode()

                    if os.path.exists(file_name):
                        os.remove(file_name)

                    total = 0
                    with open(file_name, 'wb') as file:
                        while str(total) != lenOfFile:
                            data = self.server.recv(1024)
                            total = total + len(data)     
                            file.write(data)
                    
                    self.textCons.config(state=tk.DISABLED)
                    self.textCons.config(state = tk.NORMAL)
                    self.textCons.insert(tk.END, "<" + str(send_user) + "> " + file_name + " Received\n\n")
                    self.textCons.config(state = tk.DISABLED) 
                    self.textCons.see(tk.END)
                else:
                    self.textCons.config(state=tk.DISABLED)
                    self.textCons.config(state = tk.NORMAL)
                    self.textCons.insert(tk.END, 
                                    message+"\n\n") 

                    self.textCons.config(state = tk.DISABLED) 
                    self.textCons.see(tk.END)
                

                

            except Exception as e: 
                # print("An error occured!")
                print(e) 
                # self.login.destroy()
                # self.server.close() 
                # break

    def sendMessage(self):
        self.textCons.config(state=tk.DISABLED) 
        while True:  
            print(self.msg)
            self.textCons.config(state = tk.NORMAL)
            self.textCons.insert(tk.END, 
                            "<You> " + self.msg + "\n\n") 
            self.server.send(self.msg.encode())
            self.textCons.config(state = tk.DISABLED) 
            self.textCons.see(tk.END)
            break



if __name__ == "__main__":
    ip_address = "127.0.0.1"
    port = 12345
    g = GUI(ip_address, port)
