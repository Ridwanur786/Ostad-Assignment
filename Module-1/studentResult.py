import math

#Student Result management System
studentName = str(input("Enter your Name: "))
studentID = int(input("Enter your Id: "))
department = str(input("Enter your Department name: "))

#Subject marks

subjects =["Python", "Math","English", "Physics", "ICT"]

student_marks = {}

for subject in subjects:
   marks = int(input(f"enter Marks for {subject} :"))
   student_marks[subject] = marks
print("\n")
print("======PRINT DICTIONARY=====\n")
print("\n Marks Dictionary:")
print("{")
for subject, marks in student_marks.items():
   print(f'"{subject}": {marks},')
print("}")
print("======PRINT DICTIONARY=====\n \n \n")
   
# Total marks, Average marsk, Highest marks & Lowest marks Calculation
list = student_marks.values()
total_marks = sum(list)
min_marks = min(list)
max_marks = max(list)
average = total_marks/len(student_marks)

failed_subject = [ subject for subject, marks in student_marks.items() if marks < 40]

# print(failed_subject)

status = "Failed" if failed_subject else "Passed"

if status == "Failed":
   grade = "Failed"
if average >= 80:
   grade = "A+"
elif average >= 70:
   grade= "A"
elif average >= 60:
   grade= "A-"
elif average >= 50:
   grade="B"
elif average >= 40:
   grade="C"
else:
   grade = "Failed"

print("====================")
print("Students Report")
print("====================")
print("\n")
print(f"Student Name: {studentName}")
print(f"Student ID: {studentID}")
print(f"Student Department: {department}")
print("\n")

for subject, marks in student_marks.items():
   print(f"{subject} : {marks}")

print("------------------------------\n")
print(f"Total marks : {total_marks}")
print(f"Min marks : {min_marks}")
print(f"Total marks : {max_marks}")
print(f"Average Marks : {average}")
print(f"Grade : {grade}")
print(f"Status : {status}")
print("=====================\n \n")

# Str Operation
print("======String Operation=====\n")
uppercase = studentName.upper()
lowercase = studentName.lower()
length = len(studentName)

firstthree = studentName[:3]
lastthree = studentName[-3:]


print(f"Uppercase Name: {uppercase}\n")
print(f"Lower case Name: {lowercase}\n")
print(f"Length of Name: {length}\n")
print(f"First Three Character: {firstthree}\n")
print(f"Last Three Character: {lastthree}\n")
print("======String Operation=====\n\n\n")


# Password Verification
print("======Password Verification=====\n")
password="python123"

userpassword = input("enter your Password: ")

while userpassword != password:
   print("Password is correct! please try again\n")
 
   userpassword = input("enter your Password: ")
print("Pssword is Correct!! granted access\n")
print("======Password Verification=====\n \n")


#SET
# Dispaly common  
print("======SET OPERATION=====\n")
sports = {"Football", "Cricket", "Badminton"}
clubs ={ "programming", "Cricket", "Photography"}
commonitems = sports.intersection(clubs)
allitems = sports.union(clubs)

print(f"Displaying Common Items: {commonitems}\n")
print(f"Displaying All Items: {allitems}\n")
print("======SET OPERATION=====\n \n \n")


#Tuples
print("======TUPLES OPERATION=====\n")
weeks = ("saturday", "sunday", "monday", "tuesday", "Wednesday", "Thursday", "friday")

firstday = weeks[0]
lastday = weeks[6]

totaldays = len(weeks)
print(f"FirstDay of the Week is: {firstday}\n")
print(f"Lastday of the Week is: {lastday}\n")
print(f"Total Number of days in a week is : {totaldays}\n")
print("======TUPLES OPERATION=====\n")




  


   