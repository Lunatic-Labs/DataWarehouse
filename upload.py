import pycurl
import certifi
import urllib
import urlparse
from io import BytesIO #for getFromHttps()

import pycurl
try:
    # python 3
    from urllib.parse import urlencode
except ImportError:
    # python 2
    from urllib import urlencode

#code from http://pycurl.io/docs/latest/quickstart.html, I'm learning what it all does -Justin T.
#below: Post a given file to a given url using pycurl - url format should be 'https://website.com/' (including single quotes)
def _postToHttps(url, filename):
    c = pycurl.Curl()
    c.setopt(c.URL, url)

    c.setopt(c.HTTPPOST, [
    ('fileupload', (
        c.FORM_BUFFER, filename,
        c.FORM_BUFFERPTR, 'insert description here',
    )),
    ])

    #{field : value} needs to be filled in. How?
    post_data = {'field': 'value'}
    # Form data must be provided already urlencoded. Function defined here: https://docs.python.org/2/library/urllib.html#urllib.urlencode 
    postfields = urlencode(post_data)
    # Sets request method to POST,
    # Content-Type header to application/x-www-form-urlencoded (the data type expected of string arguments)
    # and data to send in request body.
    c.setopt(c.POSTFIELDS, postfields)

    c.perform()
    c.close()

#below: Code from https://stackoverflow.com/questions/24572210/what-is-the-equivalent-to-curls-data-urlencode-in-pycurl

def _encodeData(url, queryString):
    your_dict = {urlparse.parse_qs(queryString)}
    res = urllib.request.urlopen(url), urllib.parse.urlencode(your_dict).encode()
    # Get the result
    return(res.read())

# urlparse.parse_qs() defined here: https://docs.python.org/2/library/urlparse.html#module-urlparse
# parse_qs() returns a dictionary made from the string argument (the query string)
# If we need the string as name & value data pairs we should use parse_qsl()

# Code from https://stackabuse.com/using-curl-in-python-with-pycurl/ - OPTION 1
# and http://pycurl.io/docs/latest/quickstart.html                   - OPTION 2
# below: pull from a given url, written in bytes - url format should be 'https://website.com/' (including single quotes)
def _getFromHttps(url, filename):
    c = pycurl.Curl()
    c.setopt(c.URL, url)

    # OPTION 1: Write bytes into the given file. File format should be 'file.txt' (including single quotes)
    c.setopt(c.WRITEDATA, filename)

    c.perform()
    c.close()

def _getFromHttps(url):
    c = pycurl.Curl()
    c.setopt(c.URL, url)

    # OPTION 2: Write bytes to a BytesIO object. Not sure how this is stored.
    buffer = BytesIO()
    c.setopt(c.WRITEFUNCTION, buffer.write)
    c.setopt(c.CAINFO, certifi.where()) #HTTPS Certificate

    c.perform()
    c.close()