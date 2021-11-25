from pymongo import MongoClient
import time
import os
import base64

L = os.listdir("./ccassignment1")
Images = {}

for img in L:
	with open("./ccassignment1/"+img,"rb") as f:
		data = f.read()
		tmp = base64.b64encode(data)
		image = tmp.decode("utf-8")
		Images[img] = image

client = MongoClient("mongo-service",27017)

client.drop_database("CC_Categories")

mydb = client["CC_Categories"]

#Animal's Collection
catcoll = mydb["AnimalRights"]

mylist = [
{ "actId": 10001, "username": "user1", "timestamp": time.strftime('%d-%m-%Y:%S-%M-%H', time.gmtime()), "caption": "He has a right to criticize, who has a heart to help.", "upvotes": 0, "imgB64": Images["dog_save.jpg"]},
{ "actId": 10002, "username": "user3", "timestamp": time.strftime('%d-%m-%Y:%S-%M-%H', time.gmtime()), "caption": "An animal's eyes have the power to speak a great language.", "upvotes": 0, "imgB64": Images["wildlife.jpg"]},
{ "actId": 10003, "username": "user5", "timestamp": time.strftime('%d-%m-%Y:%S-%M-%H', time.gmtime()), "caption": "We only have what we give.", "upvotes": 0, "imgB64": Images["nature.jpg"]},
{ "actId": 10004, "username": "user2", "timestamp": time.strftime('%d-%m-%Y:%S-%M-%H', time.gmtime()), "caption": "No one has ever become poor by giving.", "upvotes": 0, "imgB64": Images["cleaning.jpg"]}
]

x = catcoll.insert_many(mylist)

print(x.inserted_ids)


#Cleanliness collection
catcoll = mydb["Cleanliness"]

mylist = [
{ "actId": 20001, "username": "user2", "timestamp": time.strftime('%d-%m-%Y:%S-%M-%H', time.gmtime()), "caption": "He has a right to criticize, who has a heart to help.", "upvotes": 0, "imgB64": Images["cleaning_2.jpg"]},
{ "actId": 20002, "username": "user5", "timestamp": time.strftime('%d-%m-%Y:%S-%M-%H', time.gmtime()), "caption": "Cleanliness is a state of purity, clarity, and precision", "upvotes": 0, "imgB64": Images["cleaning_3.jpg"]},
{ "actId": 20003, "username": "user3", "timestamp": time.strftime('%d-%m-%Y:%S-%M-%H', time.gmtime()), "caption": "No act of kindness, no matter how small, is ever wasted.", "upvotes": 0, "imgB64": Images["cleaning_4.jpg"]},
{ "actId": 20004, "username": "user1", "timestamp": time.strftime('%d-%m-%Y:%S-%M-%H', time.gmtime()), "caption": "No one has ever become poor by giving.", "upvotes": 0, "imgB64": Images["cleaning_5.jpg"]}
]

x = catcoll.insert_many(mylist)

print(x.inserted_ids)




#HelpThePoor collection
catcoll = mydb["HelpThePoor"]

mylist = [
{ "actId": 30001, "username": "user4", "timestamp": time.strftime('%d-%m-%Y:%S-%M-%H', time.gmtime()), "caption": "Give, but give until it hurts", "upvotes": 0, "imgB64": Images["poor_1.jpg"]},
{ "actId": 30002, "username": "user3", "timestamp": time.strftime('%d-%m-%Y:%S-%M-%H', time.gmtime()), "caption": "No one is useless in this world who lightens the burdens of another.", "upvotes": 0, "imgB64": Images["poor_2.jpg"]},
{ "actId": 30003, "username": "user1", "timestamp": time.strftime('%d-%m-%Y:%S-%M-%H', time.gmtime()), "caption": "We only have what we give.", "upvotes": 0, "imgB64": Images["poor_3.jpg"]},
{ "actId": 30004, "username": "user2", "timestamp": time.strftime('%d-%m-%Y:%S-%M-%H', time.gmtime()), "caption": "No one has ever become poor by giving.", "upvotes": 0, "imgB64": Images["poor_4.jpg"]}
]

x = catcoll.insert_many(mylist)

print(x.inserted_ids)




#NatureConserve collection
catcoll = mydb["NatureConserve"]

mylist = [
{ "actId": 40001, "username": "user1", "timestamp": time.strftime('%d-%m-%Y:%S-%M-%H', time.gmtime()), "caption": "Give, but give until it hurts", "upvotes": 0, "imgB64": Images["nature.jpg"]},
{ "actId": 40002, "username": "user2", "timestamp": time.strftime('%d-%m-%Y:%S-%M-%H', time.gmtime()), "caption": "No one is useless in this world who lightens the burdens of another.", "upvotes": 0, "imgB64": Images["cleaning.jpg"]},
{ "actId": 40003, "username": "user3", "timestamp": time.strftime('%d-%m-%Y:%S-%M-%H', time.gmtime()), "caption": "We only have what we give.", "upvotes": 0, "imgB64": Images["cleaning_5.jpg"]},
{ "actId": 40004, "username": "user4", "timestamp": time.strftime('%d-%m-%Y:%S-%M-%H', time.gmtime()), "caption": "No one has ever become poor by giving.", "upvotes": 0, "imgB64": Images["cleaning_6.jpg"]}
]

x = catcoll.insert_many(mylist)

print(x.inserted_ids)

