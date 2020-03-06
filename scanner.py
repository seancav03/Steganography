import sys, getopt
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
		#This is a domain name: Convert to IP
		try:
			host = socket.gethostbyname(host)
		except:
			sys.exit("Invalid host domain")
		#Prepare to check if found IP is valid
		hostCheckArr = host.split(".")
	#Check formatting of IP Address
	if(len(hostCheckArr) == 4):
		isValidIP = True
		validNum = 256
		for num in hostCheckArr:
			num = num.strip()
			try:
				#Convert String to Integer (If it is one)
				validNum = int(num)
			except:
				print("Part of IP is not an int - Failure:", sys.exc_info()[0])
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
	#IP must be valid if code gets here
	#begin parsing other arguments
	try:
		opts, args = getopt.getopt(argv,"",["p=", "ICMP","SYN"])
	except getopt.GetoptError:
		sys.exit("INVALID INPUT: Correct arguments and try again")

	for opt, arg in opts:
		if opt == "--ICMP":
			if type != 0:
				sys.exit("Invalid Input: Only chose ICMP OR SYN")
			type=1
		elif opt == "--SYN":
			if type != 0:
				sys.exit("Invalid Input: Only chose ICMP OR SYN")
			type=2
		elif opt == "--p":
			portString = arg
	if type == 0:
		sys.exit("Invalid Input: Specify ICMP OR SYN")

	if type == 1:
		#Non-Stealth Scan
		try:
			p=sr1(IP(dst=host)/ICMP(), timeout=10)
			if p:
				print("ICMP scan: Machine Found")
			else:
				print("ICMP scan: Machine Not Found")
			
		except Exception:
			#port Closed
			print("ICMP scan: Machine Not Found")
	else:
		portSets = portString.split(',')
		trimedPortSets = []
		for part in portSets:
			trimedPortSets.append(part.strip())
		#Open ports will be put here
		openPorts = []
		#Run through all ports wanted
		for ports in trimedPortSets:
			if '-' in ports:
				nums = ports.split("-")
				start = nums[0]
				end = nums[1]
				#range of ports
				for testPort in range(int(start), (int(end)+1)):
					if(checkPort(testPort, host)):
						openPorts.append(testPort)
			else:
				#Just a single port number
				if(checkPort(int(ports), host)):
					openPorts.append(int(ports))
		print("Open Ports:", openPorts)
			
#Takes destination port, destination IP, and scan type and checks if port is open (1-ICMP, 2=SYN)
def checkPort(port, ip):
	
	dst_ip = ip
	src_port = RandShort()
	dst_port=port
	isItOpen = False

	#Stealth Scan
	stealth_scan_resp = sr1(IP(dst=dst_ip)/TCP(sport=src_port,dport=dst_port,flags="S"),timeout=3)
	if(stealth_scan_resp==None):
		#Filtered
		print("Port Closed: ", dst_port)
	elif(stealth_scan_resp.haslayer(TCP)):
		if(stealth_scan_resp.getlayer(TCP).flags == 0x12):
			send_rst = sr(IP(dst=dst_ip)/TCP(sport=src_port,dport=dst_port,flags="R"),timeout=3)
			#Port is Open
			print("Port Open ", dst_port)
			isItOpen = True
		elif (stealth_scan_resp.getlayer(TCP).flags == 0x14):
			#Port Closed
			print("Port Closed: ", dst_port)
	elif(stealth_scan_resp.haslayer(ICMP)):
		if(int(stealth_scan_resp.getlayer(ICMP).type)==3 and int(stealth_scan_resp.getlayer(ICMP).code) in [1,2,3,9,10,13]):
			#Filtered
			print("Port Open: ", dst_port)
			isItOpen = True
	#retuns whether stealth scan method found the port to be open
	return isItOpen


if __name__ == "__main__":
	main(sys.argv[1:])