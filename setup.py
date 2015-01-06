from distutils.core import setup	

setup(name='Distutils',
      version='0.3',
      description='Python tools for Arma',
      author='sux',
      author_email='iamthesux@gmail.com',
	  packages=['p4a', 'p4a.formats', 'p4a.formats.rap'],
	  package_dir={'p4a': 'src/p4a'},
     )