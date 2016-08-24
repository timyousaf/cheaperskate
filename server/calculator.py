import numpy as np
import pandas as pd
import datetime
import dateutil
import json
import copy

class Calculator():

	def __init__(self, chart_config):
		self.chart_config = chart_config

	def parseTransactions(self, transactions):

		synthetic_transactions = []
		for transaction in transactions:
			for chart in self.chart_config['lines']:
				if transaction['name'] in chart['matchNames'] or not set(transaction['category']).isdisjoint(set(chart['matchCategories'])):
					monster = copy.deepcopy(transaction)
					monster['name'] = chart['key']
					synthetic_transactions.append(monster)

		filters = []
		for chart in self.chart_config['lines']:
			filters.append(chart['key'])

		filter_string = '|'.join(filters)

		t_df = pd.DataFrame(synthetic_transactions)

		start_days_ago = 730
		end_days_from = 1
		bucket = 'M' # D = day, W = week, M = month

		# not actually sure what this does ...
		df = t_df[ t_df.name.str.contains(filter_string) ]
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
		