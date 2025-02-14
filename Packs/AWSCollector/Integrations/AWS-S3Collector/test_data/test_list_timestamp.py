from datetime import datetime, date, timedelta

data = [datetime.now(), datetime.now()-timedelta(days=1), datetime.now()-timedelta(days=2),
        datetime.now()-timedelta(days=3)]
print(min(data))