from datetime import datetime, timedelta
 
# date object of today's date
today = datetime.now()
activationdate = datetime.now()
expirydate = datetime.now() + timedelta(days=90)


print("Current Date : " , today)
print("Activation Date : ", activationdate)
print("Expiry Date : ", expirydate)

if ( (expirydate-today) == 30):
	print("Num of Days : ", (expirydate-today))
elif ( (expirydate-today) == 15) :
	print("Num of Days : ", (expirydate-today))
else :
	print("Num of Days : ", (expirydate-today))