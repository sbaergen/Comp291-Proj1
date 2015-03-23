import cx_Oracle
import getpass
import datetime

def getPic(File_name):
        # #Load image into memory from local file
        # #(Assumes a file by this name exists in the directory you are running from)
        f_image  = open(File_name,'rb')
        image  = f_image.read()
        f_image.close()
        return image

def getDate(message):
        while(True):
                date = input(message)
                try:
                        datetime.datetime.strptime(date, '%Y-%m-%d')
                        return date
                except:
                        print("Incorrect data format, should be YYYY-MM-DD")
        return None


class SqlConnection:
        def __init__(self, user, passw):
                # create the new connection
                self.con = cx_Oracle.connect(user+"/"+passw+"@gwynne.cs.ualberta.ca:1521/CRS")  # lets see if this works!
                self.con.autocommit = 1  # save the changes we make

                self.curs = self.con.cursor()

        def execute(self, statement, dict = {}):
                return self.curs.execute(statement,dict)

        def exeAndFetch(self, statement):
                return self.curs.execute(statement).fetchall()

        def executeFromFile(self, fileName):
                # may want a try catch in here eventually
                f = open(fileName)
                pop = f.read().replace("\n", "").split(";")
                for t in pop:
                        if (len(t) <= 0):
                                continue
                        self.curs.execute(t)
                f.close()
                return None

        def getCurs(self):
                return self.curs

        def commitOff(self):
                self.con.autocommit = 0

        def commitOn(self):
                self.con.autocommit = 1

        def close(self):
                self.curs.close()
                self.con.close()
