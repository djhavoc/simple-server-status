class Services:
    
    def __init__(self):
        ## establish database connection
        result = Database.connect_database()
        self.dbCursor = result[0]
        self.dbConn = result[1]
    
    def mysqlChecks(self):
        checks = {}
        return checks
        
    def httpChecks(self):
        checks = {}
        return checks
        
    def tcpChecks(self):
        checks = {}
        return checks