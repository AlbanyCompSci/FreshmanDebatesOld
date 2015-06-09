from smt.Z3 import *
import unittest
from AuthConfidentiality import Authentication, Principal
import JeevesLib

class TestAuthConfidentiality(unittest.TestCase):
  def setUp(self):
    JeevesLib.init()
    self.alicePwd = "alicePwd"
    self.bobPwd = "bobPwd"
    self.aliceUser = Principal.User(1, "Alice", self.alicePwd)
    self.bobUser = Principal.User(2, "Bob", self.bobPwd)

  def testUserCanSeeOwnPassword(self):  
    alicePwdToAlice = JeevesLib.concretize(
        self.aliceUser, self.aliceUser.pwd)
    self.assertEqual(alicePwdToAlice, self.alicePwd)

  def testUserCannotSeeOtherPassword(self):
    bobPwdToAlice = JeevesLib.concretize(
        self.aliceUser, self.bobUser.pwd)
    self.assertEqual(bobPwdToAlice, "")

  def testLogin(self):
    self.assertEqual( JeevesLib.concretize(self.aliceUser
                        , Authentication.login(self.aliceUser, self.alicePwd))
                    , self.aliceUser)
    self.assertEqual( JeevesLib.concretize(self.aliceUser
                        , Authentication.login(self.aliceUser, "otherPwd"))
                      , Principal.NullUser())

  def testSensitiveUserPassword(self):
    # Make a sensitive user that is either Alice or Bob. Make sure it shows the
    # the right password based on the access level of the user.
    pass

if __name__ == '__main__':
    unittest.main()
