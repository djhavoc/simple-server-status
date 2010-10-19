import sys
import os
import pexpect
import copy
import MySQLdb
import socket
#import TimeoutSocket
import urllib2
import Database
import config
import time

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

        if (kind == 'ipsec'):
            self.db.cursor.execute("""SELECT id, 
                                                title, 
                                                ipsec_gateway, 
                                                ipsec_group, 
                                                AES_DECRYPT(ipsec_secret,'%s') as ipsec_secret,
                                                ipsec_user,
                                                AES_DECRYPT(ipsec_pass,'%s') as ipsec_pass                                                
                                        FROM services
                                        WHERE services.kind = 'ipsec'""" %(config.DB_CRYPTOKEY,config.DB_CRYPTOKEY))

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

        elif (kind == 'ipsec'):
            if (self.db.cursor.rowcount > 0):
                for item in self.db.cursor.fetchall():
                    self.ipsec(item['id'], item['ipsec_gateway'], item['ipsec_group'], item['ipsec_secret'], item['ipsec_user'], item['ipsec_pass'])        

        return True

    def ipsec(self, serviceID, ipsec_gateway, ipsec_group, ipsec_secret, ipsec_user, ipsec_pass):
        '''check ipsec tunnel'''

        
        ## establish vpn connection
        vpncShell = pexpect.spawn('/sbin/vpnc')
        vpncShell.logfile = sys.stdout

        vpncShell.expect('Enter IPSec gateway address:')
        vpncShell.sendline(ipsec_gateway)        

        vpncShell.expect('Enter IPSec ID for %s:' %(ipsec_gateway))
        vpncShell.sendline(ipsec_group)

        vpncShell.expect('Enter IPSec secret for %s@%s:' % (ipsec_group, ipsec_gateway))
        vpncShell.sendline(ipsec_secret)

        vpncShell.expect('Enter username for %s:' % (ipsec_gateway))
        vpncShell.sendline(ipsec_user)

        vpncShell.expect('Enter password for %s@%s:' % (ipsec_user, ipsec_gateway))
        vpncShell.sendline(ipsec_pass)


        vpncShell.expect('VPNC started in background')


        time.sleep(1)
        pexpect.run('sudo /sbin/route add -host 172.24.13.11 dev tun0')

        print pexpect.run('/bin/netstat -r')
        time.sleep(10)
        vpncShell.sendline('ping 172.24.13.11 -c 2')

        vpncDisconnectShell = pexpect.spawn('/sbin/vpnc-disconnect')
        
        
        
        
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
        socket.setdefaulttimeout(2)
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
        self.recordResult(status, serviceID)
        
