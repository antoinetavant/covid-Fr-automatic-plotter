
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

ndays = 50

fig, [ax1, ax2] = plt.subplots(2, 1, figsize=(10,8))

ax1.plot(dfr_all.jour.values[-ndays:], dfr_all.positivity.values[-ndays:])

for i in range(1, 50):
    x = dfr_all.jour.values[-i]
    y = dfr_all.positivity.values[-i]
    s = dfr_all.daynam.values[-i]
    
    if s in ["Friday"]:
        ax1.text(x, 0.96*y, s)
        ax1.scatter(x, y, c="blue")
    elif s in ["Monday"]:
        ax1.text(x, 1.02*y, s)
        ax1.scatter(x, y, c="green")
        

ax2.plot(dfr_all.jour.values[-ndays:], dfr_all.positivity.values[-ndays:], label="true dates")
ax2.plot(dfr_all.jour.values[-ndays-7:-7], dfr_all.positivity.values[-ndays:], label="one week shift")
ax2.legend()



for ax in [ax1, ax2]:
  ax.set_xlim(dfr_all.jour.values[-50], dfr_all.jour.values[-1]+  np.timedelta64(1,'D'))
  ax.grid(color="grey", linestyle=":")
  ax.set_ylim( dfr_all.positivity.values[-50:].min()*0.9 , dfr_all.positivity.values[-50:].max()*1.1)
  ax.set_ylabel("Positivity (# Positifs/ # Tests)")  
  ax.set_xlabel("Date")
  
#fig.autofmt_xdate()
for ax in fig.get_axes():
    if ax.is_last_row():
        for label in ax.get_xticklabels():
            label.set_ha('right')
            label.set_rotation(30.)
    else:
        for label in ax.get_xticklabels():
            label.set_visible(False)
        ax.set_xlabel('')
  
now = datetime.now()
ax1.set_title("Evolution of the Positivity as fonction of date \n made on "  + now.strftime("%A %d/%m/%Y") )



plt.savefig("covid_positivity_days.png", dpi=200)
