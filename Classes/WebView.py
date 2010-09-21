import Service

class Status:

    ## fetch all checks data and display
    def GET(self):

        self.serviceList = Service.Listing()
        
        content = """
        <html>
        <head>
        <title>Simple Server Status</title>
        <link rel="stylesheet" href="static/styles/reset.css" type="text/css" media="screen" />
        <link rel="stylesheet" href="static/styles/960.css" type="text/css" media="screen" />
        <link href='http://fonts.googleapis.com/css?family=Droid+Sans:bold' rel='stylesheet' type='text/css'>
        <link rel="stylesheet" href="static/styles/norm.css" type="text/css" media="screen" />
        </head>
        <body>
        <div id="container" class="container_16">
        <div id="mainContent" class="grid_16">
        <div id="header" class="grid_8">
        <h1>Simple Server Status</h1>
        </div>
        <br /><br /><br />
        """

        ## mysql
        listOfChecks = self.serviceList.mysql()
        if (listOfChecks.rowcount > 0):
            content += "<div class='checkModule grid_15'>"
            content += "<div class='checkName grid_6'><h2>MySQL</h2></div>"
            content += "<div class='grid_15'>"
            content += "<table class='checkTable' width='100%'>"
            content += "<thead><tr><th><b>status</b></th><th><b>title</b></th><th><b>when</b></th><th><b>database</b></th><th><b>host</b></th><th><b>user</b></th></tr></thead>"
            content += "<tbody>"
            for item in listOfChecks.fetchall():
                content += '<tr>'
                content += '<td><img src=\"static/images/' + str(item['status']) + '.png\" /></td>'
                content += '<td>' + item['title'] + '</td>'
                content += '<td>' + str(item['last_check']) + '</td>'
                content += '<td>' + item['db_name'] + '</td>'
                content += '<td>' + item['db_host'] + '</td>'
                content += '<td>' + item['db_user'] + '</td>'
                content += '</tr>'        
            content += "</tbody>"
            content += "</table></div></div>"

        ## http
        listOfChecks = self.serviceList.http()
        if (listOfChecks.rowcount > 0):
            content += "<div class='checkModule grid_16'>"
            content += "<div class='checkName grid_6'><h2>HTTP</h2></div>"
            content += "<div class='grid_15'>"
            content += "<table class='checkTable' width='100%'>"
            content += "<thead><tr><th><b>title</b></th><th><b>status</b></th><th><b>when</b></th><th><b>url</b></th></tr></thead>"
            content += "<tbody>"
            for item in listOfChecks.fetchall():
                content += '<tr>'
                content += '<td><img src=\"static/images/' + str(item['status']) + '.png\" /></td>'
                content += '<td>' + item['title'] + '</td>'
                content += '<td>' + str(item['last_check']) + '</td>'
                content += '<td>' + str(item['http_url']) + '</td>'
                content += '</tr>'
            content += "</tbody>"
            content += "</table></div></div>"

        ## tcp
        listOfChecks = self.serviceList.tcp()
        if (listOfChecks.rowcount > 0):
            content += "<div class='checkModule grid_16'>"
            content += "<div class='checkName grid_6'><h2>TCP Port</h2></div>"
            content += "<div class='grid_15'>"
            content += "<table class='checkTable' width='100%'>"
            content += "<thead><tr><th><b>title</b></th><th><b>status</b></th><th><b>when</b></th><th><b>ip</b></th><th><b>port</b></th></tr></thead>"
            content += "<tbody>"
            for item in listOfChecks.fetchall():
                content += '<tr>'
                content += '<td><img src=\"static/images/' + str(item['status']) + '.png\" /></td>'
                content += '<td>' + item['title'] + '</td>'
                content += '<td>' + str(item['last_check']) + '</td>'
                content += '<td>' + str(item['tcp_ip']) + '</td>'
                content += '<td>' + str(item['tcp_port']) + '</td>'
                content += '</tr>'
            content += "</tbody>"
            content += "</table></div></div>"

            content += """</div></div></body></html>"""        
        return content

class AddCheck:
        
    def GET(self):
        
        content = "AddCheck"
        return content