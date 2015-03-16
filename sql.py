import cx_Oracle
import getpass

def main():
        user = input("User [%s]:" % getpass.getuser())
        if not user:
                user = getpass.getuser()
        passw = getpass.getpass("Pass:")

        # create a new instance of a connection object
        sql = SqlConnection(user, passw)

        # Drop & Create Tables
        print("Dropping / Creating Tables")
        sql.executeFromFile("p1_setup.sql.txt")

        # Populate tables
        print("Populate Tables")
        sql.executeFromFile("population.txt")

        sql.close()  # clean up sql object


class SqlConnection:
        def __init__(self, user, passw):
                # create the new connection
                self.con = cx_Oracle.connect(user+"/"+passw+"@gwynne.cs.ualberta.ca:1521/CRS")  # lets see if this works!
                self.con.autocommit = 1  # un tested I think this is how to change autocommit properties

                self.curs = self.con.cursor()

        def execute(self, statement):
                return self.curs.execute(statement)

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

        def close(self):
                self.curs.close()
                self.con.close()

# old demo code

# # drop tables if they exist
# statement = "drop table movie"
# curs.execute(statement)
#
# # create table statements
# statement = "create table movie(title char(20), movie_number integer, primary key(movie_number))"
# curs.execute(statement)
#
# # insert data into tables
# statement = "insert into movie values('Chicago', 1)"
# curs.execute(statement)
#
# # make a selection from the data
# query = "select title, movie_number from movie"
# curs.execute(query)
# rows = curs.fetchall()

# close connection and curs

