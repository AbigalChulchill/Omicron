import sys
sys.path.insert(1,'lib')

import requests
import time

from urllib.parse import urlencode


class BinanceException(Exception):


    def __init__(self, status_code, data):
        self.status_code = status_code
        if data:
            self.code = data['code']
            self.msg = data['msg']
        else:
            self.code = None
            self.msg = None
        message = f"{status_code} [{self.code}] {self.msg}"
        super().__init__(message)


if __name__ == '__main__':

    

    pass

    
