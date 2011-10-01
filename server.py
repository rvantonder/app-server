"""
The most basic (working) CherryPy application possible.
"""

import time
# Import CherryPy global namespace
import cherrypy
import random

#time, so that its unique
#phone number, just cuz
#random shift cuz want things to be sufficiently mixed up

class Server:
    """ Sample request handler class. """

    def __init__(self):
      self.db = {}
      self.balances = {}

    def index(self):
        return "Test"

    # Expose the index method through the web. CherryPy will never
    # publish methods that don't have the exposed attribute set to True.
    index.exposed = True

    def codeRequest(self, userid=None):
      if not userid in self.db.keys():
        self.db[userid] = []
        
      r =  int(random.random()*20)
      ls = int(userid) << r
      rs = int(userid) >> 32-r
      uc = int(time.time()) ^ int(hash(ls ^ rs))
      suc = str(uc) if uc > 0 else str(uc*-1)
      self.db[userid].append(suc)
      print 'current db',self.db
      return suc 

    codeRequest.exposed = True

    def balanceRequest(self, userid=None):
      """
      returns 0 if the user does not exist, or the value otherwise
      """

      if not userid in self.balances.keys():
        self.balances[userid] = 0
        return str(0)
      else:
        return str(self.balances[userid])

    balanceRequest.exposed = True

    def claimCode(self, userid=None): #number seperated by '#'
      try:
        num, code = userid.split('Q')
      except:
        print 'no split'
        return "FAIL"

      if not num in self.db.keys():
        self.db[num] = []

      if not num in self.balances.keys():
        self.balances[num] = 0

      if code in self.db[num]:
        self.db[num].remove(code) #remove the code
        self.balances[num] += 1
        return "SUCCESS"
      else:
        return "FAIL"
    
    claimCode.exposed = True  

    def redeemPoints(self, userid=None): #redeemPoints only called from Admin interface, with user phone. No authentication with cashiers number
      if self.balances[userid] - 9 >= 0:
        self.balances[userid] = self.balances[userid] - 9#decrement
        return "SUCCESS"
      else:
        return "FAIL"

    redeemPoints.exposed = True


import os.path
appconf = os.path.join(os.path.dirname(__file__), 'app.conf')

if __name__ == '__main__':
    # CherryPy always starts with app.root when trying to map request URIs
    # to objects, so we need to mount a request handler root. A request
    # to '/' will be mapped to HelloWorld().index().
    cherrypy.quickstart(Server(), config=appconf)
else:
    # This branch is for the test suite; you can ignore it.
    cherrypy.tree.mount(Server(), config=appconf)
