import Service

class Status:

    ## fetch all checks data and display
    def GET(self):

        self.serviceList = Service.Listing()
        
        content = """
        <html>
        <head>
        <title>Simple Server Status</title>
        <link rel="stylesheet" href="static/styles/norm.css" type="text/css" media="screen" />
        </head>
        <body>
        <h1>Simple Server Status</h1>
        <br /><br />
        """
        
        ## mysql
        listOfChecks = self.serviceList.mysql()
        if (listOfChecks.rowcount > 0):
            content += "<h2>MySQL</h2>"
            content += "<table>"
            content += "<tr><td><b>status</b></td><td><b>title</b></td><td><b>when</b></td><td><b>database</b></td><td><b>host</b></td><td><b>user</b></td></tr>"
            for item in listOfChecks.fetchall():
                content += '<tr>'
                content += '<td><img src=\"static/images/' + str(item['status']) + '.png\" /></td>'
                content += '<td>' + item['title'] + '</td>'
                content += '<td>' + str(item['last_check']) + '</td>'
                content += '<td>' + item['db_name'] + '</td>'
                content += '<td>' + item['db_host'] + '</td>'
                content += '<td>' + item['db_user'] + '</td>'
                content += '<tr>'        
            content += "</table>"

        ## http
        listOfChecks = self.serviceList.http()
        if (listOfChecks.rowcount > 0):
            content += "<h2>HTTP</h2>"
            content += "<table>"
            content += "<tr><td><b>title</b></td><td><b>status</b></td><td><b>when</b></td><td><b>url</b></td></tr>"
            for item in listOfChecks.fetchall():
                content += '<tr>'
                content += '<td><img src=\"static/images/' + str(item['status']) + '.png\" /></td>'
                content += '<td>' + item['title'] + '</td>'
                content += '<td>' + str(item['last_check']) + '</td>'
                content += '<td>' + str(item['http_url']) + '</td>'
                content += '<tr>'        
            content += "</table>"

        ## tcp
        listOfChecks = self.serviceList.tcp()
        if (listOfChecks.rowcount > 0):
            content += "<h2>TCP Port</h2>"
            content += "<table>"
            content += "<tr><td><b>title</b></td><td><b>status</b></td><td><b>when</b></td><td><b>ip</b></td><td><b>port</b></td></tr>"
            for item in listOfChecks.fetchall():
                content += '<tr>'
                content += '<td><img src=\"static/images/' + str(item['status']) + '.png\" /></td>'
                content += '<td>' + item['title'] + '</td>'
                content += '<td>' + str(item['last_check']) + '</td>'
                content += '<td>' + str(item['tcp_ip']) + '</td>'
                content += '<td>' + str(item['tcp_port']) + '</td>'
                content += '<tr>'        
            content += "</table>"
        
        content += """</body></html>"""        
        return content

class AddCheck:
        
    def GET(self):
        
        content = "AddCheck"
        return content