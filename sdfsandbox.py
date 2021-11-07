import pandas as pd

from convertmol import parse_sdf_file

# result = parse_sdf_file("Structure2D_CID_962.sdf")
result = parse_sdf_file("pubchem_files/Conformer3D_CID_5988.sdf")

result

atoms = filter(lambda x: x[0][0]=="?",result[0].items())
atoms = map(lambda x:x[1],atoms)
bonds = filter(lambda x: x[0][0]=="(",result[0].items())
bonds = map(lambda x:x[0].split(" ")[-2:],bonds)
bonds = map(lambda x:(x[0][5:], x[1][5:-1]),bonds)
list(bonds)

",".join([";".join(x) for x in bonds])

d = pd.DataFrame(atoms)
d


import urllib.request
code="962"
urllib.request.urlretrieve("https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/CID/"+code+"/record/SDF/?record_type=3d&response_type=save&response_basename=Conformer3D_CID_"+code, code+".sdf")
name="codeine"
urllib.request.urlretrieve("https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/"+name+"/sdf",name+".sdf")
