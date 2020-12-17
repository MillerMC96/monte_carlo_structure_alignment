################################################################################
# python script for structure alignment using Monte Carlo method               #
# Author: Panyue Wang                                                          #
# Email: pywang@ucdavis.edu                                                    #
################################################################################
import numpy as np
import sys

# returns CA and all atom coordinates
def pdb_parser(pdb_file_obj):
    xyz = np.zero(3)
    ca_coords = []
    atom_coords = []
    for line in pdb_file_obj:
        line_arr = line.split()
        xyz[0] = line_arr[6]
        xyz[1] = line_arr[7]
        xyz[2] = line_arr[8]
        # get C-alphas
        if line_arr[2] == "CA":
            ca_coords.append(xyz)
        atom_coords.append(xyz)
    
    return np.array(ca_coords), np.array(atom_coords)

if __name__ == "__main__":
    input_pdb = open(sys.argv[1], 'r')
    ca, atom = pdb_parser

    pass