#### Simple Server Status
####
#### http://github.com/joet3ch/simple-server-status
####
#### joet3ch (joe@t3ch.com)
####

## launch web app

import sys
sys.path.append('Classes/')
sys.path.append('Classes/webpy/')
import web
from WebView import *

## define views
urls = ( 
    '/', 'Status',
    '/status', 'Status',
    '/status/', 'Status',
    '/new', 'AddCheck',
    '/new/', 'AddCheck'
    )

app = web.application(urls, globals())
        
if __name__ == "__main__":
    app.run()