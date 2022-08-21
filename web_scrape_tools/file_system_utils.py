from pathlib import Path
import time

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

import file_system_utils as fileu