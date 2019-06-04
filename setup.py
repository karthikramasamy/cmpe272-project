import io

from setuptools import find_packages, setup

with io.open('README.rst', 'rt', encoding='utf8') as f:
    readme = f.read()

setup(
    name='airbnb',
    version='1.0.0',
    url='https://github.com/karthikramasamy/cmpe272-project/',
    license='BSD',
    maintainer='Karthik Ramasamy',
    description='The basic airbnb app built for the SJSU CMPE-272 Spring 2019 course.',
    long_description=readme,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
        'pymongo',
        'pyjwt',
        'authlib',  
        'six',
        'python-dotenv',
        'dnspython',
    ],
    extras_require={
        'test': [
            'mongomock',
            'pytest',
            'pytest-cov',
            'coverage',
        ],
    },
)
