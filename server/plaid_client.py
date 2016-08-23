from plaid import Client
from plaid import errors as plaid_errors
from plaid.utils import json
import sys

class PlaidClient():
	
	def __init__(self, filename):
		# real plaid client
		creds_file =  open(filename)
		creds = json.loads(creds_file.read())
		self.creds = creds
		self.loadTransactions()

	def loadTransactions(self):
		creds = self.creds		
		client_id = creds["client_id"]
		secret = creds["secret"]
		amex_access_token = creds["amex_access_token"]
		
		print client_id, secret, amex_access_token

		Client.config({
			'url': 'https://tartan.plaid.com'
		})
		client = Client(client_id=client_id, secret=secret, access_token=amex_access_token)

		try:
		    response = client.connect_get()
		except plaid_errors.PlaidError as e:
			print e.message
			print("Failed to load transactions from Plaid API.")
			sys.exit()
		else:
			connect_data = response.json()
			transactions = connect_data["transactions"]
			print "Loaded {0} transactions.".format(len(transactions))
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

	def getMockTransactions(self):
		return [
				{ "date" : "2016-05-03", "amount" : 11.65, "name" : "Uber" },
				{ "date" : "2016-05-13", "amount" : 23.04, "name" : "Uber" },
				{ "date" : "2016-05-16", "amount" : 13.41, "name" : "Uber" },
				{ "date" : "2016-05-26", "amount" : 17.11, "name" : "Uber" },
				{ "date" : "2016-05-27", "amount" : 13.16, "name" : "Uber" },
				{ "date" : "2016-05-29", "amount" : 15.02, "name" : "Uber" },
				{ "date" : "2016-05-30", "amount" : 11.29, "name" : "Uber" },
				{ "date" : "2016-06-06", "amount" : 30.03, "name" : "Uber" },
				{ "date" : "2016-06-15", "amount" : 32.11, "name" : "Uber" },
				{ "date" : "2016-06-25", "amount" : 10.74, "name" : "Uber" },
				{ "date" : "2016-07-03", "amount" : 11.89, "name" : "Uber" },
				{ "date" : "2016-07-05", "amount" : 26.95, "name" : "Uber" },
				{ "date" : "2016-07-22", "amount" : 19.59, "name" : "Uber" },
				{ "date" : "2016-07-23", "amount" : 41.52, "name" : "Uber" },
				{ "date" : "2016-07-25", "amount" : 85.26, "name" : "Uber" },
				{ "date" : "2016-07-27", "amount" : 59.29, "name" : "Uber" },
				{ "date" : "2016-07-29", "amount" : 58.50, "name" : "Uber" },
				{ "date" : "2016-08-02", "amount" : 9.93, "name" : "Uber" },
				{ "date" : "2016-08-07", "amount" : 13.97, "name" : "Uber" },
				{ "date" : "2016-08-14", "amount" : 12.98, "name" : "Uber" },
				{ "date" : "2016-08-16", "amount" : 5.44, "name" : "Uber" },
				{ "date" : "2016-08-19", "amount" : 9.43, "name" : "Uber" },
				{ "date" : "2016-09-03", "amount" : 20.32, "name" : "Uber" },
				{ "date" : "2016-09-06", "amount" : 9.55, "name" : "Uber" },
				{ "date" : "2016-10-03", "amount" : 17.41, "name" : "Uber" },
				{ "date" : "2016-10-06", "amount" : 92.53, "name" : "Uber" },
				{ "date" : "2016-11-01", "amount" : 44.01, "name" : "Uber" },
				{ "date" : "2016-12-02", "amount" : 24.16, "name" : "Uber" },
				{ "date" : "2016-12-04", "amount" : 17.35, "name" : "Uber" },
				{ "date" : "2016-12-06", "amount" : 42.84, "name" : "Uber" }
			]