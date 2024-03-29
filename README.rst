
web_automation_tools
#########
tools for helping with web scrapping and web automation using tools like BeautifulSoup and Selenium


Downloading the Chrome Driver For Web Automation
#################
In order for the Selenium package to work with Chrome to enable web interaction the 
chrome driver needs to be downloaded and extracted and placed in a known location for the 
script to use (placing in Downloads folder is assumed otherwise the path needs to be specifiied)

Process:

1) Open Chrome Browser and click 3 dots in top right corner > Help > About Google Chrome (this will show what version of chrome you have and if version is up to date)

2) Go to the following website and download the driver for your current chrome version (do the latest stable version, currrently ChromeDriver 104.0.5112.79 at the top of the page)
    download: https://sites.google.com/chromium.org/driver/
    
3) Extract the files form the zip folder and Place in Downloads folder (or other known location)

Installation
############
To install using git applicatio (better if code updates pushed). From the command line (cmd), navigate to a folder where you want the code stored and type into command line the following:

::

    git clone https://github.com/bacelii/web_automation_tools.git
    cd web_automation_tools
    pip install -e .

    
to install without git application

1) Navigate to https://github.com/bacelii/web_automation_tools.git
2) Click on top right green button "Code" > Download Zip
3) Rename the zip file web_automation_tools and extract files where you want the code stored
4) in command line navigate to the inner web_automation_tools folder and type

::

	cd web_automation_tools
    	pip install -e .


Running
############
The pipeline application can be used in different ways and can be located in web_automation_tools/Applications/Eleox_Data_Fetch/Eleox_Data_Fetcher_vp1.py 

1) Used as command line python program 
::
    
    ...navigate to web_automation_tools/Applications/Eleox_Data_Fetch/
    python Eleox_Data_Fetcher_vp1.py [...command line arguments]
    
    
2) Accessed through the command in the command line
::

    pipeline_download [...command line arguments]


3) the data_fetch_pipeline() function and all helper functions copied into another repo/code and arguments sent through function
::

    data_fetch_pipeline(**kwargs)


Arguments
############

::

	usage: ipykernel_launcher.py [-h] [-f EXPORT_FILEPATH] [-d DRIVER_EXE_PATH]
	                             [-ret RETRIEVE_BUTTON_ID]
	                             [-down DOWNLOAD_BUTTON_ID] [-v VISIBLE_BROWSER]
	                             [-a APPEND_SOURCE] [-s RETRIEVE_SLEEP_SECONDS]
	                             [-b BASE_URL] [-cat_n CATEGORY_CLASS_NAME]
	                             [-cat CATEGORIES [CATEGORIES ...]]

	optional arguments:
	  -h, --help            show this help message and exit
	  -f EXPORT_FILEPATH, --export_filepath EXPORT_FILEPATH
	                        csv filepath for the output of data (default: download.csv)
	  -d DRIVER_EXE_PATH, --driver_exe_path DRIVER_EXE_PATH
	                        path to where stored chrome driver exe (default: C:\Us
	                        ers\celii\Downloads\chromedriver_win32\chromedriver.ex
	                        e)
	  -ret RETRIEVE_BUTTON_ID, --retrieve_button_id RETRIEVE_BUTTON_ID
	                        the id of the retrieve button in the html source
	                        (default: WebSplitter1_tmpl1_ContentPlaceHolder1_Heade
	                        rBTN1_btnRetrieve)
	  -down DOWNLOAD_BUTTON_ID, --download_button_id DOWNLOAD_BUTTON_ID
	                        the id of the download button in the html source
	                        (default: WebSplitter1_tmpl1_ContentPlaceHolder1_Heade
	                        rBTN1_btnDownload)
	  -v VISIBLE_BROWSER, --visible_browser VISIBLE_BROWSER
	                        whether a browser window should pop up and perform the
	                        scripted actions. Set to False for headerless
	                        (default: True)
	  -a APPEND_SOURCE, --append_source APPEND_SOURCE
	                        whether the url and the pipeline name should be
	                        appended to the entries to show where entry was
	                        fetched from (default: True)
	  -s RETRIEVE_SLEEP_SECONDS, --retrieve_sleep_seconds RETRIEVE_SLEEP_SECONDS
	                        how long the program will sleep after activating the
	                        retrieve button (to help if takes long time to buffer)
	                        (default: 2)
	  -b BASE_URL, --base_url BASE_URL
	                        what webpage to start from (default: https://pipeline2
	                        .kindermorgan.com/LocationDataDownload/LocDataDwnld.as
	                        px?code=ARLS)
	  -cat_n CATEGORY_CLASS_NAME, --category_class_name CATEGORY_CLASS_NAME
	                        the class name from the html source to which signal
	                        which tags to search for in finding categories
	                        (default: igdm_NautilusMenuItemHorizontalRootLink)
	  -cat CATEGORIES [CATEGORIES ...], --categories CATEGORIES [CATEGORIES ...]
	                        the pipelines to pull data from (listed in the
	                        dropdown tabs of webpage). Currently only supports one
	                        pipeline input specified with str (default:
	                        Interstate)
	    
Examples: 

::

    # if the chrome driver exe is in your downloads folder in a folder called chromedriver_win32
    pipeline_download -f download.csv -d chromedriver_win32
    
    # if you wanted all of the pipelines in Midstream
    pipeline_download -cat Midstream
    
