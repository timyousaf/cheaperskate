import numpy as np
import pandas as pd
import datetime
import dateutil
import json

class Calculator():

	def __init__(self):
		pass

	def parseTransactions(self, transactions):
		df = pd.DataFrame(transactions)

		start_days_ago = 500
		end_days_from = 1
		bucket = 'W' # D = day, W = week, M = month
		
		df = df[ df.name.str.contains("Uber") ]
		df['date'] = df['date'].apply(dateutil.parser.parse, dayfirst=True)
		df = df.groupby(['date'])['amount'].sum()
		df = df.resample(bucket, axis=0).sum() # re-groups & sums by week
		df = df.reset_index().to_json(orient='records', date_format='iso')
		# HACKHACK because I'm too lazy to figure out pandas
		hack = json.loads(df)
		for thing in hack:
			thing['uber'] = thing['amount']
			thing['date'] = thing['date'].split('T')[0]
		self.uber_transactions = hack

	def getUberTransactions(self):
		return json.dumps(self.uber_transactions)
		