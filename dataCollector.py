#!bin/python3
import re
import sys
import subprocess
import os


#Declaration
data=""
_imp_ports=[];imp_ports=[];ports=[]
dir_name=sys.argv[1];ip_addr=sys.argv[2]
file_name=dir_name+'/nmapscan.txt'
with open(file_name,'r') as file:
	data=file.read()
with open("project_data/imp_ports.txt",'r') as file:
	_ports=file.readlines()
	_imp_ports=[int(i) for i in _ports]
	#print(_imp_ports)
	
file_name=sys.argv[1]
port_data=dict()
file=open(dir_name+"/report.data",'w')


#Patterns
patterns=['\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}.*',"\s[0-9a-fA-F]{2}:[0-9a-fA-F]{2}:[0-9a-fA-F]{2}:[0-9a-fA-F]{2}:[0-9a-fA-F]{2}:[0-9a-fA-F]{2}",r"\n\d{1,5}/\w+\s+\w+\s+\S+.*"]
#
#Code

#Name-oF Machine
def getName(data):
	found=re.findall('Nmap scan report for .*',data)
	_data=found[0][21:]
	data=_data.split()
	if len(data)>1:
		machine_name=data[0]
	else:
		machine_name=" - "
	print("Machine Name :",machine_name)
	file.write("Machine Name : "+machine_name+"\n")

def getDate(data):
	date_pattern=patterns[0]	#Date
	date_time=re.search(date_pattern,data).group()
	print("Date And Time : ",date_time)
	file.write("Date And Time : "+date_time+"\n")
	
def getMACAddress(data):
	pattern=patterns[1]	#MAC Address
	_mac=re.search(pattern,data)
	if _mac:
		mac_address=_mac.group()
	else:
		mac_address="-"
	file.write("MAC Address : "+mac_address+"\n")
	print("MAC Address :",mac_address)

def checkData(data):	#This method is used to check if there is any data that can be of Help
	pattern="PORT\s+STATE\s+SERVICE\s+VERSION"
	has_result=re.search(pattern,data)
	if has_result:
		return 1
	else:
		print("All the Ports on the MAchine are in Ignored State.")
		file.write("All the Ports on the MAchine are in Ignored State.")
		return -1
	
#Overview
def displayOverview():
	file1=open(dir_name+"/temp_port_data.data",'w')	#Write only the Port_Data in this MOdule. for searching purposes
	file2 = open(dir_name + "/searchsploit.csv", 'w')
	pattern=patterns[2];imp_ports=[]
	results=re.findall(pattern,data)
	for port in results:
		useful_data=port.split()
		if len(useful_data) <4:
			version="Unknown"
			(port_number,filtered,service) = useful_data
			spl=port_number.split('/')
			port_num=spl[0];connection=spl[1]
			port_data[port_num]=[service,version,filtered,connection]
		else:
			version=""
			for i in useful_data[3:]:
				version=version+i+' '
			(port_number,filtered,service)=useful_data[:3]
			spl=port_number.split('/')
			port_num=spl[0];connection=spl[1]
			port_data[port_num]=[service,version,filtered,connection]
	#Now write it in Overview Section
	file.write("\nPort Overview : \n")
	file.write("PORT\tSERVICE\t\tVERSION\t\tFILTER\tCONNECTION\n")
	print("Port Overview : ")
	print("PORT\tSERVICE\t\tVERSION\t\tFILTER\tCONNECTION")
	columns=port_data.keys()
	for port in columns :
		(service,version,filtered,connection)=port_data[port]
		file.write(port+'\t'+service+'\t'+version+'\t\t'+filtered+'\t'+connection+'\n')
		file1.write(service+' '+version+'\n')
		file2.write(service+','+version+'\n')
		
		print(port+'\t'+service+'\t'+version+'\t'+filtered+'\t'+connection)
	print("\n\n")
	return columns

def completeView(data):
	print("Complete Over-View : \n")
	file.write("\nComplete Overview :")
	pattern="\w+\s+\w+\s+\w+\s+\s\w+"
	det=re.search(pattern,data)
	#print(str(det))
	res=re.findall("\(\d{0,5}.*\d{0,5}\)",str(det))[0].strip("()").split(',')
	init_pos=int(res[0]);final_pos=int(res[1])
	file.write(data[init_pos:-1])
	print(data[init_pos:-1])
	print("\n\nComplete.")
		

def traceRoute():
	print("Tracing the Route To Destination...")
	traceRoute_data=os.popen("traceroute "+ip_addr).read()
	file.write('\n\n'+traceRoute_data)
	print("Tracing Complete..")

if __name__=="__main__":
	#print(data)
	flag=checkData(data)
	if flag == -1:
		sys.exit(0)	
	getName(data)
	getDate(data)
	getMACAddress(data)
	ports=displayOverview()
	#completeView(data)
	#Traceroute the Target
	#traceRoute()
	
	

