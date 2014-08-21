from bs4 import BeautifulSoup
import urllib.request
import os
import sys
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

def do_input(questions_list = ['exit', 'put url']):
    while True:
        print('\nMake a choice(put number):')
        
        do_output(questions_list)
        
        try:
            answer = int(input('put number: '))
            
            if answer > -1 and answer < len(questions_list):
                return (answer, questions_list[answer])
        
        except ValueError as exception:
            print(exception)

def do_output(result_list):
    for number in range(len(result_list)):
        print(''.join('{number}: {data}'.format(number = number, data = result_list[number])))
    
def main():
    default_questions = ['exit', 'put url']
    choice = do_input()
    
    if choice[1] == 'exit':
        sys.exit(1)
    
    url = input('put url: ')
    
    while True:
        #page = urllib.request.urlopen(url)
        folders_list = get_links_list('saved_resource.html')
        
        for i in range(len(default_questions)):
            folders_list.insert(i, default_questions[i])
        #    print(link)
        choice = do_input(folders_list)
        
        if choice[1] == 'exit':
            sys.exit(1)

if __name__ == '__main__':
    main()
    
