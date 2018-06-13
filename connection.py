import MySQLdb
def connection():
    try:
        # conn=MySQLdb.connect(host='localhost',user='root',password='mysql',db='product',port=3306)
        conn = MySQLdb.connect('localhost','root','mysql','product',)
        cur=conn.cursor()
    except:
        print "errror"
    return cur,conn