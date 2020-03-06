import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *
import socket

def main(argv):
	type = 0	#1=ICMP, 2=SYN
	portString = "80"
	host = argv[len(argv)-1]
	argv = argv[:((len(argv))-1)]

	#Convert host to an IP if it isn't
	hostCheckArr = host.split(".")
	if(len(hostCheckArr) != 4):
		print("Converting Domain to IP")
		#This is a domain name: Convert to IP
		try:
			host = socket.gethostbyname(host)
		except:
			sys.exit("Invalid host domain")
		print("Found IP for Domain: ", host)
		#Prepare to check if found IP is valid
		hostCheckArr = host.split(".")
	#Check formatting of IP Address
	if(len(hostCheckArr) == 4):
		print("IP detected: Checking Validity")
		isValidIP = True
		validNum = 256
		for num in hostCheckArr:
			num = num.strip()
			try:
				#Convert String to Integer (If it is one)
				validNum = int(num)
			except:
				print("Part of IP is not an int - Failure")
				isValidIP = False
				break
			if(not(validNum >= 0 and validNum < 256)):
				print("IP part not within range of 0-255 - Failure")
				isValidIP = False
				break
		if(not isValidIP):
			sys.exit("Invalid host IP or Domain")
	else:
		sys.exit("Invalid Host IP or domain")


	#Set up port scan stuff
	dst_ip = host
	src_port = RandShort()
	dst_port= 5038
	isItOpen = False

	#Non-Stealth Scan
	print("(Values) dst_ip:", dst_ip, "src_port:", src_port, "dst_port:", dst_port)

	default_scan = sr1(IP(dst=dst_ip)/TCP(sport=src_port, dport=dst_port, flags="S"), timeout=4)
	print("default_scan: ", default_scan)

	
	# tcp_connect_scan_resp = sr1(IP(dst=dst_ip)/TCP(sport=src_port,dport=dst_port,flags="S"),timeout=10)
	# print("Response:", tcp_connect_scan_resp)
	# if(tcp_connect_scan_resp==None):
	# 	#Port is Closed
	# 	print("Port Closed: ", dst_port)
	# 	pass
	# elif(tcp_connect_scan_resp.haslayer(TCP)):
	# 	if(tcp_connect_scan_resp.getlayer(TCP).flags == 0x12):
	# 		send_rst = sr(IP(dst=dst_ip)/TCP(sport=src_port,dport=dst_port,flags="AR"),timeout=10)
	# 		#Port is Open!
	# 		print("Port Open: ", dst_port)
	# 		isItOpen = True
	# 	elif (tcp_connect_scan_resp.getlayer(TCP).flags == 0x14):
	# 		#Port is Closed
	# 		print("Port Closed-: ", dst_port)
	# 		pass


if __name__ == "__main__":
	main(sys.argv[1:])