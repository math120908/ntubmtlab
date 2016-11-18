import urllib
import urllib2
import cookielib
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.badminton.data

def get_url_content(url):
   class NoExceptionCookieProcesser(urllib2.HTTPCookieProcessor):
         def http_error_500(self, req, fp, code, msg, hdrs): 
                 return fp
   try:
      req = urllib2.Request(url)
      cj = cookielib.CookieJar()
      opener = urllib2.build_opener(NoExceptionCookieProcesser(cj))
      response = opener.open(req, timeout=10)
      content = response.read().encode('UTF-8')
      response.close()
   except:
      content = u''
   return content


