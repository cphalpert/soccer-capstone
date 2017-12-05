import pandas as pd


def make_dataset():
	"""Return pandas dataframe with raw data set"""
	PATH = '/Users/chalpert/Documents/Columbia/Capstone/soccer-capstone/model/data/'
	data = pd.read_csv(PATH + 'Players_Combined_v3.csv')
	return data