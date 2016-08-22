from plaid import Client
from plaid import errors as plaid_errors
from plaid.utils import json
import sys

class PlaidClient():

	def __init__(self, filename):
		creds_file =  open(filename)
		creds = json.loads(creds_file.read())
		self.creds = creds
		self.loadTransactions()

	def loadTransactions(self):
		creds = self.creds		
		client_id = creds["client_id"]
		secret = creds["secret"]
		account_type = creds["account_type"]
		username = creds["username"]
		password = creds["password"]  	

		Client.config({
			'url': 'https://tartan.plaid.com'
		})
		client = Client(client_id=client_id, secret=secret)
		
		try:
		    response = client.connect(
		    	account_type, 
		    	{
			     'username': username,
			     'password': password
		    	})
		except plaid_errors.PlaidError as e:
			print e.message
			print("Failed to load transactions from Plaid API.")
			sys.exit()
		else:
			connect_data = response.json()
			transactions = connect_data["transactions"]
			print "Loaded {0} {1} transactions.".format(len(transactions), account_type)
			cleaned = []
			for transaction in transactions:
				cleaned.append({ "date" : transaction["date"], 
								 "name" : transaction["name"], 
								 "amount": transaction["amount"] 
								 } )
			if cleaned:
				self.transactions = cleaned
			else:
				print("Failed to load transactions from Plaid API.")
				sys.exit()

	def getTransactions(self):
		return self.transactions