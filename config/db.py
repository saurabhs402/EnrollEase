from dotenv import load_dotenv,find_dotenv
import os
import pprint

from pymongo import MongoClient
load_dotenv(find_dotenv())

password=os.environ.get("MONGO_PASSWORD");

Uri=f"mongodb+srv://saurabh:{password}@cluster0.kvokpzd.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client=MongoClient(Uri)

db=client.libraryManagement;
studentsCollection=db['students']

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)



