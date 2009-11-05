from setuptools import setup, find_packages
import os

version = open(os.path.join("Products", "feedfeeder", "version.txt")).read()
version = version.strip()
readme = open(os.path.join("Products", "feedfeeder", "README.txt")).read()
history = open(os.path.join("Products", "feedfeeder", "HISTORY.txt")).read()

setup(name='Products.feedfeeder',
      version=version,
      description="Turn external feed entries into content items",
      long_description= readme + "\n" + history,
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='Zest Software',
      author_email='m.van.rees@zestsoftware.nl',
      url='http://plone.org/products/feedfeeder',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['Products'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'FeedParser',
          'BeautifulSoup',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
