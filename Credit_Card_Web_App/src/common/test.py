import datetime

#time_now = datetime.datetime.now()
#week = time_now.strftime('%b 1 - %b 7')
#week = time_now.strftime('%m/%d/%y')
#date_1 = datetime.datetime.strptime(week, "%m/%d/%y")
#zy = date_1.strftime('%m/%d/%y')

#d = datetime.timedelta(days=7)
#z = date_1 + datetime.timedelta(days=7)
#xx = z.strftime('%b %d')

#week1 = time_now.strftime('%m/%d/%y')
#print(week1)
#date_1 = datetime.datetime.strptime(week1, "%m/%d/%y")

#plus_seven = date_1 + datetime.timedelta(days=7)
#z = plus_seven.strftime('%m/%d/%y')
#print(plus_seven)
#abx = date_1, z
#print(abx)

date = "2017-03-20"
x = ''
year = date[0:4]
month = date[5:7]
day = date[8:10]

year_int = int(year)
#print(year_int)
month_int = int(month)
#print(month_int)
day_int = int(day)
#print(day_int)

my_time = datetime.date(year_int, month_int, day_int)
print(my_time)
delta = my_time + datetime.timedelta(days=7)
print(delta)

test = delta.strftime('%Y-%m-%d')
x = x + test
print(x)
