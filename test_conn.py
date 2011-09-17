import httplib
import urllib

if __name__ == '__main__':
  username = "0123456789"
  conn = httplib.HTTPConnection('127.0.0.1:8080')
  conn.request("GET", "/doLogin?userid="+username)
  r1 = conn.getresponse()
  print r1.status, r1.reason
  data1 = r1.read()
  print data1
  conn.close()
