import pandas as pd

from convertmol import parse_sdf_file

# result = parse_sdf_file("Structure2D_CID_962.sdf")
result = parse_sdf_file("Conformer3D_CID_5988.sdf")

atoms = filter(lambda x: x[0][0]=="?",result[0].items())
atoms = map(lambda x:x[1],atoms)
d = pd.DataFrame(atoms)
d


import urllib.request
code="962"
urllib.request.urlretrieve("https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/CID/"+code+"/record/SDF/?record_type=3d&response_type=save&response_basename=Conformer3D_CID_"+code, code+".sdf")
name="codeine"
urllib.request.urlretrieve("https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/"+name+"/sdf",name+".sdf")
