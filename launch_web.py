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