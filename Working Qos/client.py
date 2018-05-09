import socket

def Main():
	ip_address = '127.0.0.1'
	port_no = 1234

	sckt = socket.socket()
	sckt.connect((ip_address,port_no))

	file_name = raw_input("Enter the filename : ")
	if file_name != 'q':
		sckt.send(file_name)
		info = sckt.recv(1024)
		if info[:6] == 'Exists':
			file_size = long(info[6:])
			msg = raw_input("Exists, " +str(file_size)+"bytes, download the file (Y/N): ")
			if msg == 'Y':
				sckt.send('OK')
				f_n = open('new_ '+file_name, 'wb')
				info = sckt.recv(1024)
				total_received = len(info)
				f_n.write(info)
				while total_received < file_size:
					info = sckt.recv(1024)
					total_received += len(info)
					f_n.write(info)

				print "download done!!!"
		else:
			print "No such file"
	
	sckt.close()

if __name__ == '__main__':
	Main()


