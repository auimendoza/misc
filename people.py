from faker import Faker
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import random

f = Faker()

def gendata(n, startid=1):
    ids = list(range(startid, n+startid))
    usernames =  list(map(lambda x: f.user_name(), ids))
    emails =  list(map(lambda x: f.email(), ids))
    firstnames = list(map(lambda x: f.first_name(), ids))
    lastnames =  list(map(lambda x: f.last_name(), ids))
    jobs =  list(map(lambda x: f.job(), ids))
    companies =  list(map(lambda x: f.company(), ids))
    zipcodes = list(map(lambda x: f.zipcode(), ids))
    birthday =  list(map(lambda x: f.date_of_birth(), ids))
    created = list(map(lambda x: f.date_time_between(start_date='-5y', end_date='-1d'), ids))
    updated = created

    columns = ["username", "email", "firstname", "lastname", "occupation", "employer", "zipcode", "dob", "created", "updated"]
    npdata = np.dstack([usernames, emails, firstnames, lastnames, jobs, companies, zipcodes, birthday, created, updated])

    data = pd.DataFrame(data=npdata[0], index=ids, columns=columns)

    return data

def genchange(data, frac, replace):
    s = data.sample(frac=frac, replace=replace)

    colfunc = [
        ('email', f.email),
        ('firstname', f.first_name),
        ('lastname', f.last_name),
        ('occupation', f.job),
        ('employer', f.company),
        ('zipcode', f.zipcode),
        ('dob', f.date_of_birth)
    ]

    cn = len(colfunc)

    for i in list(s.index):
        cidx = random.choice(range(cn))
        col, func = colfunc[cidx]
        s.loc[i, col] = func()
        hrago = random.choice(range(24))
        minago = random.choice(range(60))
        s.loc[i, "updated"] = datetime.now() - timedelta(hours=hrago, minutes=minago)
    
    return s

d = gendata(1000)
d.to_csv("users.csv", index_label="id")
n = gendata(50, 1001)
s = genchange(d, 0.3, True)
c = pd.concat([n, s])
c.to_csv("cusers.csv", index_label="id")
