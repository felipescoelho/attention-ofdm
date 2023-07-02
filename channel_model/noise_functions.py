"""Script for functions regarding noise.

Author: Luiz Felipe da S. Coelho - luizfelipe.coelho@smt.ufrj.br
Jul 2, 2023
"""


import numpy as np


def awgn(input_signal:np.ndarray, snr:float):
    """Add White Gaussian Noise
    
    Adds white Gaussian noise according to SNR.
    
    Parameters
    ----------
    input_signal : np.ndarray
        Input signal, complex or real-valued.
    snr : float
        Signal to noise ratio, in dB.
    
    Returns
    -------
    noisy_signal : np.ndarray
        Noisy signal with adjusted SNR.
    """

    snr_adjustment = np.matmul(np.conjugate(np.transpose(input_signal)),
                             input_signal)/len(input_signal) * 10**(-snr/10)
    if input_signal.dtype == np.complex128:
        noise_real = np.random.randn(len(input_signal))
        noise_imag = np.random.randn(len(input_signal))
        noise = np.sqrt(
            snr_adjustment/np.matmul(np.transpose(noise_real), noise_real)
        )*noise_real + 1j*np.sqrt(
            snr_adjustment/np.matmul(np.transpose(noise_imag), noise_imag)
        )*noise_imag
    else:
        noise_real = np.random.randn(len(input_signal))
        noise = np.sqrt(
            snr_adjustment/np.matmul(np.transpose(noise_real), noise_real)
        )*noise_real

    noisy_signal = input_signal + noise

    return noisy_signal


# EoF
