import pymysql as mysql

def ConnectionPooling():
    db=mysql.connect(host='localhost', port=3306,user='root',passwd='1234',database='medassist_com',cursorclass=mysql.cursors.DictCursor,)
    cmd=db.cursor()

    return db,cmd

