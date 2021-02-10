from datetime import datetime
t = "17:35:15.354223".split(':')

d = datetime.strptime(t[0]+":"+t[1], "%H:%M")
print(d.strftime("%I:%M %p"))
