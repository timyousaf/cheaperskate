import mintapi
import copy
import sys
import json
import cPickle as pickle
from elasticsearch import Elasticsearch
import logging
import hashlib

backup_filename = "/Users/timyousaf/.cheaperskate.mint.cache"
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
logging.basicConfig(filename='/Users/timyousaf/cheaperskate.log',level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler())

class MintPipeline():
	
	accounts = {}
	transactions = []

	def loadMintAccount(self, creds):
		email = creds["email"]
		password = creds["password"]
		ius_session = creds["ius_session"]
		thx_guid = creds["thx_guid"]
		owner = creds["owner"]

		logging.info("Querying Mint ...")
		mint = mintapi.Mint(email, password, ius_session, thx_guid)
		transactions = mint.get_transactions()
		transactions = json.loads(transactions.to_json(orient='records', date_format='iso'))
		
		logging.info("Received transactions for {0}".format(email))
		for transaction in transactions:
			  transaction["owner"] = owner

		return transactions

	def saveCache(self):
		logging.info("Caching data")
		with open(backup_filename, 'wb') as output:
			pickle.dump(accounts, output, -1)

	def loadCache(self):
		logging.info("Loading data from cache ...")
		with open(backup_filename, 'rb') as input:
			self.accounts = pickle.load(input)

	def __init__(self, creds_file):
		lines = open(creds_file)
		for line in lines:
			try:
				creds = json.loads(line)
				self.accounts[creds["email"]] = self.loadMintAccount(creds)
			except Exception as e:
				logging.critical("Failed on this Mint account: {}".format(line))
				logging.critical(e)
				sys.exit()

	def hashTransaction(self, transaction):
		transaction = copy.deepcopy(transaction)
		del(transaction["owner"])
		del(transaction["category"])
		m = hashlib.md5()
		m.update(json.dumps(transaction))
		return m.hexdigest()

	def dedupeTransactions(self):
		deduped = {}
		duplicates = 0
		logging.info("Deduping transactions ...")
		# we dedupe on hash after removing the "owner" and "category" fields
		# the first transaction to be seen wins (subsequent duplicates are dropped)
		for account in self.accounts:
			transactions = self.accounts[account]
			for transaction in transactions:
				md5 = self.hashTransaction(transaction)
				if md5 in deduped:
					logging.info("Found a duplicate!")
					duplicates += 1
					logging.info(deduped[md5])
					logging.info(transaction)
					print
				else:
					deduped[md5] = transaction
		dedupedTransactions = []
		for k in deduped:
			dedupedTransactions.append(deduped[k])
		self.transactions = dedupedTransactions
		print "Found {0} duplicates.".format(duplicates)

	def indexTransactions(self):
		logging.info("Deleting ElasticSearch index ...")
		es.indices.delete(index='mint', ignore=[400, 404])

		index_mapping = {
		"mappings" : {
		    'transaction': {
		        "properties": {
		          "account_name": {
		            "type": "string",
		            "index" : "not_analyzed"
		          },
		          "amount": {
		            "type": "double"
		          },
		          "category": {
		            "type": "string",
		            "index" : "not_analyzed"
		          },
		          "date": {
		            "type": "date",
		            "format": "strict_date_optional_time||epoch_millis"
		          },
		          "description": {
		            "type": "string",
		            "index" : "not_analyzed"
		          },
		          "labels": {
		            "type": "string",
		            "index" : "not_analyzed"
		          },
		          "notes": {
		            "type": "string"
		          },
		          "original_description": {
		            "type": "string",
		            "index" : "not_analyzed"
		          },
		          "owner": {
		            "type": "string"
		          },
		          "transaction_type": {
		            "type": "string"
		          }
		        }
		    }
	    }
	    }

		es.indices.create(index='mint', ignore=400, body=index_mapping)

		id = 0
		# for account in self.accounts:
		# 	transactions = self.accounts[account]
		for transaction in self.transactions:
		  es.index(index='mint', doc_type='transaction', id=id, body=transaction)
		  id += 1
		  if id % 100 is 0: logging.info("Indexed {0} transactions ...".format(id))

pipeline = MintPipeline("/Users/timyousaf/mint.txt")
pipeline.dedupeTransactions()
pipeline.indexTransactions()
logging.info("Finished!")