import Service

#from Check import *

class Status:

    ## fetch all checks data and display
    def GET(self):

        self.serviceList = Service.Listing()
        
        content = """
        <html>
        <head>
        <title>Simple Server Status</title>
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
            content += "<tr><td>title</td><td>status</td><td>when</td><td>database</td><td>host</td><td>port</td><td>user</td></tr>"
            for item in listOfChecks.fetchall():
                content += '<tr>'
                content += '<td>' + item['title'] + '</td>'
                content += '<td>' + item['status'] + '</td>'
                content += '<td>' + str(item['when']) + '</td>'
                content += '<td>' + item['db_name'] + '</td>'
                content += '<td>' + item['db_host'] + '</td>'
                content += '<td>' + str(item['db_port']) + '</td>'
                content += '<td>' + item['db_user'] + '</td>'
                content += '<tr>'        
            content += "</table>"

        ## http
        listOfChecks = self.serviceList.http()
        if (listOfChecks.rowcount > 0):
            content += "<h2>HTTP</h2>"
            content += "<table>"
            content += "<tr><td>title</td><td>status</td><td>when</td><td>url</td></tr>"
            for item in listOfChecks.fetchall():
                content += '<tr>'
                content += '<td>' + item['title'] + '</td>'
                content += '<td>' + item['status'] + '</td>'
                content += '<td>' + str(item['when']) + '</td>'
                content += '<td>' + str(item['http_url']) + '</td>'
                content += '<tr>'        
            content += "</table>"

        ## tcp
        listOfChecks = self.serviceList.tcp()
        if (listOfChecks.rowcount > 0):
            content += "<h2>TCP Port</h2>"
            content += "<table>"
            content += "<tr><td>title</td><td>status</td><td>when</td><td>port</td></tr>"
            for item in listOfChecks.fetchall():
                content += '<tr>'
                content += '<td>' + item['title'] + '</td>'
                content += '<td>' + item['status'] + '</td>'
                content += '<td>' + str(item['when']) + '</td>'
                content += '<td>' + str(item['tcp_port']) + '</td>'
                content += '<tr>'        
            content += "</table>"
        
        content += """</body></html>"""        
        return content

class AddCheck:
        
    def GET(self):
        
        content = "AddCheck"
        return content