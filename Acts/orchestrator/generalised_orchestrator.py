from flask import Flask, jsonify,request
#import pymongo
#from pymongo import MongoClient
from apscheduler.schedulers.background import BackgroundScheduler
#import time
#import threading
#import os
#import base64
import json
#import re
#import random
from flask_cors import CORS
#import datetime
import requests
import docker
#from threading import Timer
#from threading import Lock
from collections import OrderedDict


app = Flask(__name__)

cors = CORS(app, resources={r"/api/*": {"origins":"*"}})

URL = 'http://localhost:' #URl or IP address of the machine
next_port = -1
client = docker.from_env()
port_cont_map = {}
port = 8000
portVal = 8000
counter = 0
job1 = None
job2 = None
start_counter = 0
dont_count = ['/api/v1/_health','/api/v1/_crash']

ImageName = None
HealthCheckTimeDelay = None
ScalingTimeDelay = None
RequestsGap = None
#StartingPort, Database, Network, MappedPort

for cont in client.containers.list():
	if not(cont.name=='mongo'):
		port_cont_map[port] = cont.short_id
		port = port + 1
port_cont_map = OrderedDict(port_cont_map)
print("This is the start : ", port_cont_map)


def health_check():

	global port_cont_map
	for port in port_cont_map.keys():
		try:
			response = requests.get(url = URL+str(port)+"/api/v1/_health")
			print("Container running on port "+str(port)+" returned status "+str(response.status_code)+"\n")
			if response.status_code==500:
				down_container(port_cont_map[port],port)
				up_container(port)
				port_cont_map = OrderedDict(sorted(port_cont_map.items()))
		except:
			print("Waiting to bring up containers \n")


def up_container(port):

	global port_cont_map
	obj = client.containers.run(ImageName, ports = {'80/tcp':port}, privileged=False, detach=True, network="acts_default")
	port_cont_map[port] = obj.short_id
	print("Container with id "+str(obj.short_id)+" launched on port "+str(port)+"\n")

def down_container(cont_id,port):

	global port_cont_map
	cont = client.containers.get(cont_id)
	cont.kill()
	del port_cont_map[port]
	print("Container with id "+str(cont_id)+" on port "+str(port)+" is killed \n")

def launch_containers(num):

	global portVal
	global port_cont_map
	num_cont = len(port_cont_map)
	if(num_cont < num):
		while(num_cont < num):
			portVal = portVal + 1
			up_container(portVal)
			num_cont = num_cont + 1
	if(num_cont > num):
		port_cont_map = OrderedDict(sorted(port_cont_map.items()))
		while(num_cont > num):
			down_container(port_cont_map[list(port_cont_map.keys())[-1]], (list(port_cont_map.keys())[-1]))
			portVal = portVal - 1
			num_cont = num_cont -1


def scale(val):

	global port_cont_map
	global portVal
	print("\n"+ "scaling " + str(val))
	c=len(port_cont_map)
	if(val < RequestsGap):
		if(c > 1):
			port_cont_map = OrderedDict(sorted(port_cont_map.items()))
			while(c > 1):
				down_container(port_cont_map[list(port_cont_map.keys())[-1]], (list(port_cont_map.keys())[-1]))
				portVal = portVal - 1
				c = c - 1
	launch_containers((val//RequestsGap)+1)
	print("# of containers " + str(len(port_cont_map)) + "\n")
	print(port_cont_map)
	return(port_cont_map)  


def sca():
	#k = random.randint(0,199)
	global counter
	k = counter
	print(str(k) + " requests received after 2 min \n")
	counter = 0
	scale(k)
	
def round_robin():

	global next_port
	num_running_cont = len(client.containers.list())-1 
	next_port = (next_port + 1)%num_running_cont
	port = 8000+next_port
	return port
	
	
#@app.route('/', defaults={'path': ''},methods=['POST','GET','DELETE','HEAD','PUT'])
@app.route('/<path:path>',methods=['POST','GET','DELETE','HEAD','PUT'])
def redirect_all(path):

	global start_counter
	global counter
	if path not in dont_count:
		if (start_counter == 0) and (counter == 0):
			start_counter = 1
			job2 = scheduler.add_job(sca, 'interval', seconds=ScalingTimeDelay)
			counter = counter + 1
		else:
			counter = counter + 1
    
	port = round_robin()
	qs = request.query_string
	url = None
	if len(qs)==0:
		url = URL+str(port)+'/'+path
	else:
		URL+str(port)+'/'+path+'?'+qs
	response = None
	
	if request.method == 'GET':
		response = requests.get(url = url)
	if request.method == 'POST':
		try:
			data = json.dumps(json.loads(request.data))
		except:
			data = None
		headers = {'content-type':'application/json'}
		response = requests.post(url = url, data = data, headers = headers)
	if request.method == 'DELETE':
		response = requests.delete(url = url)
	if request.method == 'PUT':
		try:
			data = json.dumps(json.loads(request.data))
		except:
			data = None
		headers = {'content-type':'application/json'}
		response = requests.put(url = url, data = data, headers = headers)
	if request.method == 'HEAD':
		response = requests.head(url = url)
		
	try:
		obj = response.json()
	except:
		obj = {}
	print("response received from port ",next_port)
	return jsonify(obj), response.status_code


if __name__ == '__main__':

	with open('settings.json') as json_file:
		data = json.load(json_file)
		ImageName = data["settings"]["ImageName"]
		HealthCheckTimeDelay = data["settings"]["HealthCheckTimeDelay"]
		ScalingTimeDelay = data["settings"]["ScalingTimeDelay"]
		RequestsGap = data["settings"]["RequestsGap"]

	scheduler = BackgroundScheduler()
	job1 = scheduler.add_job(health_check, 'interval', seconds=HealthCheckTimeDelay)
	#job2 = scheduler.add_job(sca, 'interval', seconds = 120)
	scheduler.start()
	app.run(debug=False,host='0.0.0.0',port=80)
