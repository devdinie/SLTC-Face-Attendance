import csv

with open ('input.csv', 'w+') as file:
    myfile = csv.writer(file)
    myfile.writerow(["Id", "Name"])
    actID= input("enter ID")
    Name = input("enter Name")
    myfile.writerow([actID, Name])


