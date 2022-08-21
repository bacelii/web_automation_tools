#!/usr/bin/env python
# coding: utf-8

# # -- Helper Functions --

# In[1]:


from pathlib import Path


# In[2]:


def download_path():
    return Path.home() / "Downloads"

def files_in_folder(path,file_ext = ""):
    return [k for k in Path(path).iterdir() if k.is_file() 
                if file_ext in k.suffix]

def download_wait(
    directory, 
    timeout=100000, 
    nfiles=None,
    verbose = False,
    verbose_while_waiting = False,):
    """
    Wait for downloads to finish with a specified timeout.

    Args
    ----
    directory : str
        The path to the folder where the files will be downloaded.
    timeout : int
        How many seconds to wait until timing out.
    nfiles : int, defaults to None
        If provided, also wait for the expected number of files.

    """
    st = time.time()
    seconds = 0
    dl_wait = True
    while dl_wait and seconds < timeout:
        if verbose_while_waiting:
            print(f"Waiting for Download")
        time.sleep(1)
        dl_wait = False
        curr_files = files_in_folder(directory)
        if nfiles and len(curr_files) != nfiles:
            dl_wait = True

        for fname in curr_files:
            if str(fname.absolute()).endswith('.crdownload'):
                dl_wait = True

        seconds += 1
        
        
        
    if verbose:
        print(f"Total time for download wait = {time.time() - st}")
    return seconds


# # -- Data Retrieval Functions --

# In[3]:


import pandas as pd
import requests
from bs4 import BeautifulSoup


# In[4]:


#default_categories = ("Interstate","Other","Midstream")
default_categories = "Interstate"
default_base_url = "https://pipeline2.kindermorgan.com/LocationDataDownload/LocDataDwnld.aspx?code=ARLS"
default_category_class_name = "igdm_NautilusMenuItemHorizontalRootLink"


# In[5]:


def fetch_download_links(
    categories = None,
    base_url = None,
    category_class_name=None,
    query_deliminiter = "?",
    return_df = False,
    verbose = True,
    **kwargs
    ):
    """
    Purpose: Retrieve the URLS for data to be downloaded along with the names and categories.
    
    Implementation: beautifulsoup web scraping
    """
    
    if categories is None:
        categories = default_categories
        
    if type(categories) == str:
        categories = [categories]
        
    if base_url is None:
        base_url = default_base_url
        
    if category_class_name is None:
        category_class_name=default_category_class_name
        
    
    
    # -- downloads the html of the base page--
    download_base = base_url[:base_url.find(query_deliminiter)]
    page = requests.get(base_url)
    soup = BeautifulSoup(page.content,"html.parser")

    # -- finds all the data categories on base page
    categories_total = soup.find_all(class_=category_class_name)

    link_dicts = []
    for cat in categories_total:
        
            
        cat_name = cat.span.text
        
        if cat_name not in categories:
            continue

        a_links = cat.next_sibling.find_all("a")

        local_dicts = [dict(
            download_link = f'{download_base}?{a["href"][a["href"].find(query_deliminiter)+1:].replace("TSP=","code=")}',
            name = a.span.text,
            category = cat_name) for a in a_links]

        if verbose:
            print(f"# of links in {cat_name} = {len(local_dicts)}")

        link_dicts += local_dicts

    if return_df:
        return pd.DataFrame.from_records(link_dicts)
    else:
        return link_dicts
    


# In[6]:


import selenium
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from pathlib import Path
import time


# In[7]:


default_driver_exe_path = str((download_path() / Path("chromedriver_win32/chromedriver.exe")).absolute())
default_retrieve_button_id = "WebSplitter1_tmpl1_ContentPlaceHolder1_HeaderBTN1_btnRetrieve"
default_download_button_id = "WebSplitter1_tmpl1_ContentPlaceHolder1_HeaderBTN1_btnDownload"
default_visible_browser = True
default_append_source = True
default_retrieve_sleep_seconds = 2


# In[8]:


Path("./").exists()


# In[9]:


def download_data(
    data_to_download,
    driver_exe_path = None,
    retrieve_button_id = None,
    download_button_id = None,
    visible_browser = None,
    append_source = None,
    retrieve_sleep_seconds = None,
    ignore_empty_download = True,
    debug = False,
    verbose = True,
    **kwargs
    ):
    """
    Purpose: To go and fetch the data from the
    download links and to export as a csv file
    """
    
    if driver_exe_path is None:
        driver_exe_path = default_driver_exe_path
        
    if retrieve_button_id is None:
        retrieve_button_id = default_retrieve_button_id
        
    if download_button_id is None:
        download_button_id = default_download_button_id
        
    if visible_browser is None:
        visible_browser = default_visible_browser
        
    if append_source is None:
        append_source = default_append_source
        
    if retrieve_sleep_seconds is None:
        retrieve_sleep_seconds = default_retrieve_sleep_seconds
        
    
    #1) Creates the Chrome browser
    if not visible_browser:
        options = Options()
        options.add_argument("--headless")
        assert options.headless
    else:
        options = None
        
    
    if not Path(driver_exe_path).exists():
        guess_path = Path(f"{driver_exe_path}")
        if '.exe' not in driver_exe_path:
            guess_path = guess_path / Path("chromedriver.exe")
        driver_exe_path = str((download_path() / guess_path).absolute())
        if verbose:
            print(f"Inferred path to driver = {driver_exe_path}")
    
    curr_path = str(Path(driver_exe_path).absolute())
    if debug:
        print(f"Path to Chrome driver = {curr_path}")

    driver = Chrome(curr_path,options = options)
    
    #2) The data retrieval loop
    """
    Purpose: Given a link where data can be found: 
    1) Go to webpage
    2) click the retrieve button
    3) click the download button
    4) wait for the download
    5) Load the file as a dataframe and delete from downloads
    """
    
    if isinstance(data_to_download,pd.DataFrame,):
        data_to_download = data_to_download.to_dict(orient='records')
        
    all_link_dfs = []
    for data_dict in data_to_download:
        data_link = data_dict["download_link"]

        if verbose:
            print(f"\n-- Working on downloading {data_dict['category']}:{data_dict['name']} from \n {data_dict['download_link']}")

        driver.get(data_link)

        elem = driver.find_element(By.ID,retrieve_button_id)
        elem.click()

        time.sleep(retrieve_sleep_seconds)

        downloads = download_path()
        download_files = files_in_folder(downloads)

        if debug:
            print(f"# of download files before download = {len(download_files)}")

        elem = driver.find_element(By.ID,download_button_id)
        elem.click()

        download_wait(
            downloads,
            nfiles = len(download_files) + 1,
            verbose = False,
            verbose_while_waiting = False)

        if debug:
            print(f"# of download files after download = {len(download_files)}")

        download_files_after = files_in_folder(downloads)
        file = list(set(download_files_after).difference(download_files))[0]

        try:
            df = pd.read_csv(file)
        except:
            df = pd.read_excel(file)

        if not ignore_empty_download and len(df) == 0:
            raise Exception(f"The following data fetch had 0 entries: \n{data_dict}")

        if append_source:
            for k,v in data_dict.items():
                df[k] = v

        file.unlink()
        all_link_dfs.append(df)

    all_link_dfs = pd.concat(all_link_dfs)
    
    return all_link_dfs


# In[10]:


default_export_filepath = "./download_data"

def export_data_df_to_csv(
    data_df,
    export_filepath=None,
    verbose = True,
    **kwargs
    ):
    
    if export_filepath is None:
        export_filepath = default_export_filepath
        
    export_path = Path(export_filepath)
    export_path = export_path.parent / Path(f"{export_path.stem}.csv")
    data_df.to_csv(str(export_path.absolute()))
    
    if verbose:
        print(f"Exportted to {export_path}")
    return 
    


# In[11]:


def data_fetch_pipeline(**kwargs):
    data_links = fetch_download_links(**kwargs)
    data_df = download_data(data_links,**kwargs)
    export_data_df_to_csv(data_df,**kwargs)


# In[12]:


import argparse

def parse_arguments():
    parser = argparse.ArgumentParser()
    
    #-- arguemtns for output
    parser.add_argument("-f","--export_filepath",default=None,
                        help="csv filepath for the output of data",
                       dest = "export_filepath")
    # -- arguments for downloading --
    parser.add_argument("-d","--driver_exe_path",default=default_driver_exe_path,
                        help="path to where stored chrome driver exe",
                       dest = "driver_exe_path")
    parser.add_argument("-ret","--retrieve_button_id",default=default_retrieve_button_id,help="the id of the retrieve button in the html source",
                       dest = "retrieve_button_id")
    parser.add_argument("-down","--download_button_id",default = default_download_button_id,help="the id of the download button in the html source",
                       dest = "download_button_id")
    parser.add_argument("-v","--visible_browser",default = default_visible_browser,
                        help="whether a browser window should pop up and perform the scripted actions. Set to False for headerless",
                       dest = "visible_browser")
    parser.add_argument("-a","--append_source",default=default_append_source,
                       help="whether the url and the pipeline name should be appended to the entries to show where entry was fetched from",
                       dest = "append_source")
    parser.add_argument("-s","--retrieve_sleep_seconds",default = default_retrieve_sleep_seconds,
                       help="how long the program will sleep after activating the retrieve button (to help if takes long time to buffer)",
                       dest = "retrieve_sleep_seconds")
    
    # -- arguments for fetch_download_links --
    parser.add_argument("-b","--base_url",default = default_base_url,
                        help = "what webpage to start from",
                       dest = "base_url")
    parser.add_argument("-cat_n","--category_class_name",default = default_category_class_name,
                        help = "the class name from the html source to which signal which tags to search for in finding categories",
                       dest = "category_class_name")
    parser.add_argument("-cat","--categories",default=default_categories,
                        help=("the pipelines to pull data from (listed in the dropdown tabs of webpage). "
                        "Currently only supports one pipeline input specified with str"),
                        type = str,
                        nargs='+',
                       dest = "categories")
    
    
    # to run in ipynb
    #args = parser.parse_args("-f download.csv -d chromedriver_win32".split())
    
    # to run as script
    args = parser.parse_args()

    
    return args
    
    


# In[13]:


def main():
    arguments = parse_arguments()
    print(f"arguments = {arguments}")
    kwargs = vars(arguments)
    data_fetch_pipeline(**kwargs)
    


# In[14]:


if __name__ == '__main__':
    main()


# In[ ]:




