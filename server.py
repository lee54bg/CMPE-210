import socket
import threading
import os

def Get_File(name, sock):
	file_name = sock.recv(1024)
	if os.path.isfile(file_name):
		sock.send("Exists "+str(os.path.getsize(file_name)))
		user_reply = sock.recv(1024)
		if user_reply[:2] == 'OK':
			with open(file_name, 'rb') as f_n:
				data_send = f_n.read(1024)
				sock.send(data_send)
				while data_send != "":
					data_send = f_n.read(1024)
					sock.send(data_send)
	else:
		sock.send("error!!!!")

	sock.close()

def Main():
	ip_address = '127.0.0.1'
	port_no = 1234

	sckt = socket.socket()
	sckt.bind((ip_address,port_no))

	sckt.listen(5)
	
	print ("Server Listening ....")
	while True:
		clnt, adrs = sckt.accept()
		print ("client with address< " + str(adrs) + " > connected")
		thrd = threading.Thread(target=Get_File, args=("GetThread", clnt))
		thrd.start()
	
	sckt.close()

if __name__ == '__main__':
	Main()





