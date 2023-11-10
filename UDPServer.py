import os
from socket import *

while True:
    #判断是否继续传输文件
    flag = input("Continue to run server? Y/n :")
    if flag == "n":
        #如果建立了Socket
        if serverSocket:
        #关闭socket
            serverSocket.close()
        print("Connection released")    
        break
    
    #设定服务器端端口号
    while True:
        serverPort = input("Please input server Port number :")
        if serverPort.isdigit() and int(serverPort)>=0 and int(serverPort)<=65535:
            serverPort = int(serverPort)
            break
        else:
            print("Please input a valid Port number!")
    
    #创建UDP socket
    serverSocket = socket(AF_INET, SOCK_DGRAM)
    serverSocket.bind(('',serverPort))
    
    #模拟建立TCP连接
    while True:
        print("Trying to establish connection")
        syn = serverSocket.recvfrom(1024)
        clientName, clientPort = syn[1]
        if syn[0] == b"SYN":
            #print("The server received syn from client,sending ack ...")
            serverSocket.sendto("ACK".encode(), (clientName,clientPort))
            while True:
                ack = serverSocket.recv(1024)
                if ack == b"ACK":
                    print(f"Connection established from IP: {clientName} , Port Number: {clientPort}")
                    break
            break
            
    while True:
        #接收传输类型
        type = serverSocket.recv(1024)
        
        #发送ACK
        serverSocket.sendto("ACK".encode(), (clientName,clientPort))    
        
        if type == b"q":
            print("The client asked to release conneciton ...")
            #接收FIN
            while True:
                fin = serverSocket.recv(1024)
                if fin == b"FIN":
                    #print("Received fin from client,sending ack ...")
                    serverSocket.sendto("ACK".encode(), (clientName,clientPort))
                    break
            #发送ACK
            serverSocket.sendto("ACK".encode(), (clientName,clientPort))
            #发送FIN
            serverSocket.sendto("FIN".encode(), (clientName,clientPort))
            #接收ACK
            while True:
                ack = serverSocket.recv(1024)
                if ack == b"ACK":
                    print("Connection released!")
                    break
            break
        elif type == b"r":   
            print("Ready to send file")  
            while True:
                #接收客户端发送的文件名
                fileName = serverSocket.recv(1024).decode()
                print(f"The client ask the file {fileName}")
                #判断文件是否存在
                if os.path.exists(fileName):
                    #发送ACK
                    serverSocket.sendto("ACK".encode(), (clientName,clientPort))
                    #打开文件
                    file = open(fileName,"rb")
                    #分块读取和发送整个文件
                    while True:
                        data = file.read(1024)
                        if not data:
                            print("File sent!")
                            #发送文件传输完成的ACK
                            serverSocket.sendto("ACK".encode(), (clientName,clientPort))
                            break
                        serverSocket.sendto(data, (clientName, clientPort))
                    #关闭文件
                    file.close()
                    break
                else:
                    #发送错误信息
                    serverSocket.sendto("Error".encode(), (clientName,clientPort))
                    print("File does not exist!")
        elif type == b"s":
            print("Ready to receive a file")
            #接收文件名
            fileName = serverSocket.recv(1024).decode()
            #返回ack
            serverSocket.sendto("ACK".encode(), (clientName,clientPort))
            file = open(fileName,"wb")
            #接收文件
            while True:
                data,addr = serverSocket.recvfrom(1024)
                clientName,clientPort=addr
                if data == b"ACK":
                    print(f"The File {fileName} received!")
                    break
                file.write(data)
            #关闭文件
            file.close()
        