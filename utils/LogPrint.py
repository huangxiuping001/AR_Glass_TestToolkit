#-*-coding: UTF-8 -*-
'''
Created on 2018年8月20日

@author: admin
'''

import time
import os
class LogPrint(object):
    '''
    classdocs
    '''


    def __init__(self,filepath):
        '''
        Constructor
        '''
        self.langtextfile=open(filepath, 'w')
        self.reportpath = os.path.abspath(os.path.join(os.getcwd(), "../Report")) + "//"
        #self.resultfile = open(self.reportpath + 'KeyOnline_standardresult.txt', 'a')


    def print_log(self, state,content):
        content = content
        t = '[' + time.strftime('%Y-%m-%d-%H-%M-%S') + ']'
        self.langtextfile.write(t +"\t"+ state+"\t"+content+"\n")
        self.langtextfile.flush()
        
    def close_log(self):
        self.langtextfile.close()

