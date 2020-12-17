################################################################################
# python script for structure alignment using Monte Carlo method               #
# Author: Panyue Wang                                                          #
# Email: pywang@ucdavis.edu                                                    #
################################################################################
import numpy as np
import sys

# returns CA and all atom coordinates
def pdb_parser(pdb_file_obj):
    xyz = np.zeros(3)
    ca_coords = []
    atom_coords = []
    for line in pdb_file_obj:
        line_arr = line.split()
        if line_arr[0] == "TER":
            break
        xyz[0] = line_arr[6]
        xyz[1] = line_arr[7]
        xyz[2] = line_arr[8]
        # get C-alphas
        if line_arr[2] == "CA":
            ca_coords.append(xyz)
        atom_coords.append(xyz)
    
    return np.array(ca_coords), np.array(atom_coords)

# calculate the RMSD between the target and the input
def get_RMSD(target, input):
    pass

# Monte Carlo functions
def MC_translation(ca_arr, stepsize):
    pass

def MC_rotation(ca_arr, stepsize):
    pass

def MC_alignment(target_arr, input_arr, steps, stepsize):
    pass

if __name__ == "__main__":
    # getting inputs
    input_pdb = open(sys.argv[1], 'r')
    input_ca, input_atom = pdb_parser(input_pdb)
    target_pdb = open(sys.argv[2], 'r')
    targe_ca, target_atom = pdb_parser(target_pdb)
    # starting Monte Carlo alignment

    pass