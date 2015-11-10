from setuptools import setup, find_packages


with open('README.md') as f:
    README = f.read()


setup(name="tornado-measures",
      version="1.0.0",
      description=u"Simple Tornado HTTP Client that automatically sends http response metrics to Backstage measures",
      long_description=README,
      author="Globo.com",
      author_email="backstage1@corp.globo.com",
      url="http://github.com/globocom/tornado-measures",
      download_url='',
      license="MIT",
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Web Environment',
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Programming Language :: Python'
      ],
      packages=find_packages(
          exclude=(
              'tests',
          ),
      ),
      include_package_data=True,
      zip_safe=True,
      install_requires=['tornado', 'measures'],
      tests_require=["nose==1.2.1", "pep8==1.4.1", "mock==1.0.1"],
      )
