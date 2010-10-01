import copy
import MySQLdb
import socket
#import TimeoutSocket
import urllib2
import Database
import config

class Checks:
    
    def __init__(self):
        self.db = Database.Connection()
        
    def closeDatabase(self):
        self.db.cursor.close()
        self.db.connection.commit()
        self.db.connection.close()
    
    ## build list of services for an inspection
    def servicesToInspect(self, kind):
        if (kind == 'mysql'):
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
                    self.tcp(item['id'], item['tcp_ip'], item['tcp_port'])        

        return True
        
    def recordResult(self, status, serviceID):
        self.db.cursor.execute("""UPDATE results SET last_check = NOW(), status = '%s' WHERE services_id = %s """ % (status, serviceID))
        return self.db.cursor.lastrowid
    
    ## check a mysql connection
    def mysql(self, serviceID, host, name, user, passwd):
        try:
            dbConn = MySQLdb.connect (host = host,
                                    user = user,
                                    passwd = passwd,
                                    db = name)
            status = 'good'
            dbConn.close()
        except MySQLdb.Error, e:
            status = 'bad'
        self.recordResult(status, serviceID)
                    
    ## check a web service
    def http(self, serviceID, url):
        try:
            result = urllib2.urlopen(url)
            #print result.read(100)
            status = 'good'
        except IOError, e:
            status = 'bad'
        self.recordResult(status, serviceID)
        
    ## check a tcp port
    def tcp(self, serviceID, ip, port):
        #TimeoutSocket.setDefaultSocketTimeout(20)
        s = None
        for res in socket.getaddrinfo(ip, int(port), socket.AF_UNSPEC, socket.SOCK_STREAM):
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
