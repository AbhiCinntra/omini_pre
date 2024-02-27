from datetime import datetime
d = datetime.strptime("18:54:29", "%H:%M:%S")
dd = d.strftime("%I:%M:%S %p")
print(dd)
