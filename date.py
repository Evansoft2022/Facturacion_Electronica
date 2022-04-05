from datetime import date

def Count_Days(d):
	future_date = date(d[0], d[1], d[2])
	today = date.today()
	_days = (future_date - today).days
	return _days

# date_ = "2022-03-01"
# _date = date_.split('-')
# dates = list(map(int, _date))
# print(Count_Days())
