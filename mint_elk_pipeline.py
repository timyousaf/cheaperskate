import mintapi
import sys
import json
import cPickle as pickle
from elasticsearch import Elasticsearch

backup_filename = "/Users/timyousaf/.cheaperskate.mint.cache"
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

class MintPipeline():
	
	accounts = {}

	def loadMintAccount(self, creds):
		email = creds["email"]
		password = creds["password"]
		ius_session = creds["ius_session"]
		thx_guid = creds["thx_guid"]
		owner = creds["owner"]

		print "Querying Mint ..."
		mint = mintapi.Mint(email, password, ius_session, thx_guid)
		transactions = mint.get_transactions()
		transactions = json.loads(transactions.to_json(orient='records', date_format='iso'))
		
		print "Received transactions for {0}".format(email)
		for transaction in transactions:
			  transaction["owner"] = owner

		return transactions

	def saveCache(self):
		print "Caching data ..."
		with open(backup_filename, 'wb') as output:
			pickle.dump(accounts, output, -1)

	def loadCache(self):
		print "Loading data from cache ..."
		with open(backup_filename, 'rb') as input:
			self.accounts = pickle.load(input)

	def __init__(self, creds_file):
		lines = open(creds_file)
		for line in lines:
			try:
				creds = json.loads(line)
				self.accounts[creds["email"]] = self.loadMintAccount(creds)
			except Exception as e:
				print("Failed on this Mint account: {}".format(line))
				print e
				sys.exit()

	def index(self):
		print "Deleting ElasticSearch index ..."
		es.indices.delete(index='test-index', ignore=[400, 404])

		id = 0
		for account in self.accounts:
			transactions = self.accounts[account]
			for transaction in transactions:
			  es.index(index='mint', doc_type='transaction', id=id, body=transaction)
			  id += 1
			  if id % 100 is 0: print "Indexed {0} transactions ...".format(id)

pipeline = MintPipeline("/Users/timyousaf/mint.txt")
pipeline.index()
print "Finished!"