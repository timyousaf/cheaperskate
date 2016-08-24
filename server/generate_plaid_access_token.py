from plaid import Client
from plaid import errors as plaid_errors
from plaid.utils import json
from optparse import OptionParser
import sys

client_id = raw_input("Please enter your client id: ")
secret = raw_input("Please enter your secret: ")

Client.config({
	'url': 'https://tartan.plaid.com'
})
client = Client(client_id=client_id, secret=secret)

try:
    institutions = client.institutions().json()
    valid_account_types = []
    for institution in institutions:
    	valid_account_types.append(institution['type'])
except plaid_errors.PlaidError as e:
	print e.message
	sys.exit()

account_type = raw_input("Please enter the account type (institution) :")

if account_type not in valid_account_types:
	print("{0} is not a valid account. These are the valid accounts: {1}"
		.format(account_type, json.dumps(valid_account_types)))
	sys.exit()

username = raw_input("Please enter your username: ")
password = raw_input("Please enter your password: ")
		
try:
    response = client.connect(
    	account_type, 
    	{
	     'username': username,
	     'password': password
    	})
except plaid_errors.PlaidError as e:
	print e.message
	sys.exit()
else:
	connect_data = response.json()
	access_token = connect_data['access_token']
	print "Your access token is {}".format(access_token)
	print "Try retrieving transactions with this curl command:"
	print "curl -X POST https://tartan.plaid.com/connect/get -d client_id={0} -d secret={1} -d access_token={2}".format(
		client_id,
		secret,
		access_token)