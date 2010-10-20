import subprocess
import Service
import web

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
		<div id="spacer" class="grid_6">&nbsp;</div>	
		<div id="settings" class="grid_1"><a href="/new"><img src="static/images/preferences_system.png" width="32" height="32"></a></div>
        <br /><br /><br />
		<div id="launcherbutton"><button id='run'>Run Checks Now</button></div>
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
            content += "<div class='checkModule grid_15'>"
            content += "<div class='checkName grid_6'><h2>HTTP</h2></div>"
            content += "<div class='grid_15'>"
            content += "<table class='checkTable' width='100%'>"
            content += "<thead><tr><th><b>status</b><th><b>title</b></th></th><th><b>when</b></th><th><b>url</b></th></tr></thead>"
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
            content += "<div class='checkModule grid_15'>"
            content += "<div class='checkName grid_6'><h2>TCP Port</h2></div>"
            content += "<div class='grid_15'>"
            content += "<table class='checkTable' width='100%'>"
            content += "<thead><tr><th><b>status</b><th><b>title</b></th></th><th><b>when</b></th><th><b>ip</b></th><th><b>port</b></th></tr></thead>"
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

        ## ipsec
        listOfChecks = self.serviceList.ipsec()
        if (listOfChecks.rowcount > 0):
            content += "<div class='checkModule grid_15'>"
            content += "<div class='checkName grid_6'><h2>Cisco IPsec</h2></div>"
            content += "<div class='grid_15'>"
            content += "<table class='checkTable' width='100%'>"
            content += "<thead><tr><th><b>status</b><th><b>target</b><th><b>title</b></th></th><th><b>when</b></th><th><b>gateway</b></th><th><b>group</b></th><th><b>user</b></th><th><b>target</b></th></tr></thead>"
            content += "<tbody>"
            for item in listOfChecks.fetchall():
                content += '<tr>'
                content += '<td><img src=\"static/images/' + str(item['status']) + '.png\" /></td>'
                content += '<td><img src=\"static/images/' + str(item['status_secondary']) + '.png\" /></td>'
                content += '<td>' + item['title'] + '</td>'
                content += '<td>' + str(item['last_check']) + '</td>'
                content += '<td>' + str(item['ipsec_gateway']) + '</td>'
                content += '<td>' + str(item['ipsec_group']) + '</td>'
                content += '<td>' + str(item['ipsec_user']) + '</td>'
                content += '<td>' + str(item['ipsec_target_host_ip']) + '</td>'
                content += '</tr>'
            content += "</tbody>"
            content += "</table></div></div>"
            content += '''
                        <script src="static/js/jquery.js" type="text/javascript"></script>
                		<script type="text/javascript">            		    
                    		$("#run").click(function()
                    		{
                    		    $("#launcherbutton").replaceWith('<img src="static/images/ajax-loader.gif" />');
                                $.get("/run/", function(data) {
                                    $('.result').html(data);
                                    location.reload();
                                });
                            });
                		</script>
                        '''
            content += """</div></div></body></html>"""        
        return content

class RunChecks:
    
    def GET(self):
        #TODO: this needs to be called securely!
        subprocess.call('/usr/bin/python launch_checks.py', shell=True)
        
class AddCheck:
        
    def GET(self):
        
        content =  """
        <html>
		<head>
		<title>Simple Server Status</title>
		<link rel="stylesheet" href="../static/styles/reset.css" type="text/css" media="screen" />
		<link rel="stylesheet" href="../static/styles/960.css" type="text/css" media="screen" />
		<link href='http://fonts.googleapis.com/css?family=Droid+Sans:bold' rel='stylesheet' type='text/css'>
		<link rel="stylesheet" href="../static/styles/norm.css" type="text/css" media="screen" />
		</head>
		<body>
		<div id="container" class="container_16">
		<div id="mainContent" class="grid_16">
		<div id="header" class="grid_8">
		<h1>Simple Server Status</h1>
		</div>
		<br /><br /><br />

		<div class='checkModule grid_15'>
		<div class='checkName grid_6'><h2>Add New Check</h2></div>
		<div class='grid_15'>
		<form name="addCheck" method="post" action="index.php">
		<div id="typeCheck">
		<select id="checkType">
		<option value="-q">&nbsp;</option>
		<option value="http">Http</option>
		<option value="tcp">TCP</option>
		<option value="mysql">MySQL</option>
		<option value="ipsec">IPSec</option>
		</select>
		</div>
		<div id="addCheckTable">
		<table id="http" class='checkTable' width='100%'>
		<thead>
		<tr>
		<th><b>title</b></th>
		<th><b>url</b></th>
		</tr>
		</thead>
		<tbody>
		<tr>
		<td><input name="http_title" type="text" size="35" /></td>
		<td><input name="http_url" type="text" size="35" /></td>
		</tr>
		</tbody>
		</table>
		<table id="tcp" class='checkTable' width='100%'>
		<thead>
		<tr>
		<th><b>title</b></th>
		<th><b>IP Address</b></th>
		<th><b>Port</b></th>
		</tr>
		</thead>
		<tbody>
		<tr>
		<td><input name="tcp_title" type="text" size="35" /></td>
		<td><input name="tcp_ip" type="text" size="35" /></td>
		<td><input name="tcp_port" type="text" size="15" /></td>
		</tr>
		</tbody>
		</table>
		<table id="mysql" class='checkTable' width='100%'>
		<thead>
		<tr>
		<th><b>title</b></th>
		<th><b>mysql hostname</b></th>
		<th><b>mysql username</b></th>
		</tr>
		</thead>
		<tbody>
		<tr>
		<td><input name="mysql_title" type="text" size="35" /></td>
		<td><input name="mysql_hostname" type="text" size="35" /></td>
		<td><input name="mysql_user" type="text" size="35" /></td>
		</tr>
		<tr>
		<th><b>mysql password (AES 256 Enabled)</b></th>
		<th><b>mysql port</b></th>
		</tr>
		<tr>
		<td><input name="mysql_pass" type="text" size="35" /></td>
		<td><input name="mysql_port" type="text" size="15" /></td>
		</tr>
		</tbody>
		</table>
		<table id="ipsec" class='checkTable' width='100%'>
		<thead>
		<tr>
		<th><b>title</b></th>
		<th><b>ipsec gateway</b></th>
		<th><b>ipsec group</b></th>
		</tr>
		</thead>
		<tbody>
		<tr>
		<td><input name="ipsec_title" type="text" size="35" /></td>
		<td><input name="ipsec_gateway" type="text" size="35" /></td>
		<td><input name="ipsec_group" type="text" size="35" /></td>
		</tr>
		<tr>
		<th><b>ipsec username</b></th>
		<th><b>ipsec password (AES 256 Enabled)</b></th>
		<th><b>ipsec secret</b></th>
		</tr>
		<tr>
		<td><input name="ipsec_user" type="text" size="35" /></td>
		<td><input name="ipsec_pass" type="text" size="35" /></td>
		<td><input name="ipsec_secret" type="text" size="35" /></td>
		</tr>
		</tbody>
		</table>
		</div>
		<input type="submit" value="Add New Check" />
		</form>
		</div>
		</div>


		</div>
		</div>
		</body>
		<script src="http://code.jquery.com/jquery-1.4.3.min.js" type="text/javascript"></script>
		<script type="text/javascript">
		$(document).ready(function()
		{
		$(".checkTable").hide();

		$("#checkType").change(function()
		{
		$(".checkTable").hide();
		$("#"+$("#checkType").val()).slideDown(500);
		});

		});
		</script>
		</html>
		"""
