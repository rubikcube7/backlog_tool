import requests
import os
import shutil
import openpyxl
import time
import sys
import configparser
from distutils.util import strtobool
from pathlib import Path


class Main(object):
    def __init__(self):
        config_path = Path(__file__).parent
        config_path /= '../config.ini'
        config = configparser.ConfigParser()
        config.read(config_path)
        self.BACKLOG_HOST = config['URL']['BACKLOG_HOST']
        self.BACKLOG_API_KEY = config['KEY']['BACKLOG_API_KEY']
        self.USER_DIR_PATH = config['PATH']['USER_DIR_PATH']
        self.USER_DIR_PATH_STG_VI = config['PATH']['USER_DIR_PATH_STG_VI']
    def run(self):
        self.ISSUES_KEY = input()
        self.USER_DIR_PATH_STG = self.USER_DIR_PATH_STG_VI + self.ISSUES_KEY
        params = {'apiKey': self.BACKLOG_API_KEY}
        r = requests.get(self.BACKLOG_HOST + '/api/v2/issues/'+ self.ISSUES_KEY, params=params)
        info = r.json()
        print(info['summary'])
        des_info = info['description']
        obj_des_info = des_info.split('\n')

        for issue in obj_des_info:
            issue2 = issue.replace('svn//',self.USER_DIR_PATH)
            print(issue2)
            if os.path.exists(issue2):
                if not os.path.exists(self.USER_DIR_PATH_STG):
                    os.mkdir(self.USER_DIR_PATH_STG)
                shutil.copy(issue2, self.USER_DIR_PATH_STG)
                shutil.make_archive(self.USER_DIR_PATH_STG, 'zip', root_dir=self.USER_DIR_PATH_STG_VI)


if __name__ == '__main__':
    main = Main()
    main.run()