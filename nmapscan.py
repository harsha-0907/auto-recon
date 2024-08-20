#!bin/python3


import os,sys
from subprocess import CalledProcessError
try:
	dir_name=sys.argv[2]
	target_ip=sys.argv[1]
	file_path=dir_name+"/nmapscan.txt"
	#print("Input Details : ")
	#print("Directory Name : ",dir_name," Target IP : ",target_ip," File Name",file_path)
	result=os.popen("sudo nmap -sS -p- -A -T5 --mtu 64  "+target_ip+" > "+file_path).read() # --badsum -D RND: 5 For Extra
	print("NMAP Complete")
except Exception:
	raise CalledProcessError
