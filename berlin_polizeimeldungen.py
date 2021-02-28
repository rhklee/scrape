import requests
import csv
from bs4 import BeautifulSoup
import time


if __name__ == '__main__':
    host = 'https://www.berlin.de'
    url_base = f'{host}/polizei/polizeimeldungen/archiv'
    page_param = 'page_at_1_0='
    
    years = range(2021, 2013, -1)
    with open('polizeimeldungen.csv', 'w') as c:
        csvwriter = csv.writer(c)
        for year in years:
            page = 1
            while True:
                url = f'{url_base}/{year}/?{page_param}' + str(page)
                print(url)
                r = requests.get(url, allow_redirects=False)

                if r.status_code != 200:
                    print(f'Status code was = {r.status_code}')
                    break

                soup = BeautifulSoup(r.text, 'html.parser')
                html_rows = soup.find_all('li', class_='row-fluid')
                for html_row in html_rows:
                    row = []
                    row.append(html_row.find('div', class_='date').string)
                    html_text = html_row.find('div', class_='text')

                    location = ''
                    if html_text.find('span', class_='category') is not None:
                        location = html_text.find('span', class_='category').get_text()
                    row.append(location)
                    row.append(html_text.find('a').string)
                    row.append(host + html_text.find('a').get('href'))
                    csvwriter.writerow(row)
                page += 1
                time.sleep(0.75)

