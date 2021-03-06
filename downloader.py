__author__ = 'admin'
resource_file = ''

from bs4 import BeautifulSoup
import urllib.request
import os
import sys
import traceback
import re
import DataIPCam

def read_url_page(url):
    #try:
    page = urllib.request.urlopen(url) #paste when url - http instead with open

    #with open(url, 'r') as page:
    return page.read()

def get_DataIPCam_list(url):
    data_list = []
    page = read_url_page(url)
    soup = BeautifulSoup(page)
    http = None
    date = None
    size = None

    for link in soup.pre.hr:
        str_link = str(link)

        if not http:
            http = re.search('/sd/011/.*\" ', str_link)
        else:
            http_next = re.search('/sd/011/.*\" ', str_link)
			
            if http_next:
                data = DataIPCam.DataIPCam(http.group(0)[:-2], date, size)
                http = http_next
                date = None
                size = None

                data_list.append(data)
            else:
                size = re.search("(\d{1,4})KB", str_link)
                date = re.search("(\d{1,4})-(\d{1,2})-(\d{1,2}) (\d{1,2}):(\d{1,2}):(\d{1,2})", str_link)

                if date:
                    if size:
                        size = size.group(0)

                    data = DataIPCam.DataIPCam(http.group(0)[:-2], date.group(0), size)
                    http = None
                    date = None
                    size = None

                    data_list.append(data)

    return data_list

def download_file(url, file_name = None):
    if file_name == None:
        file_name = urllib.parse.urlparse(url)

    file_name = 'e:/Camera/' + file_name#os.path.basename(file_name.path)

    try:
        response = urllib.request.urlretrieve(url, file_name)

        return True
    except IOError as exception:
        print(exception)
        #raise exception

def do_input(questions_list = [['exit'], ['put url']]):
    while True:
        print('\nMake a choice(put number):')

        do_output(questions_list)

        try:
            answer = int(input('put number: '))

            if answer > -1 and answer < len(questions_list):
                return (answer, questions_list[answer])

        except ValueError as exception:
            #raise ValueError
            print(exception)

def do_output(result_list):
    for number in range(len(result_list)):
        #data = '/t'.join([part for part in result_list[number]])
        print(''.join('{number}: {data}'.format(number = number, data = result_list[number][0])))

def get_links_list(data_list):
    links_list = []

    for data in data_list:
        links_list.append(data.url)

    return links_list

def get_dir_list(data_list):
    links_list = []

    for data in data_list:
        links_list.append([data.get_last_dir(), data.size, data.get_date()])

    return links_list

def main():
    default_questions = ['exit', 'put url']

    while True:
        choice = do_input()

        if choice[1][0] == 'exit':
            sys.exit(1)

        url = input('put url(http://host): ')
        #url_test = 'http://localhost:8090' #delete when not test
        try:
            data_list = get_DataIPCam_list(url + '/sd/011/')
			
            while True:
                try:
                    #page = urllib.request.urlopen(url)
                    #except urllib.request.URLError as exception:
                    #data_list = get_DataIPCam_list(url + '' + resource_file)
                    folders_list = get_dir_list(data_list)

                    #for i in range(len(default_questions)):
                    folders_list.insert(0, [default_questions[0]])
                    folders_list.append(['download files'])
					
                    choice = do_input(folders_list)

                    if choice[1][0] == 'exit':
                        sys.exit(1)
                    if choice[1][0] == 'download files':
                        folder_name = input('put folder name: ')
                        number_download = 1

                        for obj in [object for object in data_list if object.size]:
                            print('downloading {0} file from {1}'.format(obj.get_last_dir(), url + obj.name))

                            if download_file(url + obj.name, '{0}/{1}'.format(folder_name, obj.get_last_dir())) == True: #download_file(obj.url, obj.name)
                                print('{0} -> {1} download'.format(number_download, obj.get_last_dir()))

                                number_download = number_download + 1

                        continue
                    #data_list = get_DataIPCam_list(url + data_list[choice[0] - 1].name + resource_file)
                    data_list = get_DataIPCam_list(url + data_list[choice[0] - 1].name + '/')

                except urllib.error.URLError as exception:
                    print('------1111URLError------')
                    print(url + data_list[choice[0] - 1].name + '/')
                    print(exception)
                except urllib.error.HTTPError as exception:
                    print('------HTTPError------')
                    print(exception)
                except ValueError as exception:
                    print('------ValueError------')
                    print(exception)
        except urllib.error.URLError as exception:
            print('------URLError------')
            print(exception)
        except urllib.error.HTTPError as exception:
            print('------HTTPError------')
            print(exception)
        except ValueError as exception:
            print('------ValueError------')
            print(exception)

if __name__ == '__main__':
    main()
