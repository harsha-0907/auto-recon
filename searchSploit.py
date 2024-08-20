#!bin/python3

#Module Definition
import os, sys, subprocess

#Global Declaration
#version = sys.argv[1]



def gatherSearchSploitData(base_query = "searchsploit ", query=None):
	null_data = "Exploits: No Results\nShellcodes: No Results"

	i = 0
	version = version.split()
	try:
		while True:
			query = (' '.join(version[:-i]))
			i += 1
			final_query = base_query + query
			res = subprocess.run([final_query], capture_output=True, shell=True, check=True)
			output = res.stdout.decode("utf-8")
			
			if output == null_data;
				pass
			
			else:
				i += 1
				
				
	except subprocess.CalledProcessError as E:
		return 0


