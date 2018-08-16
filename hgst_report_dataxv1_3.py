#######################################################
# Author: Nitin Kushwah
#
#History:
#v1.3: Added OOBM firmware, reordering expander output
#V1.2: Added support for Data102/4U102
#v1.1: Added support for Data60/4U60G3
#
#
########################################################
import json
import requests
import time
import os
from requests.auth import HTTPBasicAuth
import argparse
import getpass
import sys
print("\n")
print('This is \'Beta\' version 1.3 . This utility collects useful information from the Data60 and Data102 JBODs. This version doesn\'t verify HTTP Certificate. Press Ctrl+C if you do not wish to continue.')
print("\n")

parser = argparse.ArgumentParser(description='This is \'Beta\' version 1.1 . This utility collects useful information from the Data60 and Data102 JBODs. This version doesn\'t verify HTTP Certificate')
parser.add_argument('-ip', nargs='+', help='IP Address ',required=True)
parser.add_argument('-o',help='Outfile', required=True)

parser.add_argument('-u',help='username', required=True)
parser.add_argument('-p',nargs='?', help='ask password', required=False)


parser.set_defaults(u='admin') #Default user=admin
parser.set_defaults(p='admin') #Default password=admin

args = parser.parse_args()
user=args.u
passw=args.p
outfile=args.o
if args.p==None:
	print("")
	try:
		passw= getpass.getpass()
	except:
		print("\nCancelled: exiting....")
		sys.exit()
#print("User: %s" %user)
#print("Pass: %s" %passw)

sys.stdout = open(os.path.join(os.getcwd(),outfile), "a")
#sys.stdout = sys.__stdout__

start_time = time.time()
if os.name == 'nt':
	from requests.packages.urllib3.exceptions import InsecureRequestWarning
	requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
line = "-"*90

#################################################
## Replace below IP with the IOM IP Address
#IP="10.50.14.159"
IP=args.ip[0]
ipaddr="https://"+IP+"/redfish/v1"
print(ipaddr)
#################################################

url_encl=ipaddr+'/Chassis/Enclosure'
r=requests.get(url_encl, auth=HTTPBasicAuth(user,passw), verify=False)
json_data=r.json()
print()
#print("Status: ",r.status_code)
sys.stdout = sys.__stdout__
print("Connected")
print("Collecting Enclosure information")
sys.stdout = open(os.path.join(os.getcwd(),outfile), "a")
print("Model:",str(str(json_data["Model"])))
print("Serial:",str(json_data["SerialNumber"]))
print(json_data["Status"])

#Power#
sys.stdout = sys.__stdout__
print("Collecting Power Supply status")
sys.stdout = open(os.path.join(os.getcwd(),outfile), "a")
url_enclPower=ipaddr+'/Chassis/Enclosure/Power'
r=requests.get(url_enclPower, auth=HTTPBasicAuth(user,passw), verify=False)
json_data=r.json()
print()
print("PSU:")
print("PSU A: ",str(json_data["PowerSupplies"][0]["SerialNumber"]),str(json_data["PowerSupplies"][0]["Status"]))
print("PSU B: ",str(json_data["PowerSupplies"][1]["SerialNumber"]),str(json_data["PowerSupplies"][1]["Status"]))



#Thermal
sys.stdout = sys.__stdout__
print("Collecting Thermal status")
sys.stdout = open(os.path.join(os.getcwd(),outfile), "a")
url_thermal=ipaddr+'/Chassis/Enclosure/Thermal'
r=requests.get(url_thermal, auth=HTTPBasicAuth(user,passw), verify=False)
json_data=r.json()
print()
print("Temperature Sensors:")
for i in range(0,len(json_data["Temperatures"])):
	print(str(json_data["Temperatures"][i]["Name"]),str(json_data["Temperatures"][i]["Status"]))


#Host Port
sys.stdout = sys.__stdout__
print("Collecting Host Port status")
sys.stdout = open(os.path.join(os.getcwd(),outfile), "a")
url_self = ipaddr+'/Systems/Self/'
r=requests.get(url_self, auth=HTTPBasicAuth(user,passw), verify=False)
json_data_host=r.json()
print()
print("Host port:")
#print("Status: ",r.status_code)
hostports=len(json_data_host["Oem"]["WDC"]["SASHostPorts"])
for i in range(0,hostports):
	print("Host Port:"+str(json_data_host["Oem"]["WDC"]["SASHostPorts"][i]["Id"])+" Connected: "+str(json_data_host["Oem"]["WDC"]["SASHostPorts"][i]["IsCableConnected"]))




#########IOM A , OOBM A ##########
sys.stdout = sys.__stdout__
print("Collecting OOBM Firmware")
sys.stdout = open(os.path.join(os.getcwd(),outfile), "a")
url_OOBMA=ipaddr+'/UpdateService/FirmwareInventory/IOModuleA_OOBM'
#url_OOBMA=ipaddr+/UpdateService/FirmwareInventory/IOModuleB_OOBM
r=requests.get(url_OOBMA, auth=HTTPBasicAuth(user,passw), verify=False)
json_data=r.json()
print()
print("IOM A:")
print(json_data["Name"],json_data["Version"])




#ipaddr+'/Chassis/IOModuleAFRU
sys.stdout = sys.__stdout__
print("Collecting IO Modules ")
sys.stdout = open(os.path.join(os.getcwd(),outfile), "a")
url_IOMA=ipaddr+'/Chassis/IOModuleAFRU'
r=requests.get(url_IOMA, auth=HTTPBasicAuth(user,passw), verify=False)
json_data=r.json()
print()

print(str(json_data["Id"]),str(json_data["SerialNumber"]),str(json_data["Status"]))


url = ipaddr+'/Systems/Self/EthernetInterfaces/IOModuleAFRU'
r=requests.get(url, auth=HTTPBasicAuth(user,passw), verify=False)
#print(r.headers)
#print("Result: \n",r.text)
#print(r.encoding)
json_data=r.json()
print()
#print("Status: ",r.status_code)
print(str(json_data["Name"]))
print("MAC Address:",str(json_data["PermanentMACAddress"]))
print("Status:",str(json_data["LinkStatus"]))
print("Network Details:",str(json_data["IPv4Addresses"]))

print()




######## IOM B , OOBM B #####
sys.stdout = sys.__stdout__
print("Collecting OOBM Firmware")
sys.stdout = open(os.path.join(os.getcwd(),outfile), "a")
url_OOBMB=ipaddr+'/UpdateService/FirmwareInventory/IOModuleB_OOBM'
r=requests.get(url_OOBMB, auth=HTTPBasicAuth(user,passw), verify=False)
json_data=r.json()
print()
print("IOM B:")
print(json_data["Name"],json_data["Version"])


url_IOMB=ipaddr+'/Chassis/IOModuleBFRU'
r=requests.get(url_IOMB, auth=HTTPBasicAuth(user,passw), verify=False)
json_data=r.json()
#print()
print(str(json_data["Id"]),str(json_data["SerialNumber"]),str(json_data["Status"]))

url2 = ipaddr+'/Systems/Self/EthernetInterfaces/IOModuleBFRU'
r=requests.get(url2, auth=HTTPBasicAuth(user,passw), verify=False)
json_data=r.json()
print()
#print("Status: ",r.status_code)
print(str(json_data["Name"]))
print("MAC Address:",str(json_data["PermanentMACAddress"]))
print("Status:",str(json_data["LinkStatus"]))
print("Network Details:",str(json_data["IPv4Addresses"]))
####################



###### Expanders ######
sys.stdout = sys.__stdout__
print("Collecting Expander status")
sys.stdout = open(os.path.join(os.getcwd(),outfile), "a")
expanders=len(json_data_host["Oem"]["WDC"]["SASExpanders"])
print()
print("Expanders:")
for i in range(0,expanders):
	print(str(json_data_host["Oem"]["WDC"]["SASExpanders"][i]["Name"]),str(json_data_host["Oem"]["WDC"]["SASExpanders"][i]["Id"]), str(json_data_host["Oem"]["WDC"]["SASExpanders"][i]["FirmwareVersion"]),str(json_data_host["Oem"]["WDC"]["SASExpanders"][i]["Identifiers"]["DurableName"]),str(json_data_host["Oem"]["WDC"]["SASExpanders"][i]["Status"]))




###### DISKS #####
#ipaddr+'/Systems/Self/Storage
sys.stdout = sys.__stdout__
print("Collecting Disk information")
sys.stdout = open(os.path.join(os.getcwd(),outfile), "a")
url_storage = ipaddr+'/Systems/Self/Storage'
r=requests.get(url_storage, auth=HTTPBasicAuth(user,passw), verify=False)
json_data=r.json()
print()
#print(str(json_data["Members"])
for x in json_data["Members"]:
	url_storage=url_storage+"/"+x["@odata.id"].split("/")[6]

#print(url_storage)

url_disks=url_storage
r=requests.get(url_disks, auth=HTTPBasicAuth(user,passw), verify=False)
json_data=r.json()
print()
total_disks=len(json_data["Drives"])


def toGB(x):
	try:
		return str(int(x/1000000000))+" GB"
	except:
		return x


print("Slot    ","Status ","Serial  ","Size    ","Blk","Mfg ","Model          ","Rev ","SAS","Typ","Ind","Predictive")
print(line)
for i in range(1,total_disks+1):
	#print(i)
	#print("ipaddr+'/Systems/Self/Storage/5000CCAB04001580/Drives/"+str(i))
	url_drive=url_storage+"/Drives/"+str(i)
	#url_drive="ipaddr+'/Systems/Self/Storage/5000CCAB04001580/Drives/"+str(i)
	r=requests.get(url_drive, auth=HTTPBasicAuth(user,passw), verify=False)
	json_data=r.json()
	#print(str(json_data["Name"])
	x=str(json_data["CapacityBytes"])
	print(str(json_data["Name"]),str(json_data["Status"]["State"]),str(json_data["SerialNumber"]),toGB(x),str(json_data["BlockSizeBytes"]),str(json_data["Manufacturer"]),str(json_data["PartNumber"]),str(json_data["Revision"]),str(json_data["Protocol"]),str(json_data["MediaType"]), str(json_data["IndicatorLED"]), str(json_data["FailurePredicted"]))


print("Total time: %s seconds ---" % (time.time() - start_time))
print(line)
sys.stdout = sys.__stdout__
print("Completed")