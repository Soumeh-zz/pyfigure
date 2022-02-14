from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as file:
    long_description = file.read()

setup(

    name = 'pyfigure',
    version = '1.0.0',
    description = "Generate configuration files for classes.",
    url = 'http://github.com/Soumeh/pyfigure',
    author = "Soumeh",
    license = 'MIT',
    install_requires = [
        'tomlkit',
    ],
    zip_safe = False,
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    project_urls = {
        "Bug Tracker": 'https://github.com/Soumeh/pyfigure/issues',
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir = {'': 'src'},
    packages = find_packages(where='src'),
    python_requires = '>=3.6',

)