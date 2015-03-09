# This is the main menu.
# This will display the menu and handle input to the menu
def newVehicle():
	pass
def autoTrans():
	pass
def licenceReg():
	pass
def violationRec():
	pass
def searchEngine():
	pass

print ("Welcome to the Alberta Auto Registration System!")
choice = 0
while (choice != 6):
	print ("----------------------------------------")
	print ("""Please Select from the following:
	1:New Vehicle Registration
	2:Auto Transaction
	3:Driver Licence Registration
	4:Violation Record
	5:Search Engine
	6:Exit""")
	try:
		choice = input("Choice (1-6): ")
	except SyntaxError:
		choice = 7
	if choice == 1:
		newVehicle()
	elif choice == 2:
		autoTrans()
	elif choice == 3:
		licenceReg()
	elif choice == 4:
		violationRec()
	elif choice == 5:
		searchEngine()
	elif choice == 6:
		break
	else:
		print ("You are an idiot")
	print (choice)

def newVehicle():
	return

def autoTrans():
	return

def licenceReg():
	return

def violationRec():
	return

def searchEngine():
	return
