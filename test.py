from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
sdate = date(2008, 1, 1)   # start date
edate = date(2009, 1, 1)   # end date
start= sdate + relativedelta(months=1)
diff = start + sdate
print(diff)

# for i in range(11):
#     end = sdate