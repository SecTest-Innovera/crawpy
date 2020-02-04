import sys

class Handler:
    def __init__(self):
        self.directories = []
        self.found_resps = []
        self.status_codes = None
        self.pbar = None
        return

    def handle_request(self,resp):
        self.pbar.update(1)
        if resp.status_code in self.status_codes:
            if resp.status_code == 301 or resp.status_code == 302 or resp.status_code == 307:
                self.warning(resp.status_code,resp.url)
                self.directories.insert(0,resp.url)
                self.found_resps.insert(0,resp)
                return

            elif resp.status_code == 403 or resp.status_code == 401:
                self.error(resp.status_code,resp.url)
                return
            self.success(resp.status_code,resp.url)
            self.found_resps.insert(0,resp)
            return
        else:
            return


    def info(self,string):
        self.pbar.clear()
        sys.stdout.write("\033[94m[*] {}\033[97m\n".format(string))
    
    def error(self,code,string):  
        self.pbar.clear()
        sys.stdout.write("\33[91m[{}] {}\033[97m\n".format(code,string))   
    
    def warning(self,code, string):        
        self.pbar.clear()
        sys.stdout.write("\033[93m[{}] {}\033[97m\n".format(code, string))

    def success(self,code, string):
        self.pbar.clear()
        sys.stdout.write("\033[92m[{}] {}\033[97m\n".format(code, string))
    
    def dinfo(self,code,string):
        self.pbar.clear()
        sys.stdout.write("\033[95m[{}] {}\033[97m\n".format(code, string))
    
    def berror(self,code,string):  
        sys.stdout.write("\33[91m[{}] {}\033[97m\n".format(code,string))  

    def bsuccess(self,code, string):
        sys.stdout.write("\033[92m[{}] {}\033[97m\n".format(code, string))
   
    def binfo(self,string):
        sys.stdout.write("\033[94m[*] {}\033[97m\n".format(string))
