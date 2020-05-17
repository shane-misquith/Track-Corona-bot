import requests
from bs4 import BeautifulSoup
from data import html
import json
import datetime
import logging
from tabulate import tabulate
import argparse

FORMAT = '[%(asctime)-15s] %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG, filename='bot.log', filemode='a')

URL = "https://www.mohfw.gov.in/"
response = requests.get(URL).content
soup = BeautifulSoup(response , "html.parser")
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
	parser  = argparse.ArgumentParser()
	parser.add_argument('--states', default=',')
	args = parser.parse_args()
	interested_states = args.states.split(',')

	try:
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
				if any([s.lower() in row[1].lower() for s in interested_states]):
					row.append(row)

		cur_data = {x[1]: {current_time: x[2:]} for x in row}
		past_data = load()

		new_state = []
		isChanged = False
		for state in cur_data:
			if state not in past_data:
				new_state.append(f'{state} Added to the list : {cur_data[state][current_time]}')
				past_data[state] = {}
				isChanged = True
			else:
				past = past_data[state]['latest']
				cur =  cur_data[state][current_time]
				if past != cur:
					isChanged = True
					new_state.append(f'Change for {state}: {past}->{cur}')

		if isChanged:
			for state in cur_data:
				past_data[state]['latest'] = cur_data[state][current_time]
				past_data[state][current_time] = cur_data[state][current_time]
			save(past_data)

		events_info = ''
		for event in info:
			logging.warning(event)
			events_info += '\n - ' + event.replace("'", "")

		table = tabulate(row, headers= t_header, tablefmt='psql')

	except Exception as e:
		logging.exception('Script Failure')
