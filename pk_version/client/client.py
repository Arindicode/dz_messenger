from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from tkinter import *


def receive():
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            msg_list.insert(END, msg)
        except OSError:
            break


def send(event=None):
    msg = my_msg.get()
    my_msg.set("")
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        client_socket.close()
        clientWindow.quit()


def on_closing(event=None):
    my_msg.set("{quit}")
    send()


clientWindow = Tk()
clientWindow.geometry('700x400')
clientWindow.title("Python Messenger")
clientWindow.resizable(width=0, height=0)

frame_left = Frame(clientWindow)
frame_left.pack()

messages_frame = Label(frame_left, width=150, height=15)
messages_frame.pack(side=LEFT)

contacts_frame = Label(frame_left, width=150, height=15)
contacts_frame.pack(side=RIGHT)

my_msg = StringVar()

scrollbar = Scrollbar(messages_frame)

msg_list = Listbox(messages_frame, height=15, width=50)
contacts_list = Listbox(contacts_frame, height=15, width=50)

scrollbar.pack(side=RIGHT, fill=Y)

msg_list.pack()
contacts_list.pack()
messages_frame.pack()

entry_field = Entry(clientWindow, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = Button(clientWindow, text="отправить", command=send)
send_button.pack()

clientWindow.protocol("WM_DELETE_WINDOW", on_closing)

HOST = "localhost"
PORT = 8080

BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()
clientWindow.mainloop()
