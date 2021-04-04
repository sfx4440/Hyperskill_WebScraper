import requests
from bs4 import BeautifulSoup
import string
import os

orig_dir = os.getcwd()
url = 'https://www.nature.com/nature/articles'

num_pages = int(input('Enter number of pages to search: '))
article_type = input('Enter the article type: ')

for i in range(num_pages):
    os.mkdir(f'Page_{i + 1}')
    os.chdir(f'Page_{i + 1}')
    r = requests.get(url)
    r1 = r.content

    soup = BeautifulSoup(r.content, 'html.parser')

    test1 = soup.find_all('article')
    spans = soup.find_all('span', {'data-test': 'article.type'})
    lines = [span.get_text().strip() for span in spans]
    li_pages = soup.find('li', {'data-test': 'page-next'})
    page_indicators = li_pages.find('a').get('href')

    url_dict = {}
    for n in range(len(lines)):
        if lines[n] == article_type:
            a = test1[n].find('a')
            a_title = test1[n].find('a').text.strip()
            print(a_title)
            url_dict[str(a_title)] = ('https://www.nature.com' + str(a.get('href')))

    container = []
    title_list = list(url_dict.keys())
    for j in range(len(url_dict)):
        article_title = title_list[j]
        translator = str.maketrans(' ', '_'
                                        '', string.punctuation)
        article_title = article_title.translate(translator)
        with open(f'{article_title}.txt', 'wb') as file:
            r2 = requests.get(url_dict[title_list[j]])
            soup2 = BeautifulSoup(r2.content, 'html.parser')
            container.append(soup2.find('div',  {'class': 'article-item__body'}).text.strip())
            file.write(container[j].encode())

    os.chdir(orig_dir)
    url = 'https://www.nature.com' + page_indicators
