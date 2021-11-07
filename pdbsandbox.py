# import pypdb
# info = pypdb.get_info('NAG')
# import pandas as pd
import numpy as np

import re
atoms = []
bonds = []
with open("pdb_files/5b27.pdb","r") as file:
    for line in file.readlines():
        if line[:4] == "ATOM":
            # lines.append(line)
            # coords = "["+",".join(re.sub(r' +',",",line).split(",")[6:9])+"]"
            # atoms.append(coords)
            atoms.append(line)
        elif line[:6] == "CONECT":
            bonds.append(line)


import pandas as pd
len(atoms)
atoms[:10]
import sys
if sys.version_info[0] < 3:
    from StringIO import StringIO
else:
    from io import StringIO

fake_file = StringIO("".join(atoms))
pd.read_csv(fake_file, delim_whitespace=True, header=None)
fake_file2 = StringIO("A 0 0 0 0 0\n"+"".join(bonds))
d = pd.read_csv(fake_file2, delim_whitespace=True, header=None, dtype={0:str, 1:pd.Int64Dtype(), 2:pd.Int64Dtype(), 3:pd.Int64Dtype(), 4:pd.Int64Dtype(), 5:pd.Int64Dtype()})

bonds=[]
for i,r in d.iterrows():
    if i == 0: continue
    print(r[1])
    for c in r[2:]:
        if type(c) == type(0):
            # print(c)
            bonds.append((r[1], c))

bonds
# lines[0]
# import re
# coords = re.sub(r' +',",",lines[0]).split(",")[6:9]
# len(lines)
