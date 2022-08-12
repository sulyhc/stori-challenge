import os
import pymysql




def get_db_conn():

    return pymysql.connect(host=os.environ['HOST_DB'],
                                                   user=os.environ['USER_DB'],
                                                   password=os.environ['PASS_DB'],
                                                   db=os.environ['SCHEMA_DB'],
                                                   cursorclass=pymysql.cursors.DictCursor)


