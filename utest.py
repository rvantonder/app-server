import unittest
import httplib
import urllib
import time

class TestSequenceFunctions(unittest.TestCase):

  def setUp(self):
    self.conn = httplib.HTTPConnection('127.0.0.1:3000')

  def tearDown(self):
    self.conn.close()

  def testCodeRequest(self):
    username = "0123456789"
    self.conn.request("GET", "/codeRequest?userid="+username)
    r1 = self.conn.getresponse()
    self.assertTrue(r1.status == 200) 

  def testBalanceRequest(self): 
    username = "9876543210"
    self.conn.request("GET", "/balanceRequest?userid="+username)
    r1 = self.conn.getresponse()
    self.assertTrue(r1.read() == "0") #balance should be 0 

  def testClaimCode(self):
    username = "1111111111"
    self.conn.request("GET", "/balanceRequest?userid="+username) #get the current balance
    r0  = self.conn.getresponse()
    bal = int(r0.read()) #save the balance

    self.conn.request("GET", "/codeRequest?userid="+username) #generate a code
    r1 = self.conn.getresponse()
    uc = r1.read()

    self.conn.request("GET", "/claimCode?userid="+username+"Q"+uc)
    r2 = self.conn.getresponse()
    self.assertTrue(r2.read() == "SUCCESS") #make sure you get a successful claim

    self.conn.request("GET", "/balanceRequest?userid="+username) #get the current balance
    r3  = self.conn.getresponse()
    modified_bal = int(r3.read()) #save the balance

    self.assertTrue(modified_bal == bal + 1)

  def testRedeemPoints(self):
    username = "2222222222" 
    self.givePoints(username, 10)

    self.conn.request("GET", "/balanceRequest?userid="+username) #get the current balance
    r  = self.conn.getresponse()
    bal = int(r.read())

    self.assertTrue(bal == 10) #added 10 points

    self.conn.request("GET", "/redeemPoints?userid="+username)
    response = self.conn.getresponse().read()
    self.assertTrue(response == "SUCCESS")

    self.conn.request("GET", "/balanceRequest?userid="+username)
    new_bal = int(self.conn.getresponse().read())
    self.assertTrue(new_bal == 1) #10 - 9

    self.conn.request("GET", "/redeemPoints?userid="+username) #trying to redeem again should fail
    response = self.conn.getresponse().read()
    self.assertTrue(response == "FAIL")


  def givePoints(self, u, n):
    for i in xrange(n):
      self.conn.request("GET", "/codeRequest?userid="+u)
      r1 = self.conn.getresponse()
      uc = r1.read()
      self.conn.request("GET", "/claimCode?userid="+u+"Q"+uc)
      self.conn.getresponse().read() #get rid of response

      






if __name__ == '__main__':
  unittest.main()
