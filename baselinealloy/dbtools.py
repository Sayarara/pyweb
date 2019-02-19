import pymysql

def searchFromMysql(kws):
    db = pymysql.connect('localhost', 'root', '', 'er_test')
    cursor = db.cursor()
    args = '%' + kws + '%'
    sql = "SELECT ID,textual  FROM abtbuycluster where textual LIKE '%s'" % (args)
    # sql = "SELECT ID,textual  FROM abtbuycluster WHERE unique_id = %d " % (1044)
    cursor.execute(sql)
    results = cursor.fetchall()
    d = {}
    for row in results:
        d[row[0]] = row[1]
    db.close()
    return d

def getDataFromMysql():
    db = pymysql.connect('localhost', 'root', '', 'er_test')
    cursor = db.cursor()
    sql = "SELECT ID, textual FROM abtbuycluster ORDER BY ID"
    cursor.execute(sql)
    results = cursor.fetchall()
    d = {}
    for row in results:
        d[row[0]] = row[1]
    db.close()
    return  d