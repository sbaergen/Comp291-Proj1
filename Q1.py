#Register new vehicle by officer. All detailed information about the vehicle and personal information about the owner. 
#You may assume all vehicle types have been loaded into the inital database.
print("NEW VEHICLE REGISTRATION")
print("")
Serial_no = input("Enter serial_no of vehicle: ")
Maker = input("Enter the make of the vehicle: ")
Model = input("Enter the model of the vehicle: ")
Year = input("Enter the year of the vehicle: ")
Color = input("Enter the color of the vehicle: ")
Type = input("Enter the type of the vehicle (1=car,2=suv,3=crossover,4=van,5=truck): ")
Insert into vehicle values(Serial_no,Maker,Model,Year,Color,Type)

Continue = True
While Continue:
    Owner = input("Enter the owner id of the owner of the vehicle: ")
    if empty Query(SELECT o.owner_id FROM owner o, vehicle v WHERE o.owner_id = Owner and o.vehicle_id = Serial_no;):
        Primary_Ownership = input("Is this person the primary owner of the vehicle? (y/n): ")
        Insert into owner values(Owner,Serial_no,Primary_Ownership);

    if empty Query(Select * FROM person p WHERE p.sin = Owner):
        Sin = input("Enter the sin of the owner: ")
        Name = input("Enter the name of the owner: ")
        Height = input("Enter the height of the owner: ")
        Weight = input("Enter the weight of the owner: ")
        Eyecolor = input("Enter the eye color of the owner: ")
        Haircolor = input("Enter the hair color of the owner: ")
        Address = input("Enter the address of the owner: ")
        Gender = input("Enter the gender of the owner: ")
        Birthday = input("Enter the birthday of the owner: ")
        Insert into people values (Sin,Name,Height,Weight,Eyecolor,Haircolor,Address,Gender,Birthday);

    Done = False
    While not Done:
        Continue = input("Add another owner? (y/n): ")
        if Continue == 'y' or Continue == 'Y':
            Continue = True
            Done = True
        elif Continue =='n' or Continue == 'N':
            Continue = False
            Done = True
        else:
            print("Invalid input, please enter either the letter y or n")
        

                              
