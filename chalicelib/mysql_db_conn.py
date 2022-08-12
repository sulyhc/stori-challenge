import os
import pymysql




def get_db_conn():

    return pymysql.connect(host=os.environ['HOST'],
                                                   user=os.environ['USER'],
                                                   password=os.environ['PASS'],
                                                   db=os.environ['DB'],
                                                   cursorclass=pymysql.cursors.DictCursor)


