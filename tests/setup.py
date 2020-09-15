from setuptools import setup

setup(
    name='kraken_schema',
    version='0.1',
    description='kraken schema module',
    author='Tactik8',
    author_email='admin@tactik8.com',
    packages=['kraken_schema'],  #same as name
    install_requires=['requests'], #external packages as dependencies
)
