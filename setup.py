from setuptools import setup, find_packages

setup(name='avalogger',
      version='0.1',
      description='The logging package we need for our projects.',
      url='',
      author='youtapy',
      author_email='mazaheri7amin@gmail.com',
      license='MIT',
      packages=find_packages(),
      include_package_data=True,
      package_data={
            'avalogger':['*.json'],
            },
      zip_safe=False)
