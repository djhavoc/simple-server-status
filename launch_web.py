#### Simple Server Status
####
#### http://github.com/joet3ch/simple-server-status
####
#### joet3ch (joe@t3ch.com)
####

import sys
sys.path.append('webpy/')
import web
from WebView import *

## define views
urls = ( 
    '/(.*)', 'Status' )

app = web.application(urls, globals())
        
if __name__ == "__main__":
    app.run()