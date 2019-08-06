# -*- coding: utf-8 -*-
import random
import requests
import threading
import resource
import sys
import time

class CRAWPY:
    def __init__(self, URL,fileName,threads):

        # recursion limit
        #sys.setrecursionlimit(1000000)
        # connection limit
        resource.setrlimit(resource.RLIMIT_CORE, (resource.RLIM_INFINITY,resource.RLIM_INFINITY))


        #color stuff
        self.RED = "\033[1;31m"
        self.BLUE = "\033[1;34m"
        self.CYAN = "\033[1;36m"
        self.GREEN = "\033[0;92m"
        self.RESET = "\033[0;0m"
        self.BOLD = "\033[;1m"
        self.REVERSE = "\033[;7m"

        #banner
        self.banner = CRAWPY_BANNER()
        print (self.BOLD)  # to make whole stream bold
        self.banner.hello()  # greet people

        #inputs from user
        self.isCrawling = False
        self.isFinished = False
        self.fileName = fileName
        self.nThreads = threads
        self.timeOut = 5
        self.extentions = []
        self.port = 80
        self.baseUrl = self.parse_url(URL)
        self.url = self.parse_url(URL)
        self.info("URL : "+self.url)

        #default vars
        self.threadList = []
        self.directories = []
        self.statusCodes = []
        self.headers = {
            'User-Agent': 'crawpy/1.0',
            'Connection': 'Closed'
        }
        self.targets = []
        self.targetLen = 0
        self.load_file(self.fileName)
        self.session = requests.Session()
        self.isFuzzFinished = False
        
        self.foundUrls = [] #each one is a response object
        #self.bar = CRAWPY_PROGRESSBAR(self.targetLen)
        self.info("Given wordlist: {0}".format(self.fileName))
        self.info("Number of threads: {0}".format(self.nThreads))

    def chunker(self, list, size):
        return (list[i::size] for i in range(size))
    def load_file(self, fileName):
        with open(fileName, "r") as f:
            if len(self.extentions) != 0:
                self.targets = []
                for line in f:
                    flag = False
                    try:
                        for item in self.extentions:
                            if "." + item in line:
                                flag = True
                            self.targets.append(self.url + line.replace("\n", "") + "." + item)
                        # both with extention and directory itself
                        if not flag:
                                self.targets.append(self.url + line.replace("\n", ""))
                    except:
                        pass
            else:
                for line in f:
                    self.targets.append(self.url + line.replace("\n", ""))
        self.targets.reverse()
        self.targetLen = len(self.targets)
        f.close()
        return

    @staticmethod
    def parse_url(url):
        #if ":" in url:
        #    self.port = url.split(":")[1]

        if url[-1] != "/":
            url += "/"
        return url


    def req(self):
        while self.isFuzzFinished != True:

            #self.info("Left urls: {0}".format(len(self.targets)))
            # pop one url from targets
            try:
                #   self.info("Sending request")
                url = self.targets.pop() # its a complete url
                self.targetLen -= 1
                prepped = requests.Request('HEAD', url, headers=self.headers).prepare()
                r = self.session.send(prepped, allow_redirects=False, timeout=self.timeOut)
                #self.bar.next()
                self.handle_request(r)

                    #  self.info("Handled request, continuing")

            except IndexError:
                #must be return
                #self.info("Index error")
                self.isFuzzFinished = True
                return
            except Exception, e:
                #self.info(e)
                pass

            except (KeyboardInterrupt, SystemExit):
                sys.exit(1)
        return
    def handle_request(self,response):
        if response.status_code in self.statusCodes:
            if response.status_code == 301:
                self.warning("301", response.url)
                self.directories.append(response.url)
                self.foundUrls.append(response)
                return
            elif response.status_code == 403:
                self.error("403",response.url)
                return
            self.success(response.status_code, response.url)
            self.foundUrls.append(response)
            return
        else:
            return


    def fuzz(self):
        self.threadList = []
        self.isFuzzFinished = False
        for t in range(self.nThreads):

            t = threading.Thread(target=self.req, )
            self.threadList.append(t)
            t.daemon = True
            t.start()

        for t in self.threadList:
            t.join()

        #clear threadList
        return

    def crawl(self):
        print ("")
        print ("Continuing to crawl !!")
        self.isCrawling = True
        if len(self.directories) == 0:
            self.error("!","No directories found quitting")
            self.isFinished = True

        while not self.isFinished:
            self.url = self.parse_url(self.directories.pop())
            self.load_file(self.fileName)
            print ("")
            print ("/"+self.url.replace(self.baseUrl,""))
            self.fuzz()

            if len(self.directories) == 0:
                self.isFinished = True
    
    def info(self,string):
        print("\033[94m[*] {}\033[97m".format(string))

    def error(self,code,string):
        print("\33[91m[{}]] {}\033[97m".format(code,string))
    def warning(self,code, string):
        print("\033[93m[{}] {}\033[97m".format(code, string))

    def success(self,code, string):
        print("\033[92m[{}] {}\033[97m".format(code, string))


class CRAWPY_SCREENSHOT:
    def __init__(self,browserName):
        from selenium import webdriver
        if browserName == "firefox":
            self.browser = webdriver.Firefox()
        elif browserName == "chrome":
            self.browser = webdriver.Chrome()
        else:
            print "Unknown browser error,\n Please choose chrome or firefox"
            sys.exit(1)
        self.directory = "screenshots/"
    def clip(self,url):
        self.browser.get(url)
        url = url.split("//")[1]
        url = url.replace("/","-").replace(".","-")
        time.sleep(1)

        self.browser.save_screenshot(self.directory + url + ".png")
        self.success("Screenshot saved : "+url+".png")
        return

    def success(self,string):
        print("\033[92m[*] {}\033[97m".format(string))

class CRAWPY_BANNER:

    def __init__(self):
        self.banners = []
        self.banners.append(
            """
                                    ⡿⠿⠛⠋⠉⠁⠀⠀⣀⣀⣀⠀⠉⠉⠛⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
                                    ⠀⢀⣤⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣦⣄⡈⠙⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
                                    ⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⡈⠻⣿⣿⣿⣿⣿⣿⣿⣿
                                    ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⡉⠙⠻⢿⣿⣿⣿⣿⣿⢿⣦⠈⢻⣿⣿⣿⣿⣿⣿
                                    ⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⡆⠀⠀⢻⣿⣿⣿⣿⡆⠈⢳⡄⠹⣿⣿⣿⣿⣿
                                    ⣿⣿⣿⣿⣿⣿⣿⠈⢿⣿⣿⣿⣷⠖⠀⠀⣿⣿⣿⣿⣿⣄⠀⣿⡄⠘⣿⣿⣿⣿
                                    ⣿⣿⣿⣿⣿⣿⣿⣇⠀⢄⡙⠋⠻⡄⠀⣼⣿⣿⣿⣩⠟⠟⠀⣼⣿⡄⠹⣿⣿⣿
                                    ⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣭⣤⣤⣴⣿⣿⣿⣿⣿⣿⣿⣦⣴⣿⣿⣷⠀⠛⠻⣿
                                    ⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⠿⠿⢿⣿⣿⣶⣶⣶⣶⣾⣿⣿⣿⣿⣿⣿⢰⣶⣄⠈
                                    ⣏⣉⣛⣛⣛⣛⣥⣶⣾⣿⣿⣿⣷⡝⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⡇
                                    ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⠟⠀
                                    ⡇⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢋⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠈⠁⢀⣼
                                    ⡇⠀⠹⣿⣿⣿⡿⠿⠛⣋⣥⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⣾⣿⣿
            """)
        self.banners.append("""
                                    ────────────██████████──████────
                                    ────────████▒▒░░░░░░░░██▒▒░░██──
                                    ──────██▒▒░░░░██░░██░░░░██░░░░██
                                    ────██▒▒░░░░░░██░░██░░░░░░▒▒░░██
                                    ────██░░░░░░░░██░░██░░░░░░▒▒▒▒██
                                   ──██░░░░░░▒▒▒▒░░░░░░▒▒▒▒░░░░▒▒██
                                    ██▒▒░░░░░░░░░░░░██░░░░░░░░░░░░██
                                    ██░░░░▒▒░░░░░░░░██░░░░░░░░░░▒▒██
                                    ██░░░░▒▒░░░░░░░░░░░░░░░░░░░░██──
                                    ──██████░░░░░░░░░░░░░░░░░░▒▒██──
                                    ██▒▒▒▒▒▒██░░░░░░░░░░░░░░░░▒▒██──
                                    ██▒▒▒▒▒▒▒▒██░░░░░░░░░░░░▒▒██────
                                    ██▒▒▒▒▒▒▒▒██░░░░░░░░░░▒▒████────
                                    ──██▒▒▒▒▒▒▒▒██▒▒▒▒▒▒████▒▒▒▒██──
                                    ────██▒▒▒▒██████████▒▒▒▒▒▒▒▒▒▒██
                                    ──────██████──────████████████──
        """)

    def hello(self):
        print ("                                            WELCOME TO CRAWPY v1.0")
        print (self.banners[random.randint(0, len(self.banners) - 1)])

class CRAWPY_PROGRESSBAR:
    def __init__(self,length):
        from progress.bar import Bar
        self.bar = Bar('Scanning',max=length)
        return
