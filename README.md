_README for Todoist CLI scripts_

Simple CLI script to add a task to todoist.   Uses the official python API.

To install the scripts first clone the repo and then run make install from 
the cloned directory.   This expects to use pip to install the various extra
python libraries needed.

To use from command line you must first create a simple configuration file, 
default ~/.todoist-cli with the following format:

    [Authentication]
    api=xxxx
    [Network]
    proxy_pac=zzzz
    http_proxy=xxxx
    https_proxy=yyyy

The only mandatory value is the api value which is obtained from the users
Todoist account page.

An osascript is also provided to take the selected Outlook message and create
a task in Todoist via the python script.   I use Alfred to map to a key stroke.


