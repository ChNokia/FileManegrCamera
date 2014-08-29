import datetime
import os
import sys
import urllib.request

class DataIPCam(object):
    def __init__(self, abspath, date = None, size = None):
        self.__url_parse = urllib.parse.urlparse(abspath)
        self.__size = size
        self.__name = self.__url_parse.path
        #self.__date = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        
        if self.__name == '':
            self.__name = os.path.dirname(abspath)
            self.__is_file = False
        
    @property
    def name(self):
        return self.__name
    
    @property
    def url(self):
        return self.__url_parse.geturl()
    
    @property
    def date(self):
        return self.__date
    
    def get_last_dir(self):
        folders_list = self.__name.split('/')
        
        if self.__size:
            return folders_list[-1]
        
        return folders_list[-2]
