import os
import unittest
from first_blog import blog
import tempfile

class TestCase(unittest.TestCase):
	def setUp(self):
		self.db_fd, blog.app.config['DATABASE'] = tempfile.mkstemp()
		self.app = blog.app.test_client()
		with blog.app.app_context():
			blog.init_db()

	def tearDown(self):
		os.close(self.db_fd)
		os.unlink(blog.app.config['DATABASE'])

	def test_empty_db(self):
		rv = self.app.get('/')
		# print(rv.data)
		assert b'sam' in rv.data
			
	def login(self, u, p):
		return self.app.post('/login', data=dict(username=u, password=p
		), follow_redirects=True)	

	def logout(self):
		return self.app.get('/logout', follow_redirects=True)

	def test_login(self):
		rv = self.login('admin', 'admin')
		# print(type(rv.data))
		# print(rv.data.decode())
		assert 'i am login' in rv.data.decode('utf-8')
	
		rv = self.login('admin', 'x')
		assert 'invalid password' in rv.data.decode()

		rv = self.login('ad', 'admin')
		assert 'invalid username' in rv.data.decode()

	def test_logout(self):
		rv = self.logout()
		assert 'logged out' in rv.data.decode('utf-8')


if __name__ == '__main__':
	unittest.main()
