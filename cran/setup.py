from setuptools import setup, find_packages

print(find_packages())

setup(
    name='cran-server',
    version='0.1dev',
    #packages=['cran_server', 'cran_server.tasks'],
    packages=find_packages(),
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README.md').read(),
    scripts=['cran-server.py']
)
