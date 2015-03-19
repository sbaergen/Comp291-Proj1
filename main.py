import getpass
import sql as sqlFile
import os,sys
#import Image

# This will display the menu and handle input to the menu
def main():
        print("Please login before proceeding.")
        sql = None  # I don't want the sql obj to be local to the while loop
        while(True):  # cont here
                try:
                        user = input("User [%s]:" % getpass.getuser())
                        if not user:
                                user = getpass.getuser()
                        passw = getpass.getpass("Pass:")

                        # create a new instance of a connection object
                        sql = sqlFile.SqlConnection(user, passw)

                        break
                except:
                        print("Oops, try again!")
                        continue

        # Drop & Create Tables
        print("Dropping / Creating Tables")
        sql.executeFromFile("p1_setup.sql.txt")

        # Populate tables
        print("Populate Tables")
        sql.executeFromFile("population.txt")

        print ("Welcome to the Alberta Auto Registration System!")
        while(True):
                print (
"""----------------------------------------
Please Select from the following:
                1:New Vehicle Registration
                2:Auto Transaction
                3:Driver Licence Registration
                4:Violation Record
                5:Search Engine
                6:Exit""")
                choice = None
                while(True):
                        try:
                                choice = eval(input("Choice (1-6): "))
                                if (not (choice >= 1 and choice <=6)):
                                        print ("Invalid Input!", end = " ")
                                else:
                                        break
                        except:
                                print ("Invalid Input!", end = " ")
                if choice == 1:
                        newVehicle(sql)
                elif choice == 2:
                        autoTrans(sql)
                elif choice == 3:
                        licenceReg(sql)
                elif choice == 4:
                        violationRec(sql)
                elif choice == 5:
                        searchEngine(sql)
                elif choice == 6:
                        break
                else:
                        continue
                        print ("Invalid Input!", end = " ")
                        print (choice)


        sql.close()  # clean up sql object



# Register new vehicle by officer. All detailed information about the vehicle and personal information about the owner.
# You may assume all vehicle types have been loaded into the inital database.
# Create a new vehicle and select owner, if no owner exists create a new person
def newVehicle(sql):
        print("NEW VEHICLE REGISTRATION")
        print("")
        serial_no = input("Enter serial_no of vehicle: ")
        maker = input("Enter the make of the vehicle: ")
        model = input("Enter the model of the vehicle: ")
        year = input("Enter the year of the vehicle: ")
        color = input("Enter the color of the vehicle: ")
        vehicleType = eval(input("Enter the type of the vehicle (1=car,2=suv,3=crossover,4=van,5=truck): "))

        # todo: lets check all of the params

        string = "insert into vehicle values('{:s}','{:s}','{:s}','{:s}','{:s}',{:d})"
        sql.execute(string.format(serial_no, maker, model, year, color, vehicleType))

        addOwner = True
        while addOwner:
                # need to check here if the vehicle already has a primary owner
                Primary_Ownership = input("Is this person the primary owner of the vehicle? (y/n): ")
                # check for valid input of y or n, also in SQL is it upper or lower y/n?
                Owner = input("Enter the owner id of the owner of the vehicle: ")

                string = "SELECT o.owner_id FROM owner o WHERE o.owner_id = {:s}".format(Owner)
                if len(sql.exeAndFetch(string)) == 0:  # check a person exists with that SIN, if not add them
                        Sin = input("Enter the sin of the owner: ")
                        Name = input("Enter the name of the owner: ")
                        Height = eval(input("Enter the height of the owner: "))
                        Weight = eval(input("Enter the weight of the owner: "))
                        Eyecolor = input("Enter the eye color of the owner: ")
                        Haircolor = input("Enter the hair color of the owner: ")
                        Address = input("Enter the address of the owner: ")
                        Gender = input("Enter the gender of the owner: ")
                        Birthday = input("Enter the birthday of the owner in form 'YYYY-MM-DD': ")
                        string = "Insert into people values ('{:s}','{:s}',{:d},{:d},'{:s}','{:s}','{:s}','{:s}',TO_DATE('{:s}', 'YYYY-MM-DD'))"
                        sql.execute(string.format(Sin,Name,Height,Weight,Eyecolor,Haircolor,Address,Gender,Birthday))

                string = "insert into owner values ('{:s}','{:s}','{:s}')"
                string = string.format(Owner, serial_no, Primary_Ownership)
                sql.execute(string)

                while True:
                        addMore = input("Add another owner? (y/n): ")
                        if addMore.lower() == 'y':
                                addOwner = True
                                break
                        elif addMore.lower() =='n':
                                addOwner = False
                                break
                        else:
                                print("Invalid input, please enter either the letter y or n")

def autoTrans(sql):
	Vehicle = input("Enter the serial_no of the vehicle in the auto transaction: ")
	Buyer = input("Enter the sin of the buyer: ")
	## Second_Buyer = input("Would you like to enter a second Buyer? (y/n) : ")  # ask for more buyers? & which is primary owner?
	Seller = input("Enter the sin of the seller: ")
	Date = input("Enter the date of the transaction 'YYYY-MM-DD': ")
	Price = input("Enter the price the vehicle was sold for ($): ")

	string = "SELECT MAX(transaction_id) FROM auto_sale s"
	TransactionId = sql.exeAndFetch(string)[0][0] + 1

	string = "insert into auto_sale values({:d},'{:s}','{:s}','{:s}',TO_DATE('{:s}', 'YYYY-MM-DD'), '{:s}')"
	string = string.format(TransactionId, Seller, Buyer, Vehicle, Date, Price)
	print(string)
	sql.execute(string)
#This line crashes
	string = "insert into owner values('{:s}','{:s}','{:s}')".format(Buyer,Vehicle, 'y')
	sql.execute(string)
	string = "delete from owner where (owner_id = {:s} and vehicle_id = {:s})"
	string = string.format(Seller, Vehicle)
	print(string)
	sql.execute(string)
#Method 1
	string = "insert into owner values('{:s}','{:s}','{:s}')"
	string = string.format(Buyer, Vehicle, 'Y')
	sql.execute(string)
	sql.execute(string)
	return

def licenceReg(sql):
	string = "SELECT MAX(licence_no) FROM drive_licence"
	print (string)
	Licence_no = int(sql.exeAndFetch(string)[0][0]) + 1
	print(Licence_no)

	Person = input("Enter the sin of the person: ")
	Class = input("Enter the class of driving licence of the person: ")
	Issuing_date = input("Enter the date of issue: ")
	Expiry_date = input("Enter the date of expiry: ")
	File_name = input("Enter the name of the picture file to be added: ")
# From http://stackoverflow.com/questions/4664343/open-file-in-python-and-read-bytes 18/03/15
	#Picture = open(File_name, "rb")
	#Picture = Picture.read(16)
	#print "%s" % (binascii.hexlify(Picture))
	Picture = 0xFF
	string = "insert into drive_licence values ({:d},'{:s}','{:s}', '{:d}', TO_DATE('{:s}', 'YYYY-MM-DD'), TO_DATE('{:s}', 'YYYY-MM-DD'))"
	string = string.format(Licence_no,Person,Class,Picture,Issuing_date,Expiry_date)
	sql.execute(string)
	return

#This component is used by the police officer to issue a traffic ticket and record the violation
#You may also assume that all the information about ticket type is pre-loaded into the system
def violationRec(sql):
        ticket_no = 1 + sql.exeAndFetch("Select Max(t.ticket_no) From ticket t")[0][0]  # create a unique ticket so sql doen't complain
        violator = input("Enter the sin of the violator: ")
        vehicle = input("Enter the serial number of the vehicle : ")
        office = input("Enter the office number: ")
        typeTicket = input("Enter the type of ticket: ")
        date = input("Enter the date of the violation(YYYY-MM-DD): ")
        place = input("Enter the location of the infraction: ")
        descr = input("Enter a detailed description of the offence: ")

        #This simply inserts the ticket into our database
        string = "insert into ticket values({:d},'{:s}','{:s}','{:s}','{:s}',TO_DATE('{:s}', 'YYYY-MM-DD'),'{:s}','{:s}')"
        string = string.format(ticket_no,violator,vehicle,office,typeTicket,date,place,descr)
        print(string)  # debugging
        sql.execute(string)

def searchEngine(sql):
	return

main()  # run the main function
