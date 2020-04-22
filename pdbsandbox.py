# import pypdb
# info = pypdb.get_info('NAG')
# import pandas as pd

import re
atoms = []
with open("5b27.pdb","r") as file:
    for line in file.readlines():
        if line[:4] == "ATOM":
            # lines.append(line)
            # coords = "["+",".join(re.sub(r' +',",",line).split(",")[6:9])+"]"
            # atoms.append(coords)
            atoms.append(line)


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

# lines[0]
# import re
# coords = re.sub(r' +',",",lines[0]).split(",")[6:9]
# len(lines)
