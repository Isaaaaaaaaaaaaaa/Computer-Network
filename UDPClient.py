import os
from socket import *

#判断ip是否合法
def isValidIp(ip):
    parts = ip.split(".")   #将ip以'.'为分隔，分隔成一个列表parts
    if len(parts) != 4:     #判断parts的长度是否为4,不是则证明输入有误
        return False
    for part in parts:      #遍历parts列表 判断每个part是否符合规则
        if not part.isdigit():
            return False
        i = int(part)
        if i < 0 or i > 255:
            return False
    return True

while True:
    #判断是否继续传输文件
    flag = input("Continue to transfer file? Y/n :")
    if flag == "n":
        break
    
    #输入目标端口号       
    while True:
        serverPort = input("Please input server Port number :")
        if serverPort.isdigit() and int(serverPort)>=0 and int(serverPort)<=65535:
            serverPort = int(serverPort)
            break
        else:
            print("Please input a valid Port number!")
            
    #输入目标ip地址
    while True:
        serverName = input("Please input server IP :")
        if isValidIp(serverName):
            break
        else:
            print("Please input a valid IP!")

    #开始传输文件
    while True:
        #输入传输类型
        type = input("Please input transfer type:s/r(send or receive),input q to quit :")
        if type == "q":
            break
        #向Server端发送文件
        elif type == "s":
            #创建socket
            clientSocket = socket(AF_INET,SOCK_DGRAM)
            #模拟建立TCP连接
            while True:
                print("Trying to establish connection")
                clientSocket.sendto("SYN".encode(),(serverName,serverPort))
                ack = clientSocket.recv(1024)
                if ack == b"ACK":
                    print("Received ack from server,sending ack ...")
                    clientSocket.sendto("ACK".encode(),(serverName,serverPort))
                    print("Connection established")
                    break
                else:
                    print("Connection failed")
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
                    clientSocket.sendto(data, (serverName, serverPort))
                #关闭文件
                file.close()
                #模拟释放TCP连接
                while True:
                    print("Trying to release connection")
                    clientSocket.sendto("FIN".encode(),(serverName,serverPort))
                    ack = clientSocket.recv(1024)
                    if ack == b"ACK":
                        print("Connection released")
                        break
                #关闭socket
                clientSocket.close()
            else:
                print("File does not exist!")
        elif type == "r":
            #创建socket
            clientSocket = socket(AF_INET,SOCK_DGRAM)
            #创建文件
            fileName = input("Please input file name :")
            file = open(fileName,"wb")
            #接收文件
            while True:
                data,addr = clientSocket.recvfrom(1024)
                if data == b"FIN":
                    break
                file.write(data)
            #关闭文件
            file.close()
            #关闭socket
            clientSocket.close()
            
    