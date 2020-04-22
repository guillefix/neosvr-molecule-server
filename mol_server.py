from http.server import BaseHTTPRequestHandler, HTTPServer
import numpy as np
import urllib.request
import os
import sys
#this is used for a trick to parse a string into a pandas dataframe
if sys.version_info[0] < 3:
    from StringIO import StringIO
else:
    from io import StringIO
import pandas as pd
import re

# code="water"
# code="5B27"

def atom_array_to_string(array):
    #converts a numpy array with rows corresponding to (x,y,z,atom_type) to a formated string
    return ",".join(["["+";".join(["{:.4f}".format(c) for c in coords[:3]])+"]:"+str(coords[3])+":" for coords in array])+","

def get_atoms_str_PDB(code):
    if not os.path.exists(code+".pdb"):
        urllib.request.urlretrieve("https://files.rcsb.org/download/"+code+".pdb", code+".pdb")
    #parses PDB file to get the lines with the information about ATOMS
    atom_lines = []
    with open(code+".pdb","r") as file:
        for line in file.readlines():
            if line[:4] == "ATOM":
                line = line[:4]+" "+line[30:]
                atom_lines.append(line)
            elif line[:6] == "HETATM":
                line = line[:6]+" "+line[30:]
                atom_lines.append(line)

    #convert to pandas dataframe for convenience
    fake_file = StringIO("".join(atom_lines))
    atoms = pd.read_csv(fake_file, delim_whitespace=True, header=None)
    atoms = atoms.dropna()
    if len(atoms[atoms[0]=="ATOM"]) > 0:
        atoms = atoms[atoms[0]=="ATOM"]
    data = atoms[[1,2,3,6]]
    atoms_str = atom_array_to_string(data.values)
    return atoms_str

def get_atoms_str_PUBCHEM(name):
    if not os.path.exists(name+".sdf"):
        # try:
            # urllib.request.urlretrieve("https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/CID/"+code+"/record/SDF/?record_type=3d&response_type=save&response_basename=Conformer3D_CID_"+code, code+".sdf")
        # except:
        #     urllib.request.urlretrieve("https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/CID/"+code+"/record/SDF/?record_type=2d&response_type=save&response_basename=Structure2D_CID_"+code, code+".sdf")
        urllib.request.urlretrieve("https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/"+name+"/sdf",name+".sdf")

    from convertmol import parse_sdf_file
    # result = parse_sdf_file("Structure2D_CID_962.sdf")
    result = parse_sdf_file(name+".sdf")
    atoms = filter(lambda x: x[0][0]=="?",result[0].items())
    atoms = map(lambda x:x[1],atoms)
    data = pd.DataFrame(atoms)
    atoms_str = atom_array_to_string(data.values)
    return atoms_str

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        print(self.path)
        # if self.path == "/take":
        self._set_headers()
        # classification = open("classification.txt", "r").read()
        # self.wfile.write(bytes("<html><body><h1>"+str(classification)+"</h1></body></html>", "utf-8"))
        # poss = np.random.randn(10,3)
        # self.wfile.write(bytes(str(",".join(["["+";".join([str(c) for c in coords])+"]" for coords in poss])), "utf-8"))
        # self.wfile.write(bytes(str(atoms_str,"utf-8")))
        # atoms_str = get_atoms_str_PDB(self.path[1:])
        atoms_str = get_atoms_str_PUBCHEM(self.path[1:])
        self.wfile.write(bytes(atoms_str, "utf-8"))

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        # Doesn't do anything with posted data
        self._set_headers()
        self.wfile.write(bytes("<html><body><h1>POST!</h1></body></html>", "utf-8"))

def run(server_class=HTTPServer, handler_class=S, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd...')
    httpd.serve_forever()

run(port=42069)
