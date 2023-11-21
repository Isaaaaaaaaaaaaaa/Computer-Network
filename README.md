# UDP Socket Programming
# Copyright wangyisa 221002501 BFU
# The program only used as the homework of Computer-Network
# UDP Cilent & UDP Server
# This is the introduction of the two program

1.UDPClient:
	Pleease use Python3 to interpret and run this program as a client. 
	The main functions of this program are: 
		1. File transfer based on UDP. 
			Users can specify the server IP and port number; 
			during the transfer process, users can choose to receive files from the server or send files to the server. 
		2. A simulated implementation of the TCP protocol. 
			When attempting to establish a connection, a feedback mechanism from the receiver and a timeout retransmission mechanism are introduced, 
			simulating the three-way handshake of establishing a TCP connection. 
			In the process of file transfer and connection release, a certain degree of simulation of the TCP protocol is made.
			
2.UDPServer:
	Please use Python3 to interpret and run this program as a server.
	The main functions of this program are:
		1.File transfer based on UDP.
			users can specify the server’s port number for the client to connect, 
			and the server has the ability to send to or receive files from the client. 
		2. A simulated implementation of the TCP protocol. 
			Like the client, the server also implements a matching simulation of the TCP connection. 
		3. Multithreaded communication. 
			By referencing the Thread module in Python, 
			this program implements the simultaneous connection and file transfer function of multiple clients and the server. 

	Notice:The Port Number which users specified will increased by 1 after the server create a new thread.