import numpy as np
import pandas as pd
import datetime
import dateutil
import json

class Calculator():

	def parseTransactions(self, transactions):

		for transaction in transactions:
			if transaction['name'] in ("Seamless","GrubHub"):
				transaction['name'] = "Seamless"
			else:
				if "Food and Drink" in transaction['category']:
					transaction['name'] = "FoodAndDrink"

		t_df = pd.DataFrame(transactions)

		start_days_ago = 730
		end_days_from = 1
		bucket = 'M' # D = day, W = week, M = month

		# not actually sure what this does ...
		df = t_df[ t_df.name.str.contains("Uber|Seamless|Amazon|FoodAndDrink") ]
		df['date'] = df['date'].apply(dateutil.parser.parse, dayfirst=True)
		df = pd.pivot_table(df,index=["date"], columns=["name"], values=["amount"], aggfunc=[np.sum])
		now = datetime.datetime.now()
		start = now - datetime.timedelta(days=start_days_ago)
		end = now + datetime.timedelta(days=end_days_from)
		idx = pd.date_range(start.strftime("%m-%d-%Y"), end.strftime("%m-%d-%Y"))
		df = df.reindex(idx, fill_value=0)	
		df = df.resample(bucket, how='sum', axis=0)
		df.index.names = ['date']
		df = df['sum']['amount']
		df = df.reset_index().to_json(orient='records', date_format='iso')

		# HACKHACK because I'm too lazy to figure out pandas
		hack = json.loads(df)
		for thing in hack:
			thing['date'] = thing['date'].split('T')[0]
		self.transactions = hack

	def getTransactions(self):
		return json.dumps(self.transactions)
		