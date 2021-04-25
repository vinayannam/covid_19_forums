import json
from collections import defaultdict
import pandas as pd

data = pd.read_csv('sympgraph.csv')

d1 = defaultdict(list)
for i in range(data.shape[0]):
    d1[data.loc[i,'Source']].append((data.loc[i,'Destination'],data.loc[i,'Weight']))

symp_dict = open("sympgraph_dict.json", "w")
json.dump(d1, symp_dict)
symp_dict.close()


