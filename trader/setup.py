import sys
from setuptools import setup, find_packages

HERE = path.abspath(path.dirname(__file__))
__version__ = '1.0.0'

REQUIRES = [
    'certifi==2019.11.28',
    'chardet==3.0.4',
    'idna==2.8',
    'lxml==4.4.2',
    'multitasking==0.0.9',
    'numpy==1.18.0',
    'pandas==0.25.3',
    'python-dateutil==2.8.1',
    'pytz==2019.3',
    'PyYAML==5.2',
    'requests==2.22.0',
    'robin-stocks==0.9.9.5',
    'schedule==0.6.0',
    'simplejson==3.17.0',
    'six==1.13.0',
    'urllib3==1.25.7',
    'yfinance==0.1.54'
]

setup(
    name='Trader',
    author='Austin Fatt',
    author_email='afatt90@gmail.com',
    url='https://github.com/afatt/trading-app',
    version=__version__,
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 2.7'
    ],
    keywords='Trader',
    packages=find_packages(),
    install_requires=REQUIRES
)
