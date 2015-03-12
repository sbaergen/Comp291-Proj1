import getpass
import sql as sqlFile

# This will display the menu and handle input to the menu
def main():
	print("Please login before proceeding.")
	user = input("User [%s]:" % getpass.getuser())
	if not user:
		user = getpass.getuser()
	passw = getpass.getpass("Pass:")

	# create a new instance of a connection object
	sql = sqlFile.SqlConnection(user, passw)

	# Drop & Create Tables
	print("Dropping / Creating Tables")
	sql.exicuteFromFile("p1_setup.sql.txt")

	# Populate tables
	print("Populate Tables")
	sql.exicuteFromFile("population.txt")

	print ("Welcome to the Alberta Auto Registration System!")
	choice = 7
	while (choice != 6):
		print ("----------------------------------------")
		print ("""Please Select from the following:
		1:New Vehicle Registration
		2:Auto Transaction
		3:Driver Licence Registration
		4:Violation Record
		5:Search Engine
		6:Exit""")
		choice = 7
		while (choice == 7):
			try:
				choice = eval(input("Choice (1-6): "))
				if (not (choice >= 1 and choice <=6)):
					choice = 7  # Will cause a loop back to get new entry (choice was invalid)
					print ("Invalid Input!", end = " ")
			except:
				choice = 7  # Will cause a loop back to get new entry (choice was invalid)
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
			choice = 7  # Will cause a loop back to get new entry (choice was invalid)
			print ("Invalid Input!", end = " ")
		print (choice)

	sql.close()  # clean up sql object



#Register new vehicle by officer. All detailed information about the vehicle and personal information about the owner. 
#You may assume all vehicle types have been loaded into the inital database.
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
	string = "insert into vehicle values ('{:s}','{:s}','{:s}','{:s}','{:s}',{:d})".format(serial_no, maker, model, year, color, vehicleType)
	print("debugging: " + string)
	sql.exicute(string)

	return
#
#	Continue = True
#	While Continue:
#	Owner = input("Enter the owner id of the owner of the vehicle: ")
#	if empty Query(SELECT o.owner_id FROM owner o, vehicle v WHERE o.owner_id = Owner and o.vehicle_id = Serial_no;):
#		Primary_Ownership = input("Is this person the primary owner of the vehicle? (y/n): ")
#		Insert into owner values(Owner,Serial_no,Primary_Ownership);
#
#		if empty Query(Select * FROM person p WHERE p.sin = Owner):
#			Sin = input("Enter the sin of the owner: ")
#			Name = input("Enter the name of the owner: ")
#			Height = input("Enter the height of the owner: ")
#			Weight = input("Enter the weight of the owner: ")
#			Eyecolor = input("Enter the eye color of the owner: ")
#			Haircolor = input("Enter the hair color of the owner: ")
#			Address = input("Enter the address of the owner: ")
#			Gender = input("Enter the gender of the owner: ")
#			Birthday = input("Enter the birthday of the owner: ")
#			Insert into people values (Sin,Name,Height,Weight,Eyecolor,Haircolor,Address,Gender,Birthday);
#
#			Done = False
#			While not Done:
#			Continue = input("Add another owner? (y/n): ")
#			if Continue == 'y' or Continue == 'Y':
#			Continue = True
#			Done = True
#			elif Continue =='n' or Continue == 'N':
#			Continue = False
#			Done = True
#			else:
#			print("Invalid input, please enter either the letter y or n")
#	return

def autoTrans(sql):
	return

def licenceReg(sql):
	return

def violationRec(sql):
	return

def searchEngine(sql):
	return

main()  # run the main function
