#!/usr/bin/env python

import MySQLdb
import config

def connect_database():
	try:
		dbConn = MySQLdb.connect (host = config.DB_HOST,
								user = config.DB_USER,
								passwd = config.DB_PASSWD,
								db = config.DB_NAME)
	except MySQLdb.Error, e:
		print "Error %d: %s" % (e.args[0], e.args[1])
		sys.exit (1)
	dbCursor = dbConn.cursor (MySQLdb.cursors.DictCursor)
	return dbCursor, dbConn