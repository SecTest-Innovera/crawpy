from src.Handler import Handler

class Interact:
    def __init__(self,browserName):
        import sys
        from selenium import webdriver
        if browserName == "firefox":
            self.browser = webdriver.Firefox()
            self.browser.add_argument('headless')
        elif browserName == "chrome":
            self.browser = webdriver.Chrome()
            self.browser.add_argument('headless')

        else:
            Handler().error("Unknown browser error,\n Please choose chrome or firefox")
            sys.exit(1)
        self.directory = "screenshots/"
    
    def clip(self,url):
        self.browser.get(url)
        url = url.split("//")[1]
        url = url.replace("/","-").replace(".","-")
        self.browser.save_screenshot(self.directory + url + ".png")
        Handler().success("Screenshot saved : "+url+".png")
        return
