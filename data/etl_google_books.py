import sqlalchemy
from sqlalchemy import create_engine, MetaData
##from credentials import user, password, host, database
import requests
import pandas as pd


host = 'ec2-18-235-86-66.compute-1.amazonaws.com'
port = "5432"
database = "da1c06fi82ev6c"
user = "tjhqznxnlxlreh"
password = "f21ee19a9e50d41255f16288c978201fbbffd3fc9e22b644fb03b904f5216056"
api_key = 'AIzaSyAoJKviB_VKhQ6AZeJ8eHs3ycSOhw_ErmI'


conn_str = f"postgresql://{user}:{password}@{host}/{database}"
engine = create_engine(conn_str)
connection = engine.connect()
metadata = MetaData()

titles_authors = engine.execute("SELECT title,authors FROM books_eng").fetchall()

titles_authors_df = pd.DataFrame(titles_authors)

##for titles in titles_authors:
##    print(titles)


##response = requests.get(f'https://www.googleapis.com/books/v1/volumes?q=Master of the Game+inauthor:Sidney Sheldon&key={api_key}')
##response_json = response.json()



'''for i in range(len(response_json['items'])):
    if response_json['items'][i]['volumeInfo']['language'] == 'es':
        print(response_json['items'][i]['volumeInfo']['title'])'''


def extract_titles(lst, api_key = 'AIzaSyAoJKviB_VKhQ6AZeJ8eHs3ycSOhw_ErmI', url='https://www.googleapis.com/books/v1/volumes?q='):
    '''
    url: Url from the API
    lst: List of tuples with the title and author information to search with the API
    api_key: API key
    return: Dataframe with the titles in spanish
    '''
    titles_lst = []
    for element in lst:
        title = element[0]
        author = element[1]
        ##print(f'{url}intitle:{title}+inauthor:{author}&key={api_key}')
        response = requests.get(f'{url}intitle:{title}+inauthor:{author}&key={api_key}')
        response_json = response.json()
        try:
            if 'items' in response_json.keys():
                ##print(response_json)
                for i in range(len(response_json['items'])):
                    if response_json['items'][i]['volumeInfo']['language'] == 'es':
                        spanish_title = response_json['items'][i]['volumeInfo']['title']
                        titles_lst.append((spanish_title,lst.index(element)))
                        break
                        ##print(response_json['items'][i]['volumeInfo']['title'])
                    elif i == len(response_json['items']) - 1 :
                            titles_lst.append(('',lst.index(element)))
                            break
                    else:
                        pass
            else:
                titles_lst.append(('',lst.index(element)))
        except:
            titles_lst.append(('',lst.index(element)))
        print(titles_lst)
    return titles_lst


df = extract_titles(titles_authors)

