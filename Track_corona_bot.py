import requests
from bs4 import BeautifulSoup
import csv
from data import html

# URL = "https://www.mohfw.gov.in/"
# response = requests.get(URL)
soup = BeautifulSoup(html, "html.parser")
extract_contents = lambda row: [x.text for x in row]
t_header = extract_contents(soup.find_all('th'))

row = []
# all_rows = soup.find_all('tr')
for all_rows in soup.find_all('tr'):
	row_data = extract_contents(all_rows.find_all('td'))
	# print(row_data)
	# if len(row):
	if len(row_data) == 1:
		pass
	elif len(row_data) == 4 :
		row_data = ['', *row_data]
		row.append(row_data)
	elif len(row_data) == 5:	
		row.append(row_data)

for i in row:
	print(i)
# print(row)
