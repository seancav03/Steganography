
import sys, getopt
# from scapy.all import sr1,IP,ICMP

def main(argv):
	type = 0	#1=ICMP, 2=SYN
	portString = "80"
	host = argv[len(argv)-1]
	argv = argv[:((len(argv))-1)]
	try:
		opts, args = getopt.getopt(argv,"p:",["ICMP","SYN"])
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
		elif opt == "-p":
			portString = arg
	if type == 0:
		sys.exit("Invalid Input: Specify ICMP OR SYN")
	print("Type: ", type)
	print("host: ", host)
	print("Ports: ", portString)

	portSets = portString.split(',')
	print("Sets: ", portSets)
	trimedPortSets = []
	for part in portSets:
		trimedPortSets.append(part.strip())
	print("Trimmed: ", trimedPortSets)

	for ports in trimedPortSets:
		if '-' in ports:
			nums = ports.split("-")
			start = nums[0]
			end = nums[1]
			#range of ports
			#TODO ADD RANGE FUNCTIONALITY
		else:
			pass
			#Just a single port number


def checkPort(port, type):
	if type == 1:
		
	



if __name__ == "__main__":
	main(sys.argv[1:])




	"""
	try:
      opts, args = getopt.getopt(argv,"p:",["ICMP","SYN"])
	except getopt.GetoptError:
      sys.exit("INVALID INPUT")
	for opt, arg in opts:
		if opt == "--ICMP":
			if type != 0:
				sys.exit("Invalid Input: Only chose ICMP OR SYN")
			type=1
		elif opt == "--SYN"
			if type != 0:
				sys.exit("Invalid Input: Only chose ICMP OR SYN")
			type=2
		if opt == 


		p=sr1(IP(dst=argv[1])/ICMP())
	if p:
		p.show()
	"""