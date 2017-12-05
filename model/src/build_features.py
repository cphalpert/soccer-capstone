
def build_features(data)

	X = data[['age','weight','height']].to_dict('records')
	Y = data['market_val']
	return X, Y