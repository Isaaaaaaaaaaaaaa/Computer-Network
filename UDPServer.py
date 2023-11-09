import os
from socket import *

while True:
    #判断是否继续传输文件
    flag = input("Continue to transfer file? Y/n :")
    if flag == "n":
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
    
    while True:
        #输入传输类型
        type = input("Please input transfer type:s/r(send or receive),input q to quit :")
        if type == "q":
            break
        elif type == "s":
            #输入文件名
            fileName = input("Please input file name :")
            #判断文件是否存在
            if os.path.exists(fileName):
                #打开文件
                file = open(fileName,"rb")
                #分块读取和发送整个文件
                while True:
                    data = file.read(1024)
                    if not data:
                        break
                    serverSocket.sendto(data, ('', serverPort))
                #关闭文件
                file.close()
                #关闭socket
                serverSocket.close()
            else:
                print("File does not exist!")
        elif type == "r":
            #模拟建立TCP连接
            while True:
                print("Trying to establish connection")
                syn = serverSocket.recvfrom(1024)
                clientName, clientPort = syn[1]
                if syn[0] == b"SYN":
                    print("The server received syn from client,sending ack ...")
                    serverSocket.sendto("ACK".encode(), (clientName,clientPort))
                    while True:
                        ack = serverSocket.recv(1024)
                        if ack == b"ACK":
                            print("Connection established")
                            break
                    break
            #创建文件
            fileName = input("Please input file name :")
            file = open(fileName,"wb")
            #接收文件
            while True:
                data,addr = serverSocket.recvfrom(1024)
                clientName,clientPort=addr
                if data == b"FIN":
                    print("File received!")
                    serverSocket.sendto("ACK".encode(), (clientName,clientPort))
                    break
                file.write(data)
            #关闭文件
            file.close()
            #关闭socket
            serverSocket.close()
    