from setuptools import setup, find_packages

setup(
   name='web_automation_tools', # the name of the package, which can be different than the folder when using pip instal
   version='1.0',
   description='Usefule Module for Web Scraping and Automation',
   author='Brendan Celii',
   author_email='bac8@rice.edu',
   packages=find_packages(),  #teslls what packages to be included for the install
   install_requires=[
       'pathlib', 
       'beautifulsoup4', 
       'selenium<4.3',
       'pandas',
       'requests',
       'argparse',
   ], #external packages as dependencies
    
    # if wanted to install with the extra requirements use pip install -e ".[interactive]"
    extras_require={
        #'interactive': ['matplotlib>=2.2.0', 'jupyter'],
    },
    
    # if have a python script that wants to be run from the command line
    entry_points={
        'console_scripts': ['pipeline_download=Applications.Eleox_Data_Fetch.Eleox_Data_Fetcher_vp1:main']
    },
    scripts=[], 
    
)
