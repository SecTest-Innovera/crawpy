# Crawpy

Simple content discovery tool with some cool features. <br/>

### Basic Discovery
[![asciicast](https://asciinema.org/a/297821.svg)](https://asciinema.org/a/297821)

### Recursive Discovery
[![asciicast](https://asciinema.org/a/297820.svg)](https://asciinema.org/a/297820?speed=10)


# Installation
```
git clone https://github.com/morph3/crawpy
pip install -r requirements.txt
or
python3 -m pip install -r requirements.txt
```

# Usage 
```
usage: crawpy.py [-h] [-u URL] [-w WORDLIST] [-t THREADS] [-r] [-x EXTENSION]
                 [-to TIMEOUT] [-ss [SCREENSHOT]] [-s STATUS] [-o OUTPUT]
                 [-X HTTP_METHOD]

optional arguments:
  -h, --help            show this help message and exit
  -u URL, --url URL     URL
  -w WORDLIST, --wordlist WORDLIST
                        Wordlist
  -t THREADS, --threads THREADS
                        Number of threads
  -r, --recursive       Recursive scan
  -x EXTENSION, --extension EXTENSION
                        Add extensions at the end. Seperate them with comas
                        example: -x php,html,txt
  -to TIMEOUT, --timeout TIMEOUT
                        Timeout
  -ss [SCREENSHOT], --screenshot [SCREENSHOT]
                        Takes screenshot of valid requests. Default is
                        200,204,301,302,307,401,403
  -s STATUS, --status-code STATUS
                        Status codes to be checked Default is
                        200,204,301,302,307,401,403
  -o OUTPUT, --output OUTPUT
                        Output file
  -X HTTP_METHOD, --http-method HTTP_METHOD
                        Http request type
```

# Examples

```
python3 crawpy.py -u https://morph3sec.com -w /opt/SecLists/Discovery/Web-Content/common.txt
python3 crawpy.py -u https://morph3sec.com -w /opt/SecLists/Discovery/Web-Content/common.txt -r -t 50
python3 crawpy.py -u https://morph3sec.com -w /opt/SecLists/Discovery/Web-Content/common.txt -r -t 50 -x php -ss 200,301 
python3 crawpy.py -u https://morph3sec.com -w /opt/SecLists/Discovery/Web-Content/common.txt -r -t 50 -x php -ss 200,301,401 -s 200,301,401,403
```



