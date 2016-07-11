try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Collapse stacktrace for analysis',
    'author': 'Xiao Li',
    'author_email': 'lix@uber.com',
    'version': '0.1',
    'packages': ['stackcollapse'],
    'scripts': ['stackcollapse-py'],
    'name': 'stackcollapse'
}

setup(**config)
