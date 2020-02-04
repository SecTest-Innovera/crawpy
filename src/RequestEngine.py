import threading
import sys
from src.Handler import Handler
import requests
import urllib3
import time
import os
from tqdm import tqdm

try:
    from io import BytesIO
except ImportError:
    from StringIO import StringIO as BytesIO


class Requester:
    def __init__(self,url):

        ### vars ###
        self.targets = []
        self.target_len = 0
        self.len_prepped = 0
        self.total_len_prepped = 0
        self.f_name = None

        ### flags ###
        self.prep_stop_flag = False        
        self.fuzz_stop_flag = False
        self.is_cawling = False
        self.is_finished = False

        ###  configs ###
        self.timeout = 3
        self.n_threads = 30
        self.url = self.parse_url(url)
        self.redirect = False
        self.headers = {
            'User-Agent': 'crawpy/1.1',
            'Connection': 'closed'
        }
        self.http_method = ''
        self.retries = urllib3.util.retry.Retry(total=3,
               backoff_factor=0.1,
               status_forcelist=[ 500, 502, 503, 504 ])
        self.exts = None

        ###  objects ###
        self.handler = Handler()
        self.handler.status_codes = [200,204,301,302,307,401,403]
        self.prepared_requests = []
        self.session = requests.Session()
 
        self.session.mount('http://', requests.adapters.HTTPAdapter(max_retries=self.retries))
        self.session.mount('https://', requests.adapters.HTTPAdapter(max_retries=self.retries))


        return

    def load_targets(self, f_name):
        self.f_name = f_name
        with open(f_name, "r") as f:
            for line in f:
                self.targets.insert(0,self.url + line.replace("\n", ""))
        self.target_len = len(self.targets)
        f.close()
        return    

    def update_extensions(self,ext):
        _targets = []
        for target in self.targets:
            _targets.insert(0,target)
            for e in ext:
                _targets.insert(0,"{}.{}".format(target,e))
        self.targets = _targets
        return

    def fuzz(self):
        sys.stdout.write("\r")
        #print("Prepped requests in fuzz {}".format(self.len_prepped))
        self.prepare_requests()
        t_list = []
        self.fuzz_stop_flag = False
        for t in range(self.n_threads):
            t = threading.Thread(target=self.req,)
            t_list.append(t)
            t.daemon = True
            t.start()
        for t in t_list:
            try:
                t.join()
            except KeyboardInterrupt:
                os.system("stty echo")
                sys.stderr.write("\r")
                self.handler.info("Interrupt recieved, Exiting...")
                sys.exit(0)

        return

    def req(self):
        while self.fuzz_stop_flag != True:
            try:                
                resp = self.session.send(self.prepared_requests.pop(),timeout=self.timeout,allow_redirects=self.redirect)                
                self.handler.handle_request(resp)
                self.len_prepped -= 1

            except IndexError:
                self.stop_flag = True
                return
            except urllib3.exceptions.MaxRetryError:
                continue
            except requests.exceptions.ConnectTimeout:
                continue
            except urllib3.exceptions.ReadTimeoutError:
                continue
            except requests.exceptions.ReadTimeout:
                continue
            except urllib3.exceptions.NewConnectionError:
                self.handler.error("!","Error")
        return

    def prep(self):
        while self.prep_stop_flag != True:
            try:
                target = self.targets.pop()
                self.prepared_requests.insert(0,requests.Request(self.http_method, target , headers=self.headers).prepare())
                self.len_prepped += 1
            except IndexError:
                self.prep_stop_flag = True
                return

        return

    def prepare_requests(self):
        t_list = []
        self.prep_stop_flag = False
        for t in range(self.n_threads):
            t = threading.Thread(target=self.prep,)
            t_list.append(t)
            t.daemon = True
            t.start()
                
        for t in t_list:
            t.join()

        if self.handler.pbar:
            self.handler.pbar.reset(total=self.target_len)
        else:
            self.handler.pbar = tqdm(
                total=self.target_len,ncols=50,desc="Fuzzing",
                bar_format="Fuzzing -> {percentage:3.2f}% {bar} {n_fmt}/{total_fmt} #")

        return


    def crawl(self):

        self.handler.info("Crawling...")        
        self.is_cawling = True
        if len(self.handler.directories) == 0:
            self.handler.error("!","No directories found quitting")
            self.is_finished = True

        while self.is_finished == False:
            self.url = self.parse_url(self.handler.directories.pop())
            self.load_targets(self.f_name)
            self.update_extensions(self.exts)
            self.target_len = len(self.targets)
            self.prepare_requests()

            self.handler.pbar.clear()
            sys.stdout.write("\n")
            self.handler.dinfo("Directory",self.url)
            self.fuzz()

            if len(self.handler.directories) == 0:
                self.is_finished = True  




    @staticmethod
    def parse_url(url):
        if url[-1] != "/":
            url += "/"
        return url
    
