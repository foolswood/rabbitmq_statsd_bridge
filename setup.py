from setuptools import setup

setup(
    name='rabbitmq_statsd_bridge',
    version='0.1a0',
    description='Populate statsd from rabbitmq',
    long_description='',
    # Get strings for classifiers from
    # http://pypi.python.org/pypi?%3Aaction=list_classifiers:
    classifiers=[],
    keywords='',
    author='David Honour',
    author_email='david@foolswood.co.uk',
    url='FIXME',
    license='GPL3',
    install_requires=['requests', 'statsd'])
