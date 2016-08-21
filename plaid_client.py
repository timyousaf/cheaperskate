from plaid import Client
from plaid import errors as plaid_errors
from plaid.utils import json

filename = "/Users/timyousaf/plaid.txt"
creds_file =  open(filename)
creds = json.loads(creds_file.read())
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
else:
	connect_data = response.json()
	transactions = connect_data["transactions"]
	print json.dumps(transactions)

