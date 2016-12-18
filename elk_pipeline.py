import json
from server.plaid_client import PlaidClient
from server.calculator import Calculator
import os
from elasticsearch import Elasticsearch

plaid_client = PlaidClient("/Users/timyousaf/plaid.txt")
transactions = plaid_client.getTransactions()

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

id = 0
for transaction in transactions:
  print transaction
  es.index(index='transactions', doc_type='transaction', id=id, body=transaction)
  id += 1