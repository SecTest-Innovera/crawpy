import time
import termios
import sys
import argparse
from src.RequestEngine import Requester
from src.Banner import Banner
from src.Interact import Interact
import os


#python3 crawpy.py -u https://morph3sec.com -w /opt/SecLists/Discovery/Web-Content/common.txt -x html -r

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", dest="url",help="URL")
    parser.add_argument("-w", "--wordlist", dest="wordlist", help="Wordlist")
    parser.add_argument("-t", "--threads", dest="threads", help="Number of threads",default=30)
    parser.add_argument("-r", "--recursive", dest="recursive",action='store_true',help="Recursive scan")
    parser.add_argument("-x", "--extension", dest="extension",default = [],help="Add extensions at the end. Seperate them with comas \n example: -x php,html,txt")
    parser.add_argument("-to", "--timeout", dest="timeout",default = 5,help="Timeout")
    parser.add_argument("-ss", "--screenshot", dest="screenshot",nargs='?',default = "not_set",help="Takes screenshot of valid requests.\nDefault is 200,204,301,302,307")
    parser.add_argument("-s","--status-code",dest="status",default="200,204,301,302,307,401,403",help="Status codes to be checked\nDefault is 200,204,301,302,307,401,403")
    parser.add_argument("-o","--output", dest="output", default ="",help="Output file" )
    parser.add_argument("-X","--http-method", dest="http_method", default ="HEAD",help="Http request type")
    
    args = parser.parse_args()

    if len(sys.argv) < 2:
        parser.print_usage()
        sys.exit(0)

    f_name = args.wordlist
    n_threads = int(args.threads)
    is_recursive = args.recursive
    exts = args.extension
    timeout = args.timeout   
    screenshot_codes = args.screenshot
    output = args.output
    status_codes = args.status
    http_method = args.http_method
    Banner().greet()

    # initialize
    he = Requester(args.url)
    he.load_targets(f_name)
    he.http_method = http_method
    he.n_threads = n_threads
    he.handler.status_codes = [int(x) for x in status_codes.split(",")]
    he.timeout = int(timeout)



    # extension
    if len(exts)> 0:
        exts = exts.split(",")
        he.exts = exts
        he.update_extensions(he.exts)
        he.target_len = len(he.targets)


    # screenshot 
    if screenshot_codes is not "not_set":
        ss_mode = True
        if screenshot_codes == None:
            screenshot_codes = [200,204,301,302,307]
        else:
            try:
                screenshot_codes = screenshot.split(",")
                screenshot_codes.remove("")
            except:
                pass
    else:
        ss_mode = False

    #info section
    he.handler.binfo("Url: {}".format(he.url))
    he.handler.binfo("Wordlist: {}".format(he.f_name))
    he.handler.binfo("Threads: {}".format(he.n_threads))
    if ss_mode:
        he.handler.bsuccess("*","Screenshot mod is enabled for status codes : {}".format(screenshot_codes))
    he.handler.binfo("HTTP Method: {}".format(he.http_method))
    he.handler.binfo("Status Codes: {}".format(status_codes))


    os.system("stty -echo")
    he.fuzz()
    os.system("stty echo")
    termios.tcflush(sys.stdin, termios.TCIFLUSH)
    
    # recursive section
    if is_recursive:
        he.handler.info("Recursive scan enabled")
        os.system("stty -echo")
        he.crawl()
        os.system("stty echo")
        termios.tcflush(sys.stdin, termios.TCIFLUSH)


    # screenshot section
    if ss_mode:
        if len(he.handler.found_resps) < 1:
            he.handler.info("Not found any url , quiting")
            sys.exit(1)
        crawpy_ss = Interact("firefox")
        for url in he.handler.found_resps:
            if str(url.status_code) in screenshot_codes:
                crawpy_ss.clip(url.url)

    # output section
    if output != "":
        import os
        he.handler.info("Output file is {}".format(os.getcwd()+"/"+output))
        with open(output,"w") as f:
            for resp in he.handler.found_resps:
                f.write("[{}] {} \n".format(resp.status_code,resp.url))
            f.close()
