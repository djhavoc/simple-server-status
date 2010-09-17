class Checks:
    
    def mysql(self, host, name, user, passwd):
    	try:
    		dbConn = MySQLdb.connect (host = host,
    								user = user,
    								passwd = passwd,
    								db = name)
    		return True
    	except MySQLdb.Error, e:
            return False
                    
    def http(self, url):

        result = ''
        return True
        
    def tcp(self, port):

        result = ''
        return True