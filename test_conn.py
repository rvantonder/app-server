import httplib
import urllib
from string import *

if __name__ == '__main__':
  username = "0123456789"
  conn = httplib.HTTPConnection('127.0.0.1:3000')
  conn.request("GET", "/codeRequest?userid="+username)
  r1 = conn.getresponse()
  if r1.status == 404:
    print "404"
  else:
    print r1.status, r1.reason
    data1 = r1.read()
    print data1

  conn.close()
