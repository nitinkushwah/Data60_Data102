#Author: Nitin Kushwah

import requests
from requests.auth import HTTPBasicAuth
import argparse
import getpass

#from requests.packages.urllib3.exceptions import InsecureRequestWarning
#requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

#Check fw, upgrade fw(http or tftp)
#Check power , reset power
#Locator LEDs

#url_encl='https://10.50.14.159/redfish/v1/UpdateService/Actions/UpdateService.SimpleUpdate/Status'
#r=requests.get(url_encl, auth=HTTPBasicAuth('admin','admin'), verify=False)
#json_data=r.json()
#print(json_data)

import http.server
import socketserver
import ssl
import os
if os.name == 'nt':
	from requests.packages.urllib3.exceptions import InsecureRequestWarning
	requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
ssl._create_default_https_context = ssl._create_unverified_context
#PORT = 8081


parser = argparse.ArgumentParser(description='This is \'Beta\' version 1.1 firmware upload client for Data60 and Data102 IOMs. This version doesn\'t verify HTTPS Certificate')
parser.add_argument('-ip', nargs='+', dest='IOM_IP',help='IOM IP Address ',required=True)
#parser.add_argument('-s', dest='ServerIP',help='Server IP Address ',required=True)
parser.add_argument('-u',dest='user',help='username', required=True)
parser.add_argument('-p',dest='password',nargs='?', help='ask password', required=False)

parser.add_argument('-s', dest='HTTP_SERVER_IP',nargs='+', help='IP Address ',required=False)
parser.add_argument('-port',dest='port',nargs='?', help='HTTP PORT', required=False)
parser.set_defaults(port=80) #Default port=80

parser.add_argument('-f',dest='fwfile',help='firmware file in tar.gz', required=False)
parser.set_defaults(u='admin') #Default user=admin
parser.set_defaults(password='admin') #Default password=admin


args = parser.parse_args()
PORT=args.port
user=args.user
passw=args.password
fwfile=args.fwfile

#serv_ip=args.s
serv_ip=args.HTTP_SERVER_IP

if args.password==None:
	print("")
	try:
		passw= getpass.getpass()
	except:
		print("\nCancelled: exiting....")
		sys.exit()

#IP=args.ip[0]
IP=args.IOM_IP[0]
ipaddr="https://"+IP+"/redfish/v1"

Handler = http.server.SimpleHTTPRequestHandler
headers = {'content-type': 'application/json', 'Cache-Control': "no-cache" }
#httpd=socketserver.TCPServer(("10.50.14.126", PORT), Handler)
#print("serving at port", PORT)
#httpd.serve_forever()
url_fw_upg=ipaddr+'/UpdateService/Actions/UpdateService.SimpleUpdate'

#Image_loc="http://"+serv_ip+":"+str(PORT)+"/"+fwfile
#print(Image_loc)
#payload = "{\n \"ImageURI\": \"http://10.50.14.163:8081/hgst_mm_bundle_200T-073_T2.0.34.tar.gz\"\n }"
#payload = "{\n \"ImageURI\": " + Image_loc + "\n }"
#print(payload)
activate=ipaddr+'/UpdateService/Actions/UpdateService.FWActivate'

#user="admin"
#passw="admin"
#url_encl='https://10.50.14.183/redfish/v1/Chassis/Enclosure'
#r=requests.get(url_encl, auth=HTTPBasicAuth(user,passw), verify=False)
#json_data=r.json()
#print(json_data)
#r = requests.post(url_fw_upg, data=payload, headers=headers)
#r = requests.post(url_fw_upg, data=payload, headers=headers,verify=False,auth=('admin','admin'))

# Need to wait after upload !!
#{"StatusCode":2,"Description":"FW update completed. Waiting for activation.","EstimatedRemainingMinutes":0,"ErrorCode":0}

# /redfish/v1/UpdateService/Actions/UpdateService.SimpleUpdate/Status
url_fw_status=ipaddr+'/UpdateService/Actions/UpdateService.SimpleUpdate/Status'
#print(url_fw_status)
status=requests.get(url_fw_status, auth=HTTPBasicAuth(user,passw), verify=False)
#print(status.text)
json_data=status.json()
#print(json_data)
#print(json_data["Description"],json_data["StatusCode"],json_data["EstimatedRemainingMinutes"],json_data["ErrorCode"])


if json_data["StatusCode"]==2:
	print("Waiting for Activation")
	input_activate=input("Activating firmware will reset both IOMs, do you want to activate firmware now (Y/N)?")
	if(input_activate.lower()=="y"):
		print("Activating new firmware.....")
		s = requests.post(activate, headers=headers,verify=False,auth=(user,passw))
		print("IOMs will reset now please check the status after 10 mins")
if json_data["StatusCode"]==0:
	url_OOBMA=ipaddr+'/UpdateService/FirmwareInventory/IOModuleA_OOBM'
	r=requests.get(url_OOBMA, auth=HTTPBasicAuth(user,passw), verify=False)
	json_fwver=r.json()
	print(json_fwver["Name"],": ",json_fwver["Version"])
	print()
	print("Ready for FW update, please upload the firmware")
	input_upload=input("Do you want to upload firmware (Y/N)?")
	if(input_upload.lower()=="y"):
		print("Uploading firmware. Please wait...")
		if(fwfile==None):
			print("**No firmware file specified**")
		else:
			Image_loc="http://"+serv_ip+":"+str(PORT)+"/"+fwfile
			#payload = "{\n \"ImageURI\": \"http://10.50.14.163:8081/hgst_mm_bundle_200T-073_T2.0.34.tar.gz\"\n }"
			#print(Image_loc)
			payload = "{\n \"ImageURI\": " +'"'+ Image_loc+'"' + "\n }"
			#print(payload)
			r = requests.post(url_fw_upg, data=payload, headers=headers,verify=False,auth=(user,passw))

if json_data["StatusCode"]==1:
	print("Firmware unpacking: Remaining Minutes:",json_data["EstimatedRemainingMinutes"])

#s = requests.post(activate, headers=headers,verify=False,auth=('admin','admin'))
#print(r.text)
