import requests as req
from bs4 import BeautifulSoup as soup

url = 'https://sunibcurhat.com/'

response = req.get(url)
print(f'Status Code : {response.status_code}')

webdata = soup(response.text,'html.parser')
print(webdata.prettify())

button = webdata.find('button',{'class':'btn btn-warning btn-round'})
print(f'Text: {button.b.text}')

posts = webdata.findAll('p', {'class':'description mt-auto'})
for i, post in enumerate(posts):
    print(f'Post {i+1}.\n{post.text}\n')

refs = webdata.findAll('a', {'class':'nav-link'})
print(refs[1]['href'])