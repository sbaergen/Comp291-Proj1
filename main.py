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

        # the test worked here.. now for auto transaction
        # print("teting delete here:")
        # sql.execute("delete from owner where (owner_id = '121121121' and vehicle_id = '1020')")

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
        Price = eval(input("Enter the price the vehicle was sold for ($): "))

        string = "SELECT MAX(transaction_id) FROM auto_sale s"
        TransactionId = sql.exeAndFetch(string)[0][0] + 1  # new transaction id is unique now

        string = "delete from owner where (owner_id = '{:s}' and vehicle_id = '{:s}')"
        string = string.format(Seller, Vehicle)
        sql.execute(string)

        string = "insert into auto_sale values({:d},'{:s}','{:s}','{:s}',TO_DATE('{:s}', 'YYYY-MM-DD'), {:f})"
        string = string.format(TransactionId, Seller, Buyer, Vehicle, Date, Price)
        sql.execute(string)

        string = "insert into owner values('{:s}','{:s}','{:s}')"
        string = string.format(Buyer, Vehicle, 'y')
        sql.execute(string)

# I will add a person with sin = 131131131 to use for tesing w/ this function
def licenceReg(sql):
        string = "SELECT MAX(licence_no) FROM drive_licence"
        print (string + " is now ...")  # debugging
        Licence_no = eval(sql.exeAndFetch(string)[0][0]) + 1
        print(Licence_no)  # debugging

        Person = input("Enter the sin of the person: ")
        Class = input("Enter the class of driving licence of the person: ")
        Issuing_date = input("Enter the date of issue 'YYYY-MM-DD': ")
        Expiry_date = input("Enter the date of expiry 'YYYY-MM-DD': ")
        File_name = input("Enter the path to the picture: ")  # currently not used

        # #Load image into memory from local file
        # #(Assumes a file by this name exists in the directory you are running from)
        f_image  = open('meow.jpg','rb')
        image  = f_image.read()

        # prepare memory for operation parameters
        # cursor.setinputsizes(image=cx_Oracle.BLOB)

        # Housekeeping...
        f_image.close()

# From http://stackoverflow.com/questions/4664343/open-file-in-python-and-read-bytes 18/03/15
        #Picture = open(File_name, "rb")
        #Picture = Picture.read(16)
        #print "%s" % (binascii.hexlify(Picture))
        Picture = image
        curs = sql.getCurs()
        curs = sql.getCurs()
        string = "insert into drive_licence (licence_no, sin, class, photo, issuing_date, expiring_date) values (:lno, :sin, :class, :pic, TO_DATE(:issue, 'YYYY-MM-DD'), TO_DATE(:exp, 'YYYY-MM-DD'))"
        curs.execute(string, {'lno':Licence_no, 'sin':Person, 'class':Class, 'pic':Picture, 'issue':Issuing_date, 'exp':Expiry_date})
        # string = "insert into drive_licence (licence_no, sin, class, photo, issuing_date, expiring_date) values ('{:s}','{:s}','{:s}', '{:s}', TO_DATE('{:s}', 'YYYY-MM-DD'), TO_DATE('{:s}', 'YYYY-MM-DD'))"
        # string = string.format(str(Licence_no),Person,Class,Picture,Issuing_date,Expiry_date)
        # print(len(string))
        # sql.prepImage()
        # print(string)  # debugging
        # sql.execute(string)
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
    print("1.Personal Information Search")
    print("2.Personal Violation Record")
    print("3.Vehicle history")
    print("quit (q)")

    choice = input("Choose a search type number: ")

    while (choice.lower() != 'q'):
	    if choice == '1':
		    search1(sql)
	    elif choice == '2':
		    search2(sql)
	    elif choice == '3':
		    search3(sql)
	    else:
		    print("Invalid input, please enter an integer 1, 2 or 3 or press 'q' to quit")
		    choice = input("Choose a search type number: ")
	    if (choice.lower() != 'q'):
		    choice = input("Choose another search type or press 'q' to quit: ")

def search1(sql):
	licence_no = input("Enter a licence_no or press enter to continue: ")
	print("Personal information search\n")
         #These queries list the Name, licence_no, address, birthday, drivers class restriction_id and
         #licence expiry date of a person given their name or licence_no
         #Allow for duplicate names
         #Not sure whether to present r_id or the actual description of the condition
	if len(licence_no) != 0:
		string = "SELECT p.name, d.licence_no, p.addr, p.birthday, d.class, r.r_id, d.expiring_date FROM people p, drive_licence d, restrIction r WHERE d.licence_no = '{:s}' and p.sin = d.sin and d.licence_no = r.licence_no"  
		Results = (sql.exeAndFetch(string.format(licence_no)))
		name = None
	else:
		name = input("Enter a name or press enter to continue: ")
        
	if name != None and len(licence_no) == 0:
		string = "SELECT p.name, d.licence_no, p.addr, p.birthday, d.class, r.r_id, d.expiring_date FROM people p, drive_licence d, restriction r WHERE p.name = '{:s}' and p.sin = d.sin and d.licence_no = r.licence_no"
		Results = (sql.exeAndFetch(string.format(name)))

	for result in Results:
		print("Name: ", result [0])
		print("Licence_no: ", result[1])
		print("Address: ", result[2])
		print("Birthday: ", result[3])
		print("Driving Class: ", result[4])
		print("Driving Condition: ", result[5])
		print("Expiring Date: ", result[6])
	print("\n")
	return


def search2(sql):
	print("Personal Violation Record\n")
	licence_no = input("Enter a licence number or press enter to continue: ")
	if len(licence_no) != 0:
          #These Queries must list everything from ticket (not sure if t.(*) will select all) from
          #ticket given the sin of the person or their drivers licence number
		string = "SELECT t.ticket_no, t.violator_no, t.vehicle_id, t.office_no, t.vtype, t.vdate, t.place, t.descriptions FROM ticket t, drive_licence d, WHERE d.licence_no = '{:s}' and d.sin = t.violator_no"
		Results = (sql.exeAndFetch(string.format(licence_no)))
		sin = None
	else:
		sin = input("Enter a valid sin or press enter to continue: ")

	if sin != None  and len(licence_no) == 0:
		string = "SELECT t.ticket_no, t.violator_no, t.vehicle_id, t.office_no, t.vtype, t.vdate, t.place, t.descriptions FROM ticket t, drive_licence d WHERE t.violator_no = '{:s}'"
		Results = (sql.exeAndFetch(string.format(sin)))

	for result in Results:
		print("Ticket Number: ", result[0])
		print("Violator Number: ", result[1])
		print("Vehicle Identification: ", result[2])
		print("Office Number: ", result[3])
		print("Ticket Type: ", result[4])
		print("Ticket Date: ", result[5])
		print("Place: ", result[6])
		print("Descriptions: ", result[7])
	print("\n")
	return

def search3(sql):
	print("Vehicle History\n")
	serial_no = input("Enter a serial_no: ")

    #This Query must select the number of times a vehicle has been sold, its average sale price and the number of
    #incidents that it has been involved in given the serial_no of the vehicle
	string = "SELECT COUNT(a.vehicle_id), AVG(a.price), COUNT(t.vehicle_id) FROM auto_sale a, ticket t WHERE a.vehicle_id = serial_no and t.vehicle_id = '{:s}' GROUP BY a.vehicle_id"
	Results = (sql.exeAndFetch(string.format(serial_no)))

	for result in Results:
		print("Amount of Sales: ", result[0])
		print("Average Sale Price: ", result[1])
		print("Amount of Infractions: ", result[2])
	print("\n")
	return

main()  # run the main function
