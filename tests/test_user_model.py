import unittest
from app.models import User

class UserModelTestCase(unittest.TestCase):
	def test_password_setter(self):
		u = User(password='guess')
		self.assertTrue(u.password_hash is not None)

	def test_no_password_getter(self):
		u = User(password='guess')
		with self.assertRaises(AttributeError):
			u.password

	def test_password_verification(self):
		u = User(password='guess')
		self.assertTrue(u.verify_password('guess'))
		self.assertFalse(u.verify_password('box'))

	def test_password_salts_are_random(self):
		u = User(password='guess')
		u2 = User(password='guess')
		self.assertTrue(u.password_hash != u2.password_hash)
		

if __name__ == '__main__':
	unittest.main()
