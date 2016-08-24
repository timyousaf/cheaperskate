from plaid import Client
from plaid.utils import json
import cPickle as pickle
import sys

CACHE_FILENAME = "/Users/timyousaf/cheaperskate.cache"

class PlaidClient():
	
	account_clients = {}
	transactions = []

	def __init__(self, filename):
		creds_file =  open(filename)
		for line in creds_file:
			try:
				account = json.loads(line)
				self.initializeClient(account)
			except Exception as e:
				print e
				print("Failed to initialize Plaid client from line: {}".format(line))

		if len(self.account_clients) == 0:
			print("Failed to initalize any Plaid clients from the file {}".format(filename))
			sys.exit()

		self.loadTransactions()

	def initializeClient(self, account):
		client_id = account["client_id"]
		secret = account["secret"]
		access_token = account["access_token"]
		account_type = account["account_type"]

		Client.config({
			'url': 'https://tartan.plaid.com'
		})
		client = Client(client_id=client_id, secret=secret, access_token=access_token)

		self.account_clients[account_type] = client

	def loadTransactions(self):

		all_transactions = []

		for account_type in self.account_clients:
			try:
				account_client = self.account_clients[account_type]
				response = account_client.connect_get()
			except Exception as e:
				print e.message
				print("Failed to load transactions from Plaid API for account {}".format(account_type))
			else:
				connect_data = response.json()
				account_transactions = connect_data["transactions"]
				print "Loaded {0} transactions for account {1}.".format(len(account_transactions), account_type)
				cleaned = []
				for transaction in account_transactions:
					cleaned.append({ "date" : transaction["date"], 
									 "name" : transaction["name"], 
									 "amount": transaction["amount"] 
									 } )
				all_transactions.extend(cleaned)

		if len(all_transactions) == 0:
			print("Failed to load any transactions from the Plaid API. Attempting to load from cache ...")
			try:
				self.loadTransactionsFromCache()
			except Exception as e:
				print e
				print("Failed to load transactions from cache :( exiting.")
				sys.exit()
		else:
			print("Loaded total of {} transactions.".format(len(all_transactions)))
			self.transactions = all_transactions
			self.saveTransactionsToCache()

	def saveTransactionsToCache(self):
		with open(CACHE_FILENAME, 'wb') as output:
			pickle.dump(self.transactions, output, -1)
		print("Cached transactions to disk.")

	def loadTransactionsFromCache(self):
		with open(CACHE_FILENAME, 'rb') as input:
			self.transactions = pickle.load(input)
			print("Loaded transactions from cache.")

	def getTransactions(self):
		return self.transactions