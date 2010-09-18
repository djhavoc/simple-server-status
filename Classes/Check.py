import copy
import MySQLdb
import urllib
import TimeoutSocket
import Database
import config

class Checks:
    
    def __init__(self):
        self.db = Database.Connection()
    
    ## build list of services for an inspection
    def servicesToInspect(self, kind):
        if (kind == 'mysql'):
            print config.DB_CRYPTOKEY
            self.db.cursor.execute("""SELECT id, 
                                                title, 
                                                db_name, 
                                                db_host,
                                                db_user, 
                                                AES_DECRYPT(db_pass,'%s') as db_pass
                                        FROM services 
                                        WHERE services.kind = 'mysql'""" %(config.DB_CRYPTOKEY))

        elif (kind == 'http'):
            ## http
            self.db.cursor.execute("""SELECT id, http_url
                                                        FROM services 
                                                        WHERE services.kind = 'http'""")

        
        elif (kind == 'tcp'):
            self.db.cursor.execute("""SELECT id, tcp_ip, tcp_port
                                                        FROM services 
                                                        WHERE services.kind = 'tcp'""")

    ## perform inspections
    def run(self, kind):
        if (kind == 'mysql'):
            if (self.db.cursor.rowcount > 0):
                for item in self.db.cursor.fetchall():
                    self.mysql(item['id'], item['db_host'], item['db_name'], item['db_user'], item['db_pass'])

        elif (kind == 'http'):
            if (self.db.cursor.rowcount > 0):
                for item in self.db.cursor.fetchall():
                    self.http(item['id'], item['http_url'])        
        
        elif (kind == 'tcp'):
            if (self.db.cursor.rowcount > 0):
                for item in self.db.cursor.fetchall():
                    self.tcp(item['id'], item['ip'], item['tcp_port'])        

        return True
        
    def recordResult(self, status, serviceID):
        self.db.cursor.execute("""UPDATE results SET last_check = NOW(), status = '%s' WHERE services_id = %s """ % (status, serviceID))
        return self.db.cursor.lastrowid
    
    ## check a mysql connection
    def mysql(self, serviceID, host, name, user, passwd):
        print serviceID
        print host
        print name
        print user
        print passwd
        try:
            dbConn = MySQLdb.connect (host = host,
                                    user = user,
                                    passwd = passwd,
                                    db = name)
            status = 'good'
        except MySQLdb.Error, e:
            status = 'bad'
        print status
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
