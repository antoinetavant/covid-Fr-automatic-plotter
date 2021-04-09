
import requests
import matplotlib.pyplot as plt

import pandas as pd
from datetime import datetime
import numpy as np

url = "https://www.data.gouv.fr/fr/datasets/r/dd0de5d9-b5a5-4503-930a-7b08dc0adc7c"
#url = "https://www.data.gouv.fr/en/datasets/r/dd0de5d9-b5a5-4503-930a-7b08dc0adc7c"

filename = '/home/pi/covid/sp-pos-quot-fra.csv'

r = requests.get(url, allow_redirects=True)

with open(filename, 'w') as fp:
    fp.write(r.content.decode())
    
dfr = pd.read_csv(filename, sep=";", parse_dates=["jour"], dtype={"T":int, "P":int})

dfr_all = dfr.loc[dfr.cl_age90 == 0].copy()
dfr_all.loc[:, "positivity"] = dfr_all.P.values/dfr_all["T"].values
dfr_all.loc[:, "daynam"] = dfr_all.jour.dt.day_name()

fig, ax = plt.subplots(1, 1, figsize=(8,5))

plt.plot(dfr_all.jour.values, dfr_all.positivity.values)

for i in range(1, 50):
    x = dfr_all.jour.values[-i]
    y = dfr_all.positivity.values[-i]
    s = dfr_all.daynam.values[-i]
    
    if s in ["Friday"]:
        plt.text(x, 0.96*y, s)
        plt.scatter(x, y, c="blue")
    elif s in ["Monday"]:
        plt.text(x, 1.02*y, s)
        plt.scatter(x, y, c="green")
        

fig.autofmt_xdate()
plt.xlim(dfr_all.jour.values[-50], dfr_all.jour.values[-1]+  np.timedelta64(1,'D'))
plt.grid(color="grey", linestyle=":")
plt.ylim( dfr_all.positivity.values[-50:].min()*0.9 , dfr_all.positivity.values[-50:].max()*1.1)
now = datetime.now()
plt.title("Evolution of the Positivity as fonction of date \n made on "  + now.strftime("%A %d/%m/%Y") )
plt.ylabel("Positivity (# Positifs/ # Tests)")
plt.xlabel("Date")

plt.savefig("covid_positivity_days.png", dpi=200)
