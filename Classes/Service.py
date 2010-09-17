import Database

class Listing:
        
    def __init__(self):
        self.db = Database.Connection()    
    
    def mysql(self):
        self.db.cursor.execute("""SELECT services.title,
                                        services.db_name,
                                        services.db_host,
                                        services.db_port,
                                        services.db_user,
                                        results.when,
                                        results.status
                                    FROM services, results
                                    WHERE services.id = results.services_id
                                    AND services.kind = 'mysql'
                                """)
        return self.db.cursor
        
    def http(self):
        self.db.cursor.execute("""SELECT services.title,
                                        services.http_url,
                                        results.when,
                                        results.status
                                    FROM services, results
                                    WHERE services.id = results.services_id
                                    AND services.kind = 'http'
                                """)
        return self.db.cursor
        
    def tcp(self):
        self.db.cursor.execute("""SELECT services.title,
                                        services.tcp_port,
                                        results.when,
                                        results.status
                                    FROM services, results
                                    WHERE services.id = results.services_id
                                    AND services.kind = 'tcp'
                                """)
        return self.db.cursor
