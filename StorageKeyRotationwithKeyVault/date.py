import calendar
from datetime import date, datetime, timedelta

# date object of today's date
today = datetime.now()
activationdate = datetime.now()
expirydate = datetime.now() + timedelta(days=30)
notificationdate = expirydate - timedelta(days=20)


print("Current Date : " , today)
print("notificationdate Date : ", notificationdate)
print("Expiry Date : ", expirydate)


from datetime import datetime


timestamp = 1668205800
dt_obj = datetime.fromtimestamp(timestamp).strftime('%d-%m-%y')

print("date:",dt_obj)
