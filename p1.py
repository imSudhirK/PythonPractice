import sys
import datetime 
print ("Python version")
print (sys.version)
print(sys.version_info)

now = datetime.datetime.now()
print ("current Date and time")
print (now.strftime("%Y-%m-%d %H:%M:%S"))

fname = input("Input your first name : ")
lname = input("Input your last name : ")

print("Hello " + lname + " " + fname)