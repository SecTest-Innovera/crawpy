import sys
import argparse
from CRAWPY import CRAWPY
from CRAWPY import CRAWPY_SCREENSHOT
import time

"""
todo: implement virtual host fuzzing
"""

if __name__ == "__main__":


    parser = argparse.ArgumentParser()

    parser.add_argument("-u", "--url", dest="url",help="URL")
    parser.add_argument("-w", "--wordlist", dest="wordlist", help="Wordlist")
    parser.add_argument("-t", "--threads", dest="threads", help="Number of threads",default=30)
    parser.add_argument("-r", "--recursive", dest="recursive",action='store_true',help="Recursive scan")
    parser.add_argument("-x", "--extention", dest="extention",default = [],help="Add extentions at the end. Seperate them with comas \n example: -x php,html,txt")
    parser.add_argument("-to", "--timeout", dest="timeout",default = 5,help="Timeout")
    parser.add_argument("-ss", "--screenshot", dest="screenshot",nargs='?',default = "not_set",help="Takes screenshot of valid requests.\nDefault is 200,204,301,302,307")
    parser.add_argument("-s","--status-code",dest="status",default="200,204,301,302,307,403",help="Status codes to be checked\nDefault is 200,204,301,302,307")
    parser.add_argument("-o","--output", dest="output", default ="",help="Output file" )
    args = parser.parse_args()
    start = time.time()


    if len(sys.argv) < 2:
        parser.print_usage()
        sys.exit(0)

    fileName = args.wordlist
    URL = args.url
    threads = int(args.threads)
    recursive = args.recursive
    crawpy = CRAWPY(URL,fileName,threads)
    extention = args.extention
    timeout = args.timeout   
    screenshotCodes = args.screenshot
    output = args.output
    statusCodes = args.status

    if screenshotCodes is not "not_set":
        isScreenShotMode = True
        if screenshotCodes == None:
            screenshotCodes = [200,204,301,302,307]
        else:
            try:
                screenshotCodes = screenshot.split(",")
                screenshotCodes.remove("")
            except:
                pass
        crawpy.success("*","Screenshot mod is enabled for status codes : {0}".format(screenshotCodes))
    else:
        isScreenShotMode = False

    
    crawpy.statusCodes = [int(x) for x in statusCodes.split(",")]# i love python
    crawpy.info("Status codes: {0}".format(statusCodes))

    crawpy.timeOut = int(timeout) # --> that int caused me 1 hour
    crawpy.info("Timeout: {0}".format(crawpy.timeOut))
    
    # output info
    if output != "":
        import os
        crawpy.info("Output file is {0}".format(os.getcwd()+"/"+output))
    
    # extention section
    if len(extention)> 1:
        extention = extention.split(",")
        crawpy.info("Extentions: {0}".format(extention))
        crawpy.extentions = extention
        crawpy.load_file(crawpy.fileName)

    crawpy.info("Number of generated urls {0}".format(len(crawpy.targets)))
    
    # recursive info
    if recursive:
        crawpy.info("~~Recursive scan enabled~~~~ ")
        crawpy.success("~","Please select a smaller wordlist for better performance on this option!! ")

    # fuzzing section
    crawpy.fuzz()
    
    # recursive section
    if recursive:
        crawpy.crawl()
    crawpy.info(time.time()-start)
    
    # screenshot section
    if isScreenShotMode:
        if len(crawpy.foundUrls) < 1:
            crawpy.info("Not found any url , quiting")
            sys.exit(1)
        crawpy_ss = CRAWPY_SCREENSHOT("firefox")
        for url in crawpy.foundUrls:
            if str(url.status_code) in screenshotCodes:
                crawpy_ss.clip(url.url)
    # output section
    if output != "":
        with open(output,"w") as f:
            for resp in crawpy.foundUrls:
                f.write("[{}] {} \n".format(resp.status_code,resp.url))
            f.close()
