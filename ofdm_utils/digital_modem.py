"""
Script with function to handle QAM/OFDM conversion.

Author: Luiz Felipe da S. Coelho - luizfelipe.coelho@smt.ufrj.br
Jun 30, 2023
"""


import numpy as np
# from numba import njit  # Not getting faster.


# @njit
def gen_qam_symbols(no_symbols:int, bits_per_symbol:int):
    """Method to generate QAM symbols.
    

    Parameters
    ----------
    no_symbols : int
        Number of symbols generated.
    bits_per_symbols : int
        Number of bits in a QAM symbol.

    Returns
    -------
    qam_sequence : np.ndarray
        Sequence of QAM symbols.
    """

    possible_values = np.arange(-bits_per_symbol-1, bits_per_symbol+2, 2)
    qam_sequence = np.zeros((no_symbols,), dtype=np.complex128)
    for symb_id in range(no_symbols):
        qam_sequence[symb_id] = np.random.choice(possible_values) \
            + 1j*np.random.choice(possible_values)

    return qam_sequence


# @njit
def gen_frame(bits_per_symbol:int, symbols_per_block:int, blocks_per_frame:int):
    """Method to generate frame of QAM symbols

    Parameters
    ----------
    bits_per_symbol : int
        Number of bits in each QAM symbol
    symbols_per_block : int
        Number of QAM symbols in transmitted block (OFDM symbol)
        [columns in frame]
    blocks_per_frame : int
        Number of OFDM symbols in a frame
        [rows in frame]

    Returns
    -------
    frame_qam : np.ndarray
        Frame containing QAM symbols.
    """

    frame_qam = np.zeros((blocks_per_frame, symbols_per_block),
                         dtype=np.complex128)
    for block_id in range(blocks_per_frame):
        frame_qam[block_id, :] = gen_qam_symbols(symbols_per_block,
                                                 bits_per_symbol)
    
    return frame_qam


if __name__ == '__main__':
    print(gen_frame(10, 1024, 16))

# EoF
