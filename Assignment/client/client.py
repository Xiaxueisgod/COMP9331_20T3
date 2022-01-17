import socket
import sys
import time


loginStatus = 0
taskStatus = 0

def checkCorrect(clientSocket):
    global loginStatus
    username = input('Enter username: ')
    clientSocket.send(username.encode())
    username_msg = clientSocket.recv(2048).decode()
    if username_msg == 'username exists':
        password = input("Enter password: ")
        clientSocket.send(password.encode())
        password_msg = clientSocket.recv(2048).decode()
        if password_msg == "OK":
            print('Welcome to the forum')
            loginStatus = 1
        else:
            print("invalid password")
            #clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #clientSocket.connect(('127.0.0.1', serverPort))
            checkCorrect(clientSocket)

    elif username_msg == 'username not found':
        password = input(f"Enter new password for {username}: ")
        clientSocket.send(password.encode())
        password_msg = clientSocket.recv(2048).decode()
        if password_msg == "just so so":
            print(f"new user {username} created")
            loginStatus = 1


def executeTask(clientSocket):
    global taskStatus
    task = input("Enter one of the following commands: CRT, MSG, DLT, EDT, LST, RDT, UPD, DWN, RMV, XIT, SHT:")

    if task == "XIT":
        clientSocket.send(task.encode())
        print("Goodbye")
        clientSocket.close()
        taskStatus = 1

    elif "CRT" in task:
        clientSocket.send(task.encode())
        print(clientSocket.recv(2048).decode())


    elif task == "LST":
        clientSocket.send(task.encode())
        msg = clientSocket.recv(2048).decode()
        if msg == "There is no active threads":
            print(msg)
        else:
            print(msg)
            clientSocket.send("active threads".encode())
            listContent = clientSocket.recv(2048).decode()
            print(listContent)

    elif "MSG" in task:
        clientSocket.send(task.encode())
        taskContent = task.split(" ")[2:]
        taskContent = " ".join(taskContent)
        threadNumber = task.split(" ")[1]
        if clientSocket.recv(2048).decode() == "thread exist":
            print(f"Message posted to {threadNumber} thread")
        else:
            print(f"{threadNumber} not exist")

    elif "RDT" in task:
        clientSocket.send(task.encode())
        taskContent = clientSocket.recv(2048).decode()
        print(taskContent)

    elif "RMV" in task:
        clientSocket.send(task.encode())
        taskContent = clientSocket.recv(2048).decode()
        print(taskContent)

    elif "DLT" in task:
        clientSocket.send(task.encode())
        taskContent = clientSocket.recv(2048).decode()
        print(taskContent)

    elif "EDT" in task:
        clientSocket.send(task.encode())
        taskContent = clientSocket.recv(2048).decode()
        print(taskContent)

    elif "UPD" in task:
        clientSocket.send(task.encode())
        taskContent = clientSocket.recv(2048).decode()
        print(taskContent)

    elif "DWN" in task:
        clientSocket.send(task.encode())
        fileName = task.split(" ")[2]
        taskContent = clientSocket.recv(2048).decode()
        if taskContent == "all ready":
            with open(fileName, mode='a+') as wf:
                wf.write(taskContent)
            print(f"{fileName} successfully downloaded")
        else:
            print(taskContent)

    elif "SHT" in task:
        clientSocket.send(task.encode())
        taskContent = clientSocket.recv(2048).decode()
        if taskContent == "Server shutting down":
            print("Goodbye. Server shutting down")
            sys.exit()
        elif taskContent == "Incorrect command":
            print("Incorrect command")
        elif taskContent == "Incorrect input":
            print("Incorrect input")
        else:
            print("Incorrect password")

    else:
        print("Incorrect command")


if __name__ == "__main__":
    serverIP = sys.argv[1]
    serverPort = int(sys.argv[2])

    loginStatus = 0
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((serverIP, serverPort))
    while True:
        if loginStatus == 0:
            checkCorrect(clientSocket)
        else:
            break

    while True:
        if taskStatus == 0:
            executeTask(clientSocket)
        else:
            break

