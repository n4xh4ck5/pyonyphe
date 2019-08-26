#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import requests
import xlsxwriter


def read_input(path):
	d = []
	try:

		with open (path) as f:
			lines = f.readlines()
			for line in lines:
				d.append(line.rstrip('\n'))
			f.close()

	except Exception as exc:
		print ("Error in read_input" + str(exc))
	
	finally:
		return d

def export_results (targets,ports):
	# Start from the first cell. Rows and columns are zero indexed.
	row = 0
	col = 0
	i = 0
	try:
		print ("Exporting the results in an excel")
		# Create a workbook and add a worksheet.
		workbook = xlsxwriter.Workbook('pyonyphe.xlsx')
		worksheet = workbook.add_worksheet()
		worksheet.write(row, col, "IP")
		worksheet.write(row, col+1, "Ports")
		row += 1
		# Iterate over the data and write it out row by row.
		for target in targets:
				col = 0
				worksheet.write(row, col, target)
				worksheet.write(row, col+1, ports[i])
				row += 1
				i += 1

		#Close the excel
		workbook.close()


	except Exception as exc:
		print ("Error in export_results" + str(exc))

def manage_response (data):
	ports = []
	try:
		for port in data['results']:
			print (str(port['port']))
			ports.append(str(port['port']))

	except Exception as exc:
		print ("Not found information of the IP" + str(exc))
		ports = "-"

	finally:
		return ports

		
def send_request (url):

	response = None

	try:

		response = requests.get(url,timeout=20,allow_redirects =True)
	except Exception as exc:
		print ("Error in send_request" + str(exc))
	finally:
		return response.json()

def banner():

	print ("""
	                                                                                                              
		                                                            $$\                 
		                                                            $$ |                
		 $$$$$$\  $$\   $$\  $$$$$$\  $$$$$$$\  $$\   $$\  $$$$$$\  $$$$$$$\   $$$$$$\  
		$$  __$$\ $$ |  $$ |$$  __$$\ $$  __$$\ $$ |  $$ |$$  __$$\ $$  __$$\ $$  __$$\ 
		$$ /  $$ |$$ |  $$ |$$ /  $$ |$$ |  $$ |$$ |  $$ |$$ /  $$ |$$ |  $$ |$$$$$$$$ |
		$$ |  $$ |$$ |  $$ |$$ |  $$ |$$ |  $$ |$$ |  $$ |$$ |  $$ |$$ |  $$ |$$   ____|
		$$$$$$$  |\$$$$$$$ |\$$$$$$  |$$ |  $$ |\$$$$$$$ |$$$$$$$  |$$ |  $$ |\$$$$$$$\ 
		$$  ____/  \____$$ | \______/ \__|  \__| \____$$ |$$  ____/ \__|  \__| \_______|
		$$ |      $$\   $$ |                    $$\   $$ |$$ |                          
		$$ |      \$$$$$$  |                    \$$$$$$  |$$ |                          
		\__|       \______/                      \______/ \__|                          
				                                                                                                      
                                                                                                              
                                                                                                              
	""")
	print ("""
	** Tool to obtain information about the open ports throught API's onyphe.
    	** Author: Ignacio Brihuega Rodriguez a.k.a N4xh4ck5
    	** DISCLAMER This tool was developed for educational goals. 
    	** The author is not responsible for using to others goals.
    	** A high power, carries a high responsibility!
    	** Version 1.0""")
	
def initial_help():
	print (""" \n This script interactues with the onyphe's API to obtain the ports opened of a network address. The result by default is exported in xlsx format

				Example of usage: python3 pyonyphe.py ip.txt""")


def main(argv):

	banner()
	initial_help()
	target = str(sys.argv[1])
	api="YOUR_API"
	r = None
	ports = []
	array = read_input(target) 
	try:
		for ip in array:
			print (ip)
			url ="https://www.onyphe.io/api/synscan/{0}?apikey={1}".format(ip,api)
			#Send request
			r = send_request(url)
			# Manage the response
			ports = manage_response(r)
		#Export results		
		export_results(array,ports)

	except Exception as exc:
		print ("Error in main function " + str(exc))


if __name__ == "__main__":
    main(sys.argv[1:])
