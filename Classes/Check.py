import MySQLdb
import urllib
import TimeoutSocket
import Database
import config

class Checks:
    
    def __init__(self):
        self.db = Database.Connection()
    
    ## build list of services for an inspection
    def servicesToInspect(self):
        ## mysql
        self.db.cursor.execute("""SELECT id, 
                                            title, 
                                            db_name, 
                                            db_host,
                                            db_user, 
                                            AES_DECRYPT('db_pass','%s') as db_pass
                                    FROM services 
                                    WHERE services.kind = 'mysql'""" %(config.DB_CRYPTOKEY))
        self.queueMysql = self.db.cursor
                                                    
        ## http
        self.db.cursor.execute("""SELECT id, http_url
                                                    FROM services 
                                                    WHERE services.kind = 'http'""")
        self.queueHttp = self.db.cursor

        
        ## tcp
        self.db.cursor.execute("""SELECT id, tcp_ip, tcp_port
                                                    FROM services 
                                                    WHERE services.kind = 'tcp'""")
        self.queueTcp = self.db.cursor

        self.run()

    ## perform inspections
    def run(self):
        ## mysql
        if (self.queueMysql.rowcount > 0):
            for item in self.queueMysql.fetchall():
                #self.mysql(item['id'], item['db_host'], item['db_name'], item['db_user'], item['db_pass'])
                pass
        ## http
        if (self.queueHttp.rowcount > 0):
            for item in self.queueHttp.fetchall():
                self.http(item['id'], item['http_url'])        
        
        ## tcp
        if (self.queueTcp.rowcount > 0):
            for item in self.queueTcp.fetchall():
                self.tcp(item['id'], item['ip'], item['tcp_port'])        

        return True
        
    def recordResult(self, status, serviceID):
        self.db.cursor.execute("""INSERT INTO results
                                    SET when = NOW(), status = '%s'
                                    WHERE services_id = %s
                                """ % (status, serviceID))
        return db.cursor.lastrowid
    
    ## check a mysql connection
    def mysql(self, serviceID, host, name, user, passwd):
        try:
            dbConn = MySQLdb.connect (host = host,
                                    user = user,
                                    passwd = passwd,
                                    db = name)
            status = 'good'
        except MySQLdb.Error, e:
            status = 'bad'
        self.recordResult(status, serviceID)
                    
    ## check a web service
    def http(self, serviceID, url):
        urllib.cleanup()
        try:
            urllib.URLopener(url)
            status = 'good'
        except IOError, e:
            status = 'bad'
        self.recordResult(status, serviceID)
        
    ## check a tcp port
    def tcp(self, serviceID, ip, port):
        TimeoutSocket.setDefaultSocketTimeout(20)
        s = None
        for res in socket.getaddrinfo(ip, port, socket.AF_UNSPEC, socket.SOCK_STREAM):
            af, socktype, proto, canonname, sa = res
            try:
                s = socket.socket(af, socktype, proto)
                status = 'good'
            except socket.error, msg:
                status = 'bad'
                s = None
                continue
            try:
                s.connect(sa)
                status = 'good'
            except socket.error, msg:
                status = 'bad'
                s.close()
                s = None
                continue
            break
        s.close()
        self.recordResult(status, serviceID)
