"""Script to run simulation of OFDM transmission.

Author: Luiz Felipe da S. Coelho - luizfelipe.coelho@smt.ufrj.br
Jun 30, 2023
"""


import numpy as np
from ofdm_utils import (gen_frame, add_redundancy, gen_idft_matrix, 
                        gen_dft_matrix)


if __name__ == '__main__':
    # Simulation definitions:
    mod_order = 1024  # Order of the digital modulation `mod_order`-QAM
    dft_size = 1024
    no_symbols = 16
    cp_length = 32
    cs_length = 0
    ensemble = 1  # Number of samples in Monte Carlo

    # Constants
    dft_matrix = gen_dft_matrix(no_bins=dft_size)
    idft_matrix = gen_idft_matrix(no_bins=dft_size)
    for it in range(ensemble):
        frame = gen_frame(np.log2(mod_order), dft_size, no_symbols)
        ofdm_frame = np.matmul(idft_matrix, np.transpose(frame))
        cp_ofdm = add_redundancy(ofdm_frame, cp_length, cs_length)
        

        

# EoF
