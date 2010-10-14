import Database

class Listing:
        
    def __init__(self):
        self.db = Database.Connection()    
    
    def mysql(self):
        self.db.cursor.execute("""SELECT 
                                        services.id,
                                        services.title,
                                        services.db_name,
                                        services.db_host,
                                        services.db_user,
                                        results.services_id,
                                        results.last_check,
                                        results.status
                                    FROM services, results
                                    WHERE services.id = results.services_id
                                    AND services.kind = 'mysql'
                                """)
        return self.db.cursor
        
    def http(self):
        self.db.cursor.execute("""SELECT 
                                        services.id,
                                        services.title,
                                        services.http_url,
                                        results.services_id,
                                        results.last_check,
                                        results.status
                                    FROM services, results
                                    WHERE services.id = results.services_id
                                    AND services.kind = 'http'
                                """)
        return self.db.cursor
        
    def tcp(self):
        self.db.cursor.execute("""SELECT 
                                        services.id,
                                        services.title,
                                        services.tcp_ip,
                                        services.tcp_port,
                                        results.services_id,
                                        results.last_check,
                                        results.status
                                    FROM services, results
                                    WHERE services.id = results.services_id
                                    AND services.kind = 'tcp'
                                """)
        return self.db.cursor

    def ipsec(self):
        self.db.cursor.execute("""SELECT 
                                        services.id,
                                        services.title,
                                        services.ipsec_gateway,
                                        services.ipsec_group,
                                        services.ipsec_user,
                                        results.services_id,
                                        results.last_check,
                                        results.status
                                    FROM services, results
                                    WHERE services.id = results.services_id
                                    AND services.kind = 'ipsec'
                                """)
        return self.db.cursor
