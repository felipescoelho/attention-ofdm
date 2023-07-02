"""
Script with functions to generate DFT matrix.

Author: Luiz Felipe da S. Coelho - luizfelipe.coelho@smt.ufrj.br
Jun 30, 2023
"""


import numpy as np
from numba import njit


@njit
def gen_dft_matrix(no_bins : int):
    """Method to generate DFT matrix.

    Parameters
    ----------
    no_bins : int
        Number of bins in DFT matrix.
    
    Returns
    -------
    dft_matrix : np.ndarray
        DFT matrix.
    """

    dft_matrix = np.zeros((no_bins, no_bins), dtype=np.complex128)
    for row_idx in range(no_bins):
        for col_idx in range(no_bins):
            dft_matrix[row_idx, col_idx] = np.exp(1j*2*np.pi*row_idx*col_idx/no_bins)
    
    return dft_matrix


def gen_idft_matrix(no_bins : int):
    """Method to generate IDFT matrix.
    
    Parameters
    ----------
    no_bins : int
        Number of bins in IDFT matrix.
        
    Returns
    -------
    idft_matrix : np.ndarray
        IDFT matrix.
    """

    return np.conj(gen_dft_matrix(no_bins))/no_bins


# EoF
