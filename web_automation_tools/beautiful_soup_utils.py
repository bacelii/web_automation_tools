from bs4 import BeautifulSoup
import requests

"""
Notes:
a) .text field of bs4 object will eliminate the html surrounding it

"""
navigating_dom_tree_tips = """
Can use . operator with element tags: soup.body.b (this will only give the first tag of that type)
.children : iterable of children
.descendants: gives all descendents recursivel (children, children's children...)
.parent : gives surrounding tag
.next_sibling .previous_sibling: getting the neighbors
.next_siblings .previous_siblings: iterable over all siblings
  --> note: sometimes as \n can be a next sibling if it separates siblings

"""
def print_navigating_dom_tree_tips():
    print(navigating_dom_tree_tips)
    
searching_dom_tree_tips = """
Source: https://www.crummy.com/software/BeautifulSoup/bs4/doc/#kinds-of-filters
find_all options for search (looks through all descendants):

1st argument
- string: exact match
- list of strings
- function over text that returns true or false
- regular expresion:
    import re
    soup.find_all(re.compile("^b")
    
other kwargs:
- id = 
- href = 
- _class = 
- name
- attrs = {some dictionary of attributes}
    ex: attrs = {'name':'email'}
- limit = 1
    
    
find method: like the find_all method with a limit == 1
-> if can't find anything then returns None

"""
def print_searching_dom_tree_tips():
    print(searching_dom_tree_tips)

def pretty_print(results):
    """
    Print the results
    """
    print(results.prettify())

def example_page():
    url = "https://realpython.github.io/fake-jobs/"
    page = requests.get(url)
    return page

def example_soup_obj():
    soup = BeautifulSoup(example_page().content,"html.parser") 
    return soup

def example_find_element_by_id(
    page=None,
    id="ResultsContainer",
    verbose = False):
    
    if page is None:
        page = example_page()
    #pass it page.content because if did page.text would have character encoding issus
    soup = BeautifulSoup(page.content,"html.parser") 
    
    results = soup.find(id=id)
    
    if verbose:
        print(results.prettify())
        
    return results

example_results = example_find_element_by_id

def example_print_job_results(job_results):
    for idx,j in enumerate(job_results):
        print(f"--- Working on job {idx}---")
        title_element = j.find("h2",class_="title")
        company_element = j.find(f"h3",class_="company")
        location_element = j.find("p",class_="location")

        for k in [title_element,company_element,location_element]:
            print(k.text.strip()) # stripping gets rid of the extra white space
def example_find_all_elements_by_class(page=None,class_="card-content"):
    results = bsu.example_find_element_by_id(page=page,verbose = False)
    
    job_results = results.find_all("div",class_ = "card-content")
    example_print_job_results(job_results)
    
            
def example_find_all_with_filter_on_text():
    results = bsu.example_results()
    
    # will try and do exact search
    print(results.find_all("h2",string="Python"))
    
    python_jobs = results.find_all("h2", string = lambda text: "python" in text.lower())
    return python_jobs

# ------- can get an element returned by bs4 and navigate up the DOM tree to parents
def example_navigating_dom_tree():
    """
    The parent <div> element we want is 3 steps up so 
    have to call the parent 3 time and then can print out all we want on the job
    """
    python_jobs = example_find_all_with_filter_on_text()

    # -- need to go all the way up to the parent in order to print out all relavant info
    python_jobs = [k.parent.parent.parent for k in python_jobs]
    example_print_job_results(python_jobs)
    

def example_extracting_attribute_from_inside_tag():
    """
    Extracts the href attribute
    """
    soup = bsu.example_soup_obj()
    link_results = soup.find_all("a")
    url_links = [r["href"] for r in link_results]
    return url_links

import beautiful_soup_utils as bsu