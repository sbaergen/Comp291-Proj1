import getpass
import sql as sqlFile

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

        # We should ask for a file w/ create table statements

        # Drop & Create Tables
        print("Dropping / Creating Tables")
        sql.executeFromFile("p1_setup.sql.txt")

        # We should ask for a file w/ insert statements

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
                        print("New Vehicle Registration:")
                        newVehicle(sql)
                elif choice == 2:
                        print("Auto Transaction:")
                        autoTrans(sql)
                elif choice == 3:
                        print("Licence Registration:")
                        licenceReg(sql)
                elif choice == 4:
                        print("Violation Record:")
                        violationRec(sql)
                elif choice == 5:
                        print("Search Engine:")
                        searchEngine(sql)
                elif choice == 6:
                        print("Good Bye.")
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
        serial_no = sqlFile.getString("Enter serial_no of vehicle: ",15)#char (15) #unique sql check
        maker = sqlFile.getString("Enter the make of the vehicle: ",20) #varchar (20)
        model = sqlFile.getString("Enter the model of the vehicle: ",20) #varchar (20)
        year = sqlFile.getNumber("Enter the year of the vehicle: ",4,0) #number (4,0)
        color = sqlFile.getString("Enter the color of the vehicle: ",10) #varchar(10)
        # todo vehicleType input, should we be restricting it???
        vehicleType = sqlFile.getNumber("Enter the type of the vehicle (1=car,2=suv,3=crossover,4=van,5=truck): ",1,0,5)#integer

        string = "insert into vehicle values('{:s}','{:s}','{:s}',{:d},'{:s}',{:d})"
        sql.execute(string.format(serial_no, maker, model, year, color, vehicleType))
        primaryDone = False
        addOwner = True
        while addOwner:
                # need to check here if the vehicle already has a primary owner
                if not primaryDone:
                        Primary_Ownership = sqlFile.getString("Is this person the primary owner of the vehicle? (y/n): ",1,0,'yn')#char(1)
                        if Primary_Ownership.lower() == 'y':
                                primaryDone = True
                else:
                        Primary_Ownership = 'n'
                #contains (y or n)
                Owner = sqlFile.getString("Enter the owner id of the owner of the vehicle: ",15) #char(15)
                #UNIQUE SQL OWNER, VEHICLE_ID (serial_no)

                string = "SELECT o.owner_id FROM owner o WHERE o.owner_id = {:s}".format(Owner)
                if len(sql.exeAndFetch(string)) == 0:  # check a person exists with that SIN, if not add them
                        newPerson(sql, Owner)

                string = "insert into owner values ('{:s}','{:s}','{:s}')"
                string = string.format(Owner, serial_no, Primary_Ownership)
                sql.execute(string)

                while True:
                        addMore = input("Add another owner? (y/n): ")
                        if addMore.lower() == 'y':
                                addOwner = True
                                break
                        elif addMore.lower() =='n':
                                if primaryDone == True:
                                        addOwner = False
                                        break
                                else:
                                        print("Error: Need to enter a primary owner!")
                                        addOwner = True
                        else:
                                print("Invalid input, please enter either the letter y or n")

def autoTrans(sql):
        Vehicle = input("Enter the serial_no of the vehicle in the auto transaction: ")#char(15)
        Seller = sqlFile.getString("Enter the sin of the seller: ",15) #char(15)
        Date = sqlFile.getDate("Enter the date of the transaction 'YYYY-MM-DD': ") #date
        Price = sqlFile.getNumber("Enter the price the vehicle was sold for ($): ",9,0) #numeric(9,2)

        string = "SELECT MAX(transaction_id) FROM auto_sale s"
        TransactionId = sql.exeAndFetch(string)[0][0] + 1  # (int if nessesary)

        string = "delete from owner where (vehicle_id = '{:s}')"
        sql.execute(string.format(Vehicle))

        primaryExists = False
        buyerNum = sqlFile.getNumber("Enter the number of buyers: ")
        for _ in range(buyerNum):
                Buyer = sqlFile.getString("Enter the sin of the buyer: ",15)
                primary = sqlFile.getString("Is this owner the primary owner? ",1,1,'yn')
                if primary.lower() == 'y':
                         string = "insert into auto_sale values({:d},'{:s}','{:s}','{:s}',TO_DATE('{:s}', 'YYYY-MM-DD'), {:.2f})"
                         string = string.format(TransactionId, Seller, Buyer, Vehicle, Date, Price)
                         sql.execute(string)
                         primaryExists = True
                         string = "insert into owner values('{:s}','{:s}','{:s}')"
                         string = string.format(Buyer, Vehicle, 'y')
                         sql.execute(string)
                elif primary.lower() == 'n':
                         string = "insert into owner values('{:s}','{:s}','{:s}')"
                         string = string.format(Buyer, Vehicle, 'n')
                         sql.execute(string)
def licenceReg(sql):
        string = "SELECT MAX(licence_no) FROM drive_licence"
        Licence_no = eval(sql.exeAndFetch(string)[0][0]) + 1 #char(15) (if nessesary)

        Person = sqlFile.getString("Enter the sin of the person: ",15) #char(15)
        Class = sqlFile.getString("Enter the class of driving licence of the person: ",10) #varchar(10)
        Issuing_date = sqlFile.getDate("Enter the date of issue 'YYYY-MM-DD': ") #date
        Expiry_date = sqlFile.getDate("Enter the date of expiry 'YYYY-MM-DD': ") #date
        # File_name = getPic("Enter the path to the picture: ") #blob
        Picture = sqlFile.getPic("Enter the path to the picture: ")

        # prepare memory for operation parameters  # i found I didn't need to do this!
        # cursor.setinputsizes(image=cx_Oracle.BLOB)

        string = "insert into drive_licence (licence_no, sin, class, photo, issuing_date, expiring_date) values (:lno, :sin, :class, :pic, TO_DATE(:issue, 'YYYY-MM-DD'), TO_DATE(:exp, 'YYYY-MM-DD'))"
        sql.execute(string, {'lno':Licence_no, 'sin':Person, 'class':Class, 'pic':Picture, 'issue':Issuing_date, 'exp':Expiry_date})

#This component is used by the police officer to issue a traffic ticket and record the violation
#You may also assume that all the information about ticket type is pre-loaded into the system
def violationRec(sql):
        ticket_no = sql.exeAndFetch("Select Max(t.ticket_no) From ticket t")[0][0]  + 1 #int (if neccesary)
        violator = sqlFile.getString("Enter the sin of the violator: ",15) #char(15)
        vehicle = sqlFile.getString("Enter the serial number of the vehicle: ",15) #char(15)
        office = sqlFile.getString("Enter the office number: ",15) #char(15)
        typeTicket = sqlFile.getString("Enter the type of ticket: ",10) #char 10 #check in other type

        date = sqlFile.getDate("Enter the date of the violation(YYYY-MM-DD): ") #date
        place = sqlFile.getString("Enter the location of the infraction: ",20) # varchar(20)
        descr = sqlFile.getString("Enter a detailed description of the offence: ",1024) #varchar(1024)

        #This simply inserts the ticket into our database
        string = "insert into ticket values({:d},'{:s}','{:s}','{:s}','{:s}',TO_DATE('{:s}', 'YYYY-MM-DD'),'{:s}','{:s}')"
        string = string.format(ticket_no,violator,vehicle,office,typeTicket,date,place,descr)
        sql.execute(string)

def searchEngine(sql):
    print("1.Personal Information Search")
    print("2.Personal Violation Record")
    print("3.Vehicle history")
    print("quit (q)")
    choice = '0'
    invalid = False

    while (choice.lower() != 'q'):
            if invalid == False:
                    choice = input("Choose a search type or press 'q' to quit: ")
            else:
                    invalid = False

            if choice == '1':
                    search1(sql)
            elif choice == '2':
                    search2(sql)
            elif choice == '3':
                    search3(sql)
            else:
                    if choice.lower() != 'q':
                            print("Invalid input, please enter an integer 1, 2 or 3 or press 'q' to quit")
                            choice = input("Choose a valid search type or press 'q' to quit: ")
                            invalid = True

def search1(sql):
	print("\n")
	print("Personal information search\n")
	licence_no = sqlFile.getString("Enter a licence_no or press enter to input a name: ",15)

         #These queries list the Name, licence_no, address, birthday, drivers class restriction_id and
         #licence expiry date of a person given their name or licence_no
         #Allow for duplicate names
         #Not sure whether to present r_id or the actual description of the condition
	if len(licence_no) != 0:
		string = "SELECT p.name, d.licence_no, p.addr, p.birthday, d.class, r.r_id, d.expiring_date FROM people p, drive_licence d, restrIction r WHERE d.licence_no = '{:s}' and p.sin = d.sin and d.licence_no = r.licence_no"
		Results = (sql.exeAndFetch(string.format(licence_no)))
		name = None
	else:
		name = sqlFile.getString("Enter a name or press enter to choose a new search: ",40)
	if name != None and len(licence_no) == 0:
		string = "SELECT p.name, d.licence_no, p.addr, p.birthday, d.class, r.r_id, d.expiring_date FROM people p, drive_licence d, restriction r WHERE p.name = '{:s}' and p.sin = d.sin and d.licence_no = r.licence_no"
		Results = (sql.exeAndFetch(string.format(name)))

	print("\n")
	if len(Results) == 0:
		print("No person found")
		print("\n")
		return

	for result in Results:
		print("Name: ", result [0])
		print("Licence_no: ", result[1])
		print("Address: ", result[2])
		print("Birthday: ", result[3])
		print("Driving Class: ", result[4])
		print("Driving Condition: ", result[5])
		print("Expiring Date: ", result[6])
		print("\n")
	print("\n")

	return


def search2(sql):
	print("\n")
	print("Personal Violation Record\n")
	assertion1 = []
	assertion2 = []
	licence_no = sqlFile.getString("Enter a licence number or press enter to input a sin: ",15)
	string1 = "SELECT d.licence_no FROM drive_licence d WHERE d.licence_no = '{:s}'"
	if len(licence_no) != 0:
		assertion1 = (sql.exeAndFetch(string1.format(licence_no)))
          #ticket given the sin of the person or their drivers licence number
		string3 = "SELECT t.ticket_no, t.violator_no, t.vehicle_id, t.office_no, t.vtype, t.vdate, t.place, t.descriptions FROM ticket t, drive_licence d WHERE d.licence_no = '{:s}' and d.sin = t.violator_no"
		Results = (sql.exeAndFetch(string3.format(licence_no)))
		sin = None
	else:
		sin = sqlFile.getString("Enter a sin or press enter to choose a new search: ",15)

	string2 = "SELECT d.licence_no FROM drive_licence d WHERE d.licence_no = '{:s}'"

	if sin != None  and len(licence_no) == 0:
		assertion2 = (sql.exeAndFetch(string2.format(sin)))
		string4 = "SELECT t.ticket_no, t.violator_no, t.vehicle_id, t.office_no, t.vtype, t.vdate, t.place, t.descriptions FROM ticket t WHERE t.violator_no = '{:s}'"
		Results = (sql.exeAndFetch(string4.format(sin)))

	if len(assertion1) == 0 and len(assertion2) == 0:
		print("Person does not exist")
		print("\n")
		return

	print("\n")
	if len(Results) == 0:
		print("No tickets found")
		print("\n")
		return

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
	print("\n")
	return

def search3(sql):
	print("\n")
	print("Vehicle History\n")
	serial_no = sqlFile.getString("Enter a serial_no or press Enter to choose a new search type: ",15)
	string = "SELECT v.serial_no FROM vehicle v WHERE v.serial_no = '{:s}'"
	assertion = (sql.exeAndFetch(string.format(serial_no)))
	if len(assertion == 0):
		print("No vehicle found!")
		return
    #This Query must select the number of times a vehicle has been sold, its average sale price and the number of
    #incidents that it has been involved in given the serial_no of the vehicle
	string = "SELECT COUNT(a.vehicle_id), AVG(a.price) FROM auto_sale a WHERE a.vehicle_id = '{:s}'"
	Results1 = (sql.exeAndFetch(string.format(serial_no)))

	string = "SELECT COUNT(t.vehicle_id) FROM ticket t WHERE  t.vehicle_id = '{:s}'"
	Results2 = (sql.exeAndFetch(string.format(serial_no)))

	print("\n")
	for result1 in Results1:
		for result2 in Results2:
			print("Amount of Sales: ", result1[0])
			print("Average Sale Price: ", result1[1])
			print("Amount of Infractions: ", result2[0])
	print("\n")
	return

def newPerson(sql, Sin=None):
        if Sin is None:
                Sin = sqlFile.getString("Enter the sin of the person:",15) #char(15)
        Name = sqlFile.getString("Enter the name of the owner: ",40) #varchar(40)
        Height = sqlFile.getNumber("Enter the height of the owner: ",5) #number(5,2)
        Weight = sqlFile.getNumber("Enter the weight of the owner: ",5) #number(5,2)
        Eyecolor = sqlFile.getString("Enter the eye color of the owner: ",10) #varchar(10)
        Haircolor = sqlFile.getString("Enter the hair color of the owner: ",10) #varchar(10)
        Address = sqlFile.getString("Enter the address of the owner: ",50) #varchar2(50)
        Gender = sqlFile.getString("Enter the gender of the owner (m or f): ",1,0,'mf') #char #contains (m or f)
        Birthday =sqlFile.getDate("Enter the birthday of the owner in form 'YYYY-MM-DD': ") #date

        string = "Insert into people values ('{:s}','{:s}',{:d},{:d},'{:s}','{:s}','{:s}','{:s}',TO_DATE('{:s}', 'YYYY-MM-DD'))"
        sql.execute(string.format(Sin,Name,Height,Weight,Eyecolor,Haircolor,Address,Gender,Birthday))

main()  # run the main function
