from plaid import Client
from plaid import errors as plaid_errors
from plaid.utils import json
from optparse import OptionParser
import sys

parser = OptionParser()
parser.add_option("-f", "--file", dest="filename",
                  help="Specify the file from which to load credentials.")
(options, args) = parser.parse_args()

if options.filename:
	try:
		creds_file =  open(filename)
	except:
		print("Failed to open file. Please pass a valid filename with -f.")
		sys.exit()
else:
	print("Please specify a filename with -f.")
	sys.exit()

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
	sys.exit()
else:
	connect_data = response.json()
	print connect_data['access_token']