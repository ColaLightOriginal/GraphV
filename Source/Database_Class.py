import mysql.connector as sql

class Database:
    def __init__(self,user,password, host):
        self.conn=sql.connect(user=user,password=password,host=host,charset="utf8",use_unicode=True)
        self.mycursor=self.conn.cursor()

    def printTable(self, tableName):
        self.mycursor.execute("""SELECT * FROM UMKnotPrecise.""" + tableName)
        print self.mycursor.fetchall()

    # def returnTable(self, tableName, databaseName):
    #     self.mycursor.execute("""SELECT * FROM UMKnotPrecise.""" + tableName)
    #     return self.mycursor.fetchall()

    def returnTable(self, tableName, databaseName):
        self.mycursor.execute("""SELECT * FROM """ + databaseName + "." + tableName)
        return self.mycursor.fetchall()

    def returnDistinctMails(self,databaseName):
        self.mycursor.execute("""SELECT DISTINCT mail from """ + databaseName + ".employess" )
        return self.mycursor.fetchall()
