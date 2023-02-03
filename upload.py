import pycurl
import certifi
import urllib

import pycurl
try:
    # python 3
    from urllib.parse import urlencode
except ImportError:
    # python 2
    from urllib import urlencode

#code from http://pycurl.io/docs/latest/quickstart.html, I'm learning what it all does -Justin T.
#post a given file to a given url using pycurl
def _postToHttps(url, filename):
    c = pycurl.Curl()
    c.setopt(c.URL, url)

    c.setopt(c.HTTPPOST, [
    ('fileupload', (
        c.FORM_BUFFER, filename,
        c.FORM_BUFFERPTR, 'insert description here',
    )),
    ])

    #{field : value} needs to be filled in
    post_data = {'field': 'value'}
    # Form data must be provided already urlencoded. NEED TO DEFINE? IS FUNCTION DEFINED?
    postfields = urlencode(post_data)
    # Sets request method to POST,
    # Content-Type header to application/x-www-form-urlencoded
    # and data to send in request body.
    c.setopt(c.POSTFIELDS, postfields)

    c.perform()
    c.close()

#code from https://stackoverflow.com/questions/24572210/what-is-the-equivalent-to-curls-data-urlencode-in-pycurl
#Figuring out what each part does, but may need to call this before post_data in above function.
def _encodeData(url)
    your_dict = {"a": "a", "b": "b"}
    res = urllib.request.urlopen(url), urllib.parse.urlencode(your_dict).encode())
    # Get the result
    return(res.read())
