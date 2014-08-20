from bs4 import BeautifulSoup
import urllib.request

def main():
    text_html = ''
    folders_list = None
    
    #page = urllib.request.urlopen('saved_resource.html')
    
    with open('saved_resource.html', 'r') as file:
        text_html = file.read()
        
    soup = BeautifulSoup(text_html)
    
    folders_list = soup.pre.hr.findAll('a')
    
    for link in folders_list:
        print(link.get('href'))

if __name__ == '__main__':
    main()
    
