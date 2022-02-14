from setuptools import setup

setup(

    name = 'pyfigure',
    version = '1.0.0',
    description = 'Generate configuration files for classes.',
    url = 'http://github.com/Soumeh/pyfigure',
    license = 'MIT',
    packages = ['pyfigure'],
    install_requires=[
        'tomlkit',
    ],
    zip_safe = False

)