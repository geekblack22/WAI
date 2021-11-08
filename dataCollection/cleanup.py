from random import sample
import database
from datetime import datetime, timedelta
import algos
import sys
import twitterInterface
from dotenv import load_dotenv
import os 
import time
import pickle

def main():
	load_dotenv()
	
	consumer_key = os.getenv('consumer_key')
	consumer_secret = os.getenv('consumer_secret')
	server_1 = os.getenv('server_1')
	uid_1 = os.getenv('uid_1')
	database_1 = os.getenv('database_1')
	pwd_1 = os.getenv('pwd_1')
	server_2 = os.getenv('server_2')
	database_2 = os.getenv('database_2')
	uid_2 = os.getenv('uid_2')
	pwd_2 = os.getenv('pwd_2')
	bearer_token = os.getenv('test_token')
	

	db = database.Database(server_2,database_2,uid_2,pwd_2)
	db.clean()
	db.cursor.commit()


if __name__ == "__main__":
	main()
