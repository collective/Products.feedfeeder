from setuptools import setup, find_packages

readme = open("README.rst").read().strip()
history = open("CHANGES.rst").read().strip()

setup(
    name='Products.feedfeeder',
    version='3.0.1',
    description="Turn external feed entries into content items",
    long_description=readme + "\n\n" + history,
    # Get more strings from
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Framework :: Plone",
        "Framework :: Plone :: 4.3",
        "Framework :: Plone :: 5.0",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
    keywords='feed rss atom',
    author='Zest Software',
    author_email='m.van.rees@zestsoftware.nl',
    url='https://github.com/collective/Products.feedfeeder',
    license='GPL',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['Products'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'feedparser',
        'beautifulsoup4',
    ],
    extras_require={
        'test': [
            'Products.PloneTestCase',
        ],
    },
    entry_points="""
    # -*- Entry points: -*-
    [z3c.autoinclude.plugin]
    target = plone
    """,
    )
