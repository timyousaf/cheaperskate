import numpy as np
import pandas as pd
import datetime
import dateutil

class Calculator():

	def __init__(self):
		pass

	def parseTransactions(self, transactions):
		df = pd.DataFrame(transactions)

		start_days_ago = 500
		end_days_from = 1
		
		df = df[ df.name.str.contains("Uber") ]
		df['date'] = df['date'].apply(dateutil.parser.parse, dayfirst=True)
		df = df.groupby(['date'])['amount'].sum()
		df = df.resample('W', how='sum', axis=0) # re-groups & sums by week
		print df
