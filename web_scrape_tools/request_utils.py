"""
Uitls for going and retrieing webpage raw
data from a URL

Package that helps with getting information from dynamic websites: 
- https://github.com/psf/requests-html
"""

import requests

status_codes = """
Informational responses (100–199)
Successful responses (200–299)
Redirection messages (300–399)
Client error responses (400–499)
Server error responses (500–599)
"""

def example_retrieve_html(url=None,verbose = True):
    if url is None:
        url = "https://realpython.github.io/fake-jobs/"
        
    page = requests.get(url)
    
    if verbose:
        print(f"Status code = {page.status_code}")
        print(page.text)
    return page

def print_status_code_cheat_sheet():
    print(status_codes)
    
def status_code(page):
    return page.status_code


import request_utils as rqu