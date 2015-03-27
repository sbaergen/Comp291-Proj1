import cx_Oracle
import getpass
import datetime

def getPic(message):
	image = None
	while(True):
		try:
			File_name = input(message)
			f_image  = open(File_name,'rb')
			image  = f_image.read()
			f_image.close()
			break
		except:
			print("Error opening the file, please try again.")
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

def getString(message, maxLen = None, minLen = 0, contains = None):
	valid = False
	while not valid:
		valid = True
		string = input(message)
		if minLen is not None:
			if len(string) < minLen:
				valid = False
				print("String too short, try again")
		if maxLen is not None:
			if len(string) > maxLen:
				valid = False
				print("String too long, try again")
		if contains is not None:
			for char in string:
				if char not in contains:
					valid = False
					print("Invalid characters entered, try again")
	return string

def getNumber(message, maxLen = None, minLen = 0, maxValue = None, minValue = None):
	number = None
	while(True):
		try:
			number = eval(input(message))
		except:
			print("Invalid input, try again.")
			continue
		length = len(str(number))
		if maxLen is not None:
			if length > maxLen:
				print("Number length too long, try again.")
				continue
		if minLen is not None:
			if length < minLen:
				print("Number length too short, try again.")
				continue
		if maxValue is not None:
			if number > maxValue:
				print("Value too large, try again.")
				continue
		if minValue is not None:
			if number < minValue:
				print("Value too small, try again.")
				continue
		return number


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
