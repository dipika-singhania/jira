import urllib2
import base64

def getAPIResponse(url,data):
    username = 'dipika.singhania'
    password = 'gale@123!'
    auth = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
    request = urllib2.Request(url, data, {
        'Authorization': 'Basic %s' % auth,
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    })
    return urllib2.urlopen(request).read()
