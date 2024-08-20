#!bin/python

#Module Section
import os
import subprocess
import sys
import re
#import socket

#Module Section-Ends


#Global Section
mac_address=""
dir_name=""
target_ip=""

#Ends

def modifyMAC():
	data=os.popen("macchanger --show eth0 ").read().split('\n')
	current_mac=data[0].split()[2];n_mac_address=data[1].split()[2]
	if current_mac==n_mac_address:
		op=os.popen("sudo macchanger -r eth0").read()
		n_mac_address=op.split('\n')[2].split(' ')[-2] #Obtain the Modified IP
		print("Current Mac Address : ",n_mac_address)
	else:
		ip=input("Do you want to modify your MAC Address (y/n) ")
		if ip=='y' or ip=='Y':
			op=os.popen("sudo macchanger -r eth0").read()
			n_mac_address=op.split('\n')[2].split(' ')[-2] #Obtain the Modified IP
			print("Current Mac Address : ",n_mac_address)
		else:
			n_mac_address=current_mac
			print("Current Mac Address : ",n_mac_address)
		return n_mac_address

def verifyHost(target_ip):	#We are using nmap as it is reliable
	print("Verifying that the Host is Active... ",end='')
	data=subprocess.run(["sudo","nmap","-sS","--mtu","8",target_ip],capture_output=True,text=True,check=True).stdout.split('\n')[-2]
	res1=re.search("\d hosts up",data)
	res2=re.search("\d host up",data)
	res=res1 or res2
	res=int(res.group()[0].split()[0])
	if res==0:
		print("No")
		print("[-] Looks like there is no Response...\n[-] Please check your IP...")
		sys.exit(0)
	else:
		print("Yes")
		directories=subprocess.run(['ls'],check=True,text=True,capture_output=True).stdout.split('\n')
		if target_ip in directories:
			dir_name=target_ip+'new'
		else:
			print("[+] Creating Directory...")
			dir_name=target_ip
		command ='mkdir '+dir_name
		os.system(command)
	return dir_name				
def nmapScanner(target_ip,dir_name):
	print("Starting NMAP...")
	print(target_ip,"",dir_name)
	try:
		result=subprocess.run(['python3','nmapscan.py',target_ip,dir_name],check=True)
	except subprocess.CalledProcessError:
		print("An Error in nmap scan")
		sys.exit(0)


def startup():	
	output=os.popen("whoami")
	if output.read().strip('\n') == 'root':
		target_ip=input("Target IP : ")
		#target_ip="192.168.137.227"
		#See if the Host is active
		#mac_address=modifyMAC()
		dir_name=verifyHost(target_ip)
		print("Proceeding...")
		#print(target_ip,dir_name,mac_address)
		nmapScanner(target_ip,dir_name)
		dataCollector(dir_name,target_ip)
		
	else:
		print("Please Run this as Root...")
		print("sudo python3 program.py")


def dataCollector(dir_name,target_ip):
	""" """
	try:
		result=subprocess.run(["python3","dataCollector.py",dir_name,target_ip],check=True)
	except subprocess.CalledProcessError:
		print("Error at DataCollector Module")

def webSearcher():
	try:
		res=subprocess.run(["python3","websearcher.py",dir_name],check=True)
	except subprocess.CalledProcessError:
		print("Error in Wesearcher...")
		
	
try:
	startup()
except Exception as e:
	print("An Error Has Occured",e)
		
	
