#!/usr/local/bin/python
'''
This module provides a CLI to add a task to Todoist. The Todoist API is 
built using official python library from https://developer.todoist.com/
''' 

__author__      = "Mark Hannon"
__copyright__   = "Copyright 2015 Mark Hannon"
__version__     = "0.1"
__date__        = "2015-11-25"
__email__       = "mark.hannon@gmail.com"

import argparse
import ConfigParser
import os
import sys
import urllib2

''' 
https://github.com/pacparser/pacparser
https://developer.todoist.com/#api-overview
'''
import pacparser
import todoist

def is_reachable(proxy_value):
  try:
    host = proxy_value.split(':')[0]
    port = proxy_value.split(':')[1]
    s = socket.create_connection((host, port), 2)
    return True
  except:
     pass
  return False
  
def main(args):
    
    ''' Parse arguments into options dictionary '''
    
    parser = argparse.ArgumentParser(prog='todoist-add', 
                                     description='Add task to Todoist')

    parser.add_argument("--config", action="store", 
                        help="Configuration file with API")
    parser.add_argument("--item", action="store", 
                        help="Item text",
                        required=True)
    parser.add_argument("--note", action="store", 
                        help="Note text")
    parser.add_argument("--date", action="store", 
                        help="Date text - any format Todoist can parse")

    options = vars(parser.parse_args(sys.argv[1:]))
    
    ''' Load user configuration file for API key etal '''
    
    if options['config']:
        cf = options['config']
    else:
        cf = os.getenv('HOME') + '/.todoist-cli'
        
    config = ConfigParser.RawConfigParser()
    files_read = config.read(cf)
    
    if files_read == []:
        print "Unable to open configuration file " + cf + "- aborting"
        sys.exit(1)
    
    '''
    [Authentication]
    api=xxxx
    [Network]
    proxy_pac=zzzz
    http_proxy=xxxx
    https_proxy=yyyy
    '''
        
    api_key = config.get('Authentication', 'api')
    
    if api_key == '':
        print "Unable to read API value from " + cf + "- aborting"
        sys.exit(1)
        
    if config.has_section('Network'):
      
        if config.has_option('Network', 'proxy_pac'):

            proxy_pac = config.get('Network', 'proxy_pac')

            if proxy_pac != '':

                ''' Check if proxy pac exists - if so use it to set proxy '''

                try:

                    response = urllib2.urlopen(proxy_pac)
                    pac_file_contents = response.read()

                    pacparser.init()
                    pacparser.parse_pac_string(pac_file_contents)
                    https_proxy = pacparser.find_proxy('https://todoist.com', 'todoist.com').split(' ')[1]
                    pacparser.cleanup()

                    ''' Set the proxy environment '''
                    os.environ['HTTP_PROXY'] = https_proxy
                    os.environ['HTTPS_PROXY'] = https_proxy

                except IOError as e:

                    print e

        else:

            ''' Check if explicit proxy exists and use '''

            http_proxy = config.get('Network', 'http_proxy')
            if http_proxy != '':
                os.environ['HTTP_PROXY'] = http_proxy
                
            https_proxy = config.get('Network', 'https_proxy')
            if https_proxy != '':
                os.environ['HTTPS_PROXY'] = https_proxy

    ''' Use the user Todoist API key to connect '''
        
    api = todoist.TodoistAPI(api_key)
    
    if api:
        
        if options['date']:
            item = api.items.add(options['item'], 0, date_string=options['date'])
        else:
            item = api.items.add(options['item'], 0)
            
        if debug:
            print item

        if options['note']:
            note = api.notes.add(item['id'], options['note'])

            if debug:
                print note

        ''' Commit the transaction to Todoist '''
        
        result = api.commit()
        
        if debug:
            print "Result:"
            print result
            print "Settings:"
            print "API Key=" + api_key
            if proxy_pac:
                print "PAC=" + proxy_pac
            print "HTTP_PROXY=" + os.getenv('HTTP_PROXY', "Not set")
            print "HTTPS_PROXY=" + os.getenv('HTTPS_PROXY', "Not set")
    
    else:
        
        print "Unable to connect to Todoist with API key - aborting"
        print api
        sys.exit(1)

if __name__ == '__main__':
    
    debug = True
    
    main(sys.argv[1:])
