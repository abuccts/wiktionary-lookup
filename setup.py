import setuptools
import os

HERE = os.path.dirname(__file__)

setuptools.setup(
    name='pywikitionary',
    version="0.1.0",
    author='Abuccts',
    author_email='abuccts@gmail.com',
    description='',
    license='GPLv3',
    keywords='',
    url='',
    packages=['pywiktionary'],
    long_description='See https://github.com/abuccts/wiktionary-lookup',
    entry_points={
        'console_scripts': ['wiktionary=pywiktionary.wiktionary:cli']
    },
    classifiers=[
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)"
    ],
    test_suite='nose.collector',
    install_requires=[]
)
