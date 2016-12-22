import mintapi
import sys
import json
import cPickle as pickle
from elasticsearch import Elasticsearch

backup_filename = "/Users/timyousaf/.cheaperskate.mint.cache"
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

def indexMintTransactions(account):

	email = account["email"]
	password = account["password"]
	ius_session = account["ius_session"]
	thx_guid = account["thx_guid"]

	print "Deleting ElasticSearch index ..."
	es.indices.delete(index='test-index', ignore=[400, 404])
	
	print "Querying Mint ..."
	mint = mintapi.Mint(email, password, ius_session, thx_guid)
	transactions = mint.get_transactions()

	print "Received transactions. Caching ..."
	with open(backup_filename, 'wb') as output:
		pickle.dump(transactions, output, -1)

	print "Indexing transactions in ElasticSearch ..."
	with open(backup_filename, 'rb') as input:
		transactions = pickle.load(input)
		transactions = json.loads(transactions.to_json(orient='records', date_format='iso'))

		id = 0
		for transaction in transactions:
		  es.index(index='mint', doc_type='transaction', id=id, body=transaction)
		  id += 1
		  if id % 100 is 0: print "Indexed {0} transactions ...".format(id)

	print "Done!"

creds_file = open("/Users/timyousaf/mint.txt")
for line in creds_file:
	try:
		account = json.loads(line)
		indexMintTransactions(account)
	except Exception as e:
		print("Failed on this Mint account: {}".format(line))
		print e
		sys.exit()