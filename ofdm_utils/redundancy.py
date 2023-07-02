"""
Script with functions to solve redundancy in the OFDM system.

Author: Luiz Felipe da S. Coelho - luizfelipe.coelho@smt.ufrj.br
Jun 30, 2023
"""


import numpy as np


def gen_redundancy_matrix(dft_size : int, cp_length : int, cs_length : int,
                          type='cyclic'):
    """Method to generate a matrix to add redudancy
    
    Parameters
    ----------
    dft_size : int
        The length of the DFT, and of the (useful) block.
    cp_length : int
        Number of samples in prefix.
    cs_length : int
        Number of samples in suffix.
    type : str
        String to define type of redundancy, can be of two types:
            - `cyclic` -> Uses the symbol's samples to maintain the
            cyclic convolution.
            - `zeros` -> Uses zero padding as redundancy.

    Returns
    -------
    redundancy_matrix : np.ndarray
        An array with the matrix responsible for including redundancy.
    """

    if type == 'cyclic':
        cp_matrix = np.hstack((np.zeros((cp_length, dft_size-cp_length)),
                               np.eye(cp_length)))
        cs_matrix = np.hstack((np.eye(cs_length),
                               np.zeros((cs_length, dft_size-cs_length))))
    else:
        cp_matrix = np.zeros((cp_length, dft_size))
        cs_matrix = np.zeros((cs_length, dft_size))
    redundancy_matrix = np.vstack((cp_matrix, np.eye(dft_size), cs_matrix))
    
    return redundancy_matrix


def add_redundancy(frame:np.ndarray, cp_length:int, cs_length:int,
                   type='cyclic'):
    """Method to add redundancy.

    Parameters
    ----------
    frame : np.ndarray
        A frame with OFDM symbols. Symbols as columns and samples in
        rows.
    cp_length : int
        Number of samples to add as prefix
    cs_length : int
        Number of samples to add as suffix
    type : str
        String to define type of redundancy, can be of two types:
            - `cyclic` -> Uses the symbol's samples to maintain the
            cyclic convolution.
            - `zeros` -> Uses zero padding as redundancy.

    Returns
    -------
    extended_frame : np.ndarray
        A frame with OFDM symbols with redudancy added.
    """

    dft_size = frame.shape[0]
    redundancy_matrix = gen_redundancy_matrix(dft_size, cp_length, cs_length,
                                              type)
    extended_frame = np.matmul(redundancy_matrix, frame)

    return extended_frame


def gen_rm_redundancy_matrix(rm_length:int, no_recover:int):
    """Method to remove redundancy.

    Parameters
    ----------
    rm_length : int
        The number of samples to be removed from the beginning of each
        OFDM symbol.
    no_recover : int
        The number of samples to be recovered from received block.
    
    Returns
    -------
    rm_redundancy_matrix : np.ndarray
        Matrix used to remove redundancy.
    """

    rm_redundancy_matrix = np.hstack((np.zeros(no_recover, rm_length),
                                      np.eye(no_recover)))
    
    return rm_redundancy_matrix


def remove_redundancy(frame:np.ndarray, rm_length:int, no_recover:int):
    """Method to remove redundancy.

    Parameters
    ----------
    frame : np.ndarray
        An OFDM frame with redundancy.
    rm_length : int
        The number of samples to be removed from the beginning of each
        OFDM symbol.
    no_recover : int
        The number of samples to be recovered from received block.
    
    Returns
    -------
    ofdm_frame : np.ndarray
        The recovered OFDM frame without redundancy.
    """

    rm_redundancy_matrix = gen_rm_redundancy_matrix(rm_length, no_recover)
    ofdm_frame = np.matmul(rm_redundancy_matrix, frame)

    return ofdm_frame


# EoF
