import os
import multiprocessing

from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='raspberry-pi-sensor-rest',
    version='0.10',
    url='http://github.com/coddingtonbear/raspberry-pi-sensor-rest/',
    description='Expose Raspberry PI sensors via a REST interface.',
    author='Adam Coddington',
    author_email='me@adamcoddington.net',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities',
    ],
    install_requires=required,
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'rpi-sensor-rest = rpi_sensor_rest.cmdline:main'
        ]
    },
)
