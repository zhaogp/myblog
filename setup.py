from setuptools import setup, find_packages

setup(
	name='firstblog',
	version='0.2.1',
	packages=find_packages(),
	include_package_data=True,
	install_requires=['flask', 'click'],
	entry_points='''
		[console_scripts]
		initdb=first_blog.blog:initdb_command
		run=first_blog.blog:run_command
	''',
)
