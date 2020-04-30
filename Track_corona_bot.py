import requests
from bs4 import BeautifulSoup
from data import html
import json
import datetime

# URL = "https://www.mohfw.gov.in/"
# response = requests.get(URL).content
# soup = BeautifulSoup(response , "html.parser")
soup = BeautifulSoup(html , "html.parser")
extract_contents = lambda row: [x.text for x in row]
t_header = extract_contents(soup.find_all('th'))
FILE_NAME = 'covid19_data_india.json'

def save(data):
	with open(FILE_NAME, 'w') as file:
		json.dump(data, file)
	return

def load():
	old_data = {}
	with open(FILE_NAME, 'r') as file:
		old_data = json.load(file)
	return old_data


if __name__ == '__main__':
	current_time = datetime.datetime.now().strftime('%d/%m/%Y %H:%M')
	row = []
	for all_rows in soup.find_all('tr'):
		row_data = extract_contents(all_rows.find_all('td'))
		if len(row_data) == 1:
			pass
		elif len(row_data) == 4 :
			row_data = ['', *row_data]
			row.append(row_data)
		elif len(row_data) == 5:
			row.append(row_data)

	cur_data = { i[1] : {current_time: i[2:],"latest": []}  for i in row }
	save(cur_data)
	past_data = load()

	# isChanged = False
	# for state in cur_data:
	# 	if state not in past_data:
	# 		info.append(f'{state} Added to the list : {cur_data[state][current_time]}')
	# 		past_data[state] = {}
	# 		isChanged = True
	# 	else:
	# 		past = past_data[state][current_time]
	# 		cur = cur_data[state][current_time]
	# 		if past != cur:
	# 			changed = True
	# 			info.append(f'Change for {state}: {past}->{cur}')
	#
	# if isChanged:
	# 	for state in cur_data:
	# 		past_data[state]['latest'] = cur_data[state][current_time]
	# 		past_data[state][current_time] = cur_data[state][current_time]
	# save(past_data)

	# for state  in cur_data:
	# 	past = past_data[state]
	# 	cur = cur_data[state][current_time]
	# 	print(past, cur)
	for state  in cur_data:
		print(cur_data[state][current_time])
