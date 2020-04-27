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

def genchange(data, k):
    sdata = data.copy()
    sidx = random.sample(list(sdata.index), k)

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

    for i in sidx:
        cidx = random.choice(range(cn))
        col, func = colfunc[cidx]
        sdata.loc[i, col] = func()
        hrago = random.choice(range(24))
        minago = random.choice(range(60))
        sdata.loc[i, "updated"] = datetime.now() - timedelta(hours=hrago, minutes=minago)
    
    return sdata

def convertToDim(data):
    d = data.copy()
    d["current"] = 1
    d["startdate"] = d["updated"]
    d["enddate"] = list(map(lambda _: datetime(2999, 12, 31), range(d.shape[0])))
    d["id"] = d.index
    d = d.drop(["created", "updated"], axis=1)

    return d

if __name__ == "__main__":
    # generate data
    d = gendata(1000)
    d.to_csv("users.csv", index_label="id")

    # convert data to dim
    dim = convertToDim(d)
    dim.to_csv("dimusers.csv", index_label="key")

    # generate new inserts
    n = gendata(50, 1001)

    # generate updates to data
    s = genchange(d, 300)

    # new data is combination of updates and inserts
    c = pd.concat([n, s])
    c.to_csv("stgusers.csv", index_label="id")
