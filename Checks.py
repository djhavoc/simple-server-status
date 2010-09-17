class Checks:
    
    def databaseMysql(self, host, name, user, passwd):
    	try:
    		dbConn = MySQLdb.connect (host = host,
    								user = user,
    								passwd = passwd,
    								db = name)
    		return True
    	except MySQLdb.Error, e:
            return False
            
    def mysql(self, dbHost, dbName, dbUser, dbPass):    
        
    def http(self, url):

        result = ''
        return result
        
    def tcpPort(self, port):

        result = ''
        return result