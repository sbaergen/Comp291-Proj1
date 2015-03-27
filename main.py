import sys
import getpass
import sql as sqlFile

# This will display the menu and handle input to the menu
# after creating/population tables.
def main():
        print("Please login before proceeding.")
        sql = None
        while(True):
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

        # Waring if no arguments are used
        if(len(sys.argv) <= 2):
                print("Waring: Not all arguents are being used!")
                print("First argument creates tables.")
                print("Second argument populates the data with insert statements.")

        # Drop & Create Tables
        if(len(sys.argv) >= 2):
                print("Dropping / Creating Tables")
                print("Using the argument " + str(sys.argv[1]))
                sql.executeFromFile(str(sys.argv[1]))

        # Populate tables
        if(len(sys.argv) >= 3):
                print("Populate Tables")
                print("Using the argument " + str(sys.argv[2]))
                sql.executeFromFile(str(sys.argv[2]))

        print("")  # put some space between info above and start of menu
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

                choice = sqlFile.getNumber("Choice (1-6): ",1,1, 6, 1)

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
                        print ("Invalid Input!")

        sql.close()  # clean up sql object


# Register new vehicle by officer. All detailed information about the vehicle and personal information about the owner.
# You may assume all vehicle types have been loaded into the inital database.
# Create a new vehicle and select owner, if no owner exists create a new person.
# It will ensure all input is valid and all essential input is not null.
def newVehicle(sql):
        serial_no = None
        while True:
                serial_no = sqlFile.getString("Enter serial_no of vehicle: ",15,1)#char (15)
                if unique(sql, "vehicle v", "v.serial_no = '{:s}'".format(serial_no)):
                        break
                else:
                        print("Error: Vehicle already exists!")
                        choice = sqlFile.getString("Try again? (y/n): ",1,1,"ynYN").lower()
                        if choice == 'n':
                                return None
        maker = sqlFile.getString("Enter the make of the vehicle: ",20) #varchar (20)
        model = sqlFile.getString("Enter the model of the vehicle: ",20) #varchar (20)
        year = sqlFile.getNumber("Enter the year of the vehicle: ",4,4) #number (4,0)
        color = sqlFile.getString("Enter the color of the vehicle: ",10) #varchar(10)
        vehicleType = None
        while True:
                vehicleType = sqlFile.getNumber("Enter the integer type of the vehicle: ")#integer
                if unique(sql, "vehicle_type v", "v.type_id = {:d}".format(vehicleType)):
                        print ("Invalid Vehicle Type!")
                else:
                        break
        string = "insert into vehicle values('{:s}','{:s}','{:s}',{:d},'{:s}',{:d})"
        sql.execute(string.format(serial_no, maker, model, year, color, vehicleType))
        primaryDone = False
        addOwner = True
        while addOwner:
                if not primaryDone:
                        Primary_Ownership = sqlFile.getString("Is this person the primary owner of the vehicle? (y/n): ",1,1,'ynYN').lower()#char(1)
                        if Primary_Ownership.lower() == 'y':
                                primaryDone = True
                else:
                        Primary_Ownership = 'n'
                
                Owner = sqlFile.getString("Enter the owner id of the owner of the vehicle: ",15, 1) #char(15)
                
                if unique(sql, "people p", "p.sin = {:s}".format(Owner)):
                        newPerson(sql, Owner)

                string = "insert into owner values ('{:s}','{:s}','{:s}')"
                string = string.format(Owner, serial_no, Primary_Ownership)
                sql.execute(string)

                while True:
                        addMore = sqlFile.getString("Add another owner? (y/n): ",1,1,"ynYN").lower()
                        if addMore == 'y':
                                addOwner = True
                                break
                        else:
                                if primaryDone == True:
                                        addOwner = False
                                        break
                                else:
                                        print("Error: Need to enter a primary owner!")
                                        addOwner = True
                                        break

        print("New Vehicle Registered!")
        print("\n")


# autoTrans will insert a auto transaction into the database. Before this, the function ensures
# that all necessary foreign-keys are present in the data. For example, if a seller is inputed 
# that does not own the inputted vehicle, an error is displayed. Furthermore, if a buyer is inputed
# that is not in the database, the buyer is added if desired
def autoTrans(sql):
        Vehicle = None
        while(True):
                Vehicle = sqlFile.getString("Enter the serial_no of the vehicle in the auto transaction: ",15)#char(15)
                if not (unique(sql, "vehicle", "serial_no = '{:s}'".format(Vehicle))):
                        break
                else:
                        tryAgain = sqlFile.getString("Warning vehicle doen't exist! Try again? (y/n): ", 1, 1, "ynYN").lower()
                        if(tryAgain.lower() == "n"):
                                return None
        Seller = None
        while(True):
                Seller = sqlFile.getString("Enter the sin of the seller: ",15, 1) #char(15)
                if not (unique(sql, "owner", "owner_id = '{:s}' and vehicle_id = '{:s}'".format(Seller, Vehicle))):
                        break
                else:
                        tryAgain = sqlFile.getString("Warning seller doesn't exist! Try again? (y/n): ", 1, 1, "ynYN").lower()
                        if(tryAgain.lower() == "n"):
                                return None
        Date = sqlFile.getDate("Enter the date of the transaction 'YYYY-MM-DD': ") #date
        Price = sqlFile.getNumber("Enter the price the vehicle was sold for ($): ",9,0) #numeric(9,2)

        string = "SELECT MAX(transaction_id) FROM auto_sale s"
        TransactionId = sql.exeAndFetch(string)[0][0] + 1  # (int if nessesary)

        string = "delete from owner where (vehicle_id = '{:s}')"
        sql.execute(string.format(Vehicle))

        primaryExists = False
        buyerNum = sqlFile.getNumber("Enter the number of buyers: ", minValue = 1)
        for x in range(buyerNum):
                Buyer = None
                while(True):
                        Buyer = sqlFile.getString("Enter the sin of the buyer: ",15,1)
                        if not (unique(sql, "people", "sin = '{:s}'".format(Buyer))):
                                break
                        else:
                                tryAgain = sqlFile.getString("Warning buyer doesn't exist! Create a new person? (y/n): ", 1, 1, "ynYN").lower()
                                if(tryAgain.lower() == "y"):
                                        newPerson(sql, Buyer)
                                        break
                                else:
                                        tryAgain = sqlFile.getString("Do you want to quit? (y/n): ", 1, 1, "ynYN").lower()
                                        if(tryAgain.lower() == "y"):
                                                return None
                primary = None
                if (x == buyerNum - 1) and (not primaryExists):
                        print("Automatically setting this to be the primary owner.")
                        primary = 'y'
                elif not primaryExists:
                        primary = sqlFile.getString("Is this owner the primary owner? ",1,1,'ynYN').lower()
                else:
                        primary = 'n'
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

        print("Auto Transaction Completed!")
        print("\n")


# licenceReg creates a new licence in the database if the person inputted does
# not already have a licence. It ensures all necessary input is not Null and
# dependencies hold.
def licenceReg(sql):
        string = "SELECT MAX(licence_no) FROM drive_licence"
        Licence_no = eval(sql.exeAndFetch(string)[0][0]) + 1 #char(15)
        Person = None
        while True:
                Person = sqlFile.getString("Enter the sin of the person: ",15,1) #char(15)
                if not unique(sql,"drive_licence d", "d.sin = '{:s}'".format(Person)):
                        print("Person already has a licence")
                        choice = sqlFile.getString("Try again? (y/n): ",1,1,"ynYN").lower()
                        if choice == 'n':
                                return None
                elif unique(sql, "people p", "p.sin = '{:s}'".format(Person)):
                        print("Person not found, adding person")
                        newPerson(sql,Person)
                        break
                else:
                        break
        Class = sqlFile.getString("Enter the class of driving licence of the person: ",10) #varchar(10)
        Issuing_date = sqlFile.getDate("Enter the date of issue 'YYYY-MM-DD': ") #date
        Expiry_date = sqlFile.getDate("Enter the date of expiry 'YYYY-MM-DD': ") #date
        Picture = sqlFile.getPic("Enter the path to the picture: ")

        string = "insert into drive_licence (licence_no, sin, class, photo, issuing_date, expiring_date) values (:lno, :sin, :class, :pic, TO_DATE(:issue, 'YYYY-MM-DD'), TO_DATE(:exp, 'YYYY-MM-DD'))"
        sql.execute(string, {'lno':Licence_no, 'sin':Person, 'class':Class, 'pic':Picture, 'issue':Issuing_date, 'exp':Expiry_date})

        print("Licence Registered!")
        print("\n")

#This component is used by the police officer to issue a traffic ticket and record the violation
#You may also assume that all the information about ticket type is pre-loaded into the system
def violationRec(sql):
        ticket_no = sql.exeAndFetch("Select Max(t.ticket_no) From ticket t")[0][0]  + 1 #int
        while True:
                violator = sqlFile.getString("Enter the sin of the violator: ",15) #char(15)
                if unique(sql,"people p", "p.sin = '{:s}'".format(violator)):
                        print("Violator does not exist")
                        choice = sqlFile.getString("Try again? (y/n): ",1,1,"ynYN").lower()
                        if choice == 'n':
                                return None
                else:
                        break

        while True:
                vehicle = sqlFile.getString("Enter the serial number of the vehicle: ",15) #char(15)
                if unique(sql,"vehicle v", "v.serial_no = '{:s}'".format(vehicle)):
                        print("Vehicle does not exist")
                        choice = sqlFile.getString("Enter new serial_no? (y/n): ",1,1,"ynYN").lower()
                        if choice == 'n':
                                return None
                else:
                        break

        while True:
                officer = sqlFile.getString("Enter the officer number: ",15) #char(15)
                if unique(sql,"people p", "p.sin = '{:s}'".format(officer)):
                        print("Officer does not exist")
                        choice = sqlFile.getString("Try again? (y/n): ",1,1,"ynYN").lower()
                        if choice == 'n':
                                return None
                else:
                        break

        while True:
                typeTicket = sqlFile.getString("Enter the type of ticket: ",10) #char 10
                if unique(sql,"ticket_type t","vtype = '{:s}'".format(typeTicket)):
                        print("Invalid ticket type")
                        choice = sqlFile.getString("Try again? (y/n): ",1,1,"ynYN").lower()
                        if choice == 'n':
                                return None
                else:
                        break

        date = sqlFile.getDate("Enter the date of the violation(YYYY-MM-DD): ") #date
        place = sqlFile.getString("Enter the location of the infraction: ",20) # varchar(20)
        descr = sqlFile.getString("Enter a detailed description of the offence: ",1024) #varchar(1024)

        #This simply inserts the ticket into our database
        string = "insert into ticket values({:d},'{:s}','{:s}','{:s}','{:s}',TO_DATE('{:s}', 'YYYY-MM-DD'),'{:s}','{:s}')"
        string = string.format(ticket_no,violator,vehicle,officer,typeTicket,date,place,descr)
        sql.execute(string)

        print("Violation Recorded!")
        print("\n")

#This component is used to allow the user to select a search type
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
                if len(Results) == 0:
                        print("\n")
                        print("Licence not found")
                        print("\n")
                        return None
        else:
                name = sqlFile.getString("Enter a name or press enter to choose a new search: ",40)
        if name != None and len(licence_no) == 0:
                string = "SELECT p.name, d.licence_no, p.addr, p.birthday, d.class, r.r_id, d.expiring_date FROM people p, drive_licence d, restriction r WHERE p.name = '{:s}' and p.sin = d.sin and d.licence_no = r.licence_no"
                Results = (sql.exeAndFetch(string.format(name)))

        print("\n")
        if len(Results) == 0:
                print("No person found")
                print("\n")
                return None

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

        return None


def search2(sql):
        print("Personal Violation Record\n")
        assertion1 = ''
        assertion2 = ''
        licence_no = sqlFile.getString("Enter a licence number or press enter to input a sin: ",15)
        string1 = "SELECT d.licence_no FROM drive_licence d WHERE d.licence_no = '{:s}'"
        if len(licence_no) != 0:
                assertion1 = (sql.exeAndFetch(string1.format(licence_no)))
          #ticket given the sin of the person or their drivers licence number
          #This also checks to make sure that the sin or licence number are valid and 
          #do exist in the given data, running an appropriate error otherwise
                string3 = "SELECT t.ticket_no, t.violator_no, t.vehicle_id, t.office_no, t.vtype, t.vdate, t.place, t.descriptions FROM ticket t, drive_licence d WHERE d.licence_no = '{:s}' and d.sin = t.violator_no"
                Results = (sql.exeAndFetch(string3.format(licence_no)))
                sin = None
                if len(assertion1) == 0:
                        print("\n")
                        print("Licence not found")
                        print("\n")
                        return None
        else:
                sin = sqlFile.getString("Enter a sin or press enter to choose a new search: ",15)

        string2 = "SELECT d.sin FROM drive_licence d WHERE d.sin = '{:s}'"

        if sin != None  and len(licence_no) == 0:
                assertion2 = (sql.exeAndFetch(string2.format(sin)))
                string4 = "SELECT t.ticket_no, t.violator_no, t.vehicle_id, t.office_no, t.vtype, t.vdate, t.place, t.descriptions FROM ticket t WHERE t.violator_no = '{:s}'"
                Results = (sql.exeAndFetch(string4.format(sin)))

                if len(assertion2) == 0:
                        print("\n")
                        print("Person does not exist")
                        print("\n")
                        return None
        #Displays a separate result if the person is found but they have no tickets registered
        if len(Results) == 0:
                print("No tickets found")
                print("\n")
                return None

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
        return None

def search3(sql):
        print("\n")
        print("Vehicle History\n")
        serial_no = sqlFile.getString("Enter a serial_no or press Enter to choose a new search type: ",15)
        string = "SELECT v.serial_no FROM vehicle v WHERE v.serial_no = '{:s}'"
        assertion = (sql.exeAndFetch(string.format(serial_no)))
        if len(assertion) == 0:
                print("\n")
                print("No vehicle found!")
                print("\n")
                return None
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
        return None

#Allows the input and addition of a complete person into the database
#Nessesary to remove the bulk from the program and save time and space
def newPerson(sql, Sin=None):
        if Sin is None:
                #Asserts that the new person to be added does not already exist
                isUnique = False
                while not isUnique:
                        Sin = sqlFile.getString("Enter the sin of the person:",15) #char(15)
                        isUnique = unique(sql, "People p", "p.sin = '{:s}'".format(Sin))
                        if not isUnique:
                                print("Person already exists!")
        Name = sqlFile.getString("Enter the name of the person: ",40) #varchar(40)
        Height = sqlFile.getNumber("Enter the height of the person: ",None,0,999.99) #number(5,2)
        Weight = sqlFile.getNumber("Enter the weight of the person: ",None,0,1000) #number(5,2)
        Eyecolor = sqlFile.getString("Enter the eye color of the person: ",10) #varchar(10)
        Haircolor = sqlFile.getString("Enter the hair color of the person: ",10) #varchar(10)
        Address = sqlFile.getString("Enter the address of the person: ",50) #varchar2(50)
        Gender = sqlFile.getString("Enter the gender of the person (m or f): ",1,1,'mfMF').lower() #char
        Birthday =sqlFile.getDate("Enter the birthday of the person in form 'YYYY-MM-DD': ") #date

        string = "Insert into people values ('{:s}','{:s}',{:.2f},{:.2f},'{:s}','{:s}','{:s}','{:s}',TO_DATE('{:s}', 'YYYY-MM-DD'))"
        sql.execute(string.format(Sin,Name,Height,Weight,Eyecolor,Haircolor,Address,Gender,Birthday))
        print("Person Added!")
        print("\n")

#Creates a sql with gereal string slicing and formatting to remove a large amount
#of bulk from the program and increase readability. 
def unique(sql, table, conditionMessage):
        string = "SELECT * FROM {:s} WHERE {:s}"
        result = sql.exeAndFetch(string.format(table, conditionMessage))
        if not len(result):
                return True
        else:
                return False

main()  # run the main function
