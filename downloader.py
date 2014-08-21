from bs4 import BeautifulSoup
import urllib.request
import os
import traceback

def read_url_page(url):
    #try:
    #page = urllib.request.urlopen(url) paste when url - http instead with open
    #except urllib.request.URLError as exception:
    with open(url, 'r') as page:
        page = page.read()
    
    return page
    
def get_links_list(url):
    links_list = []
    page = read_url_page(url)
    soup = BeautifulSoup(page)
    
    href_list = soup.pre.hr.findAll('a')
    
    for link in href_list:
        links_list.append(link.get('href'))
    
    return links_list

def download_file(url, file_name = None):
    if file_name == None:
        file_name = urllib.parse.urlparse(url)
    
    file_name = os.path.basename(file_name.path)
    
    try:
        response = urllib.request.urlretrieve(url, file_name)
        
        return True
    except IOError as exception:
        raise exception

def do_input(questions_list = ['0: exit', '1: put url']):
    while True:
        print('\nMake a choice(put number):')
        
        number = 0
        
        for question in questions_list:
            print(''.join('{number}: {question}'.format(number = number, question = question)))
            
            number += 1
        
        try:
            answer = int(input('put number: '))
            
            if answer > -1 and answer < len(questions_list):
                return answer
        
        except ValueError as exception:
            print(exception)

    
def main():
    text_html = ''
    folders_list = None
    
    #page = urllib.request.urlopen('saved_resource.html')
    
    folders_list = get_links_list('saved_resource.html')
    
    for link in folders_list:
        print(link)
    
    do_input(folders_list)
    
if __name__ == '__main__':
    main()
    
