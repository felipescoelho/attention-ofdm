"""Script to generate Rayleigh fading distribution.

Author: Luiz Felipe da S. Coelho - luizfelipe.coelho@smt.ufrj.br
Jul 3, 2023
"""


import numpy as np


def rayleigh_fading_jakes(no_oscillators:int, doppler_freq:float,
                          sampling_freq : float):
    """This function generates a Rayleigh fading waveform. We use
    Jakes' model for fading channel.
    
    1. Each oscilator corresponds has a frequency at the first quadrant
    of the unitary circle. The frequencies are obtained by the cosinus
    of evenly spaced angles in [0, pi/2).

    Parameters
    ----------
    no_oscillators : int
        Number of oscillators (>= 15 is good practice).
    doppler_freq : float
        Maximum Doppler frequency.
    sampling_freq : float
        Sampling rate.
    """

    time_index = np.arange(0, 1, 1/sampling_freq)
    real_part = np.sqrt(2)*np.cos(2*np.pi*doppler_freq*time_index)
    imag_part = 0*time_index
    for oscillator_idx in range(no_oscillators):
        # Generate oscillators:
        oscillator_freq = doppler_freq*np.cos(
            2*np.pi*(oscillator_idx+1)/(4*no_oscillators+2)
        )
        random_phase = np.pi*np.random.randn(1)
        oscillator = np.cos(2*np.pi*oscillator_freq*time_index + random_phase)
        # Gain:
        gain_angle = (oscillator_idx+1)*np.pi/(no_oscillators+1)
        # Calculate and sum oscillators:
        real_part += 2*np.cos(gain_angle)*oscillator
        imag_part += 2*np.sin(gain_angle)*oscillator
    # Scale:
    real_part /= np.sqrt(2*no_oscillators)
    imag_part /= np.sqrt(2*(no_oscillators+1))

    return real_part + 1j*imag_part


def rayleigh_fading_gmeds_1(no_oscillators:int, doppler_freq:float,
                            sampling_freq:float, no_waveforms:int):
    """Method to generate Rayleigh fading waveform using the GMEDS_1
    algorithm described in:
    
    - M. Patzold, C. -X. Wang and B. O. Hogstad, "Two new
    sum-of-sinusoids-based methods for the efficient generation of
    multiple uncorrelated rayleigh fading waveforms," in IEEE
    Transactions on Wireless Communications, vol. 8, no. 6,
    pp. 3122-3131, June 2009, doi: 10.1109/TWC.2009.080769.
    
    Parameters
    ----------
    no_oscillators : int
        Number of oscillators (= 20 is good enough).
    doppler_freq : float
        Maximum Doppler frequency.
    sampling_freq : float
        Sampling rate.
    no_waveforms : int
        Total number of uncorrelated waveforms.
    
    Returns
    -------
    rayleigh_fading_waveforms : np.ndarray
        Rayleigh fading waveform.
    """

    time_axis = np.arange(0, 1, 1/sampling_freq)
    rayleigh_fading_waveforms = np.zeros((len(time_axis), no_waveforms),
                                         dtype=np.complex128)
    for wave_idx in range(no_waveforms):
        real_wave = np.zeros((len(time_axis),))
        imag_wave = np.zeros((len(time_axis),))
        for oscil_idx in range(no_oscillators):
            angle_rotation = (np.pi/(4*no_oscillators)) \
                * (wave_idx/(no_waveforms+2))  # Must be negative for imaginary
            angle_arrival = (np.pi/(2*no_oscillators))*(oscil_idx+.5)
            oscil_freq_real = doppler_freq*np.cos(angle_arrival+angle_rotation)
            oscil_freq_imag = doppler_freq*np.cos(angle_arrival-angle_rotation)
            real_wave += np.cos(2*np.pi*oscil_freq_real*time_axis
                                + np.pi*np.random.randn(1))
            imag_wave += np.cos(2*np.pi*oscil_freq_imag*time_axis
                                + np.pi*np.random.randn(1))
        rayleigh_wave = np.sqrt(2/no_oscillators)*(real_wave + 1j*imag_wave)
        rayleigh_fading_waveforms[:, wave_idx] = rayleigh_wave

    return rayleigh_fading_waveforms


if __name__ == '__main__':

    from scipy.constants import speed_of_light
    import matplotlib.pyplot as plt
    
    velocity = 120  # Relative speed in km/h
    carrier_freq = 2*1e9
    doppler_freq = velocity*carrier_freq/speed_of_light
    no_oscillators = 100
    sampling_freq = 12*doppler_freq

    print(doppler_freq, sampling_freq)
    # chann = rayleigh_fading_jakes(no_oscillators, doppler_freq, sampling_freq)
    chann = rayleigh_fading_gmeds_1(no_oscillators, doppler_freq,
                                    sampling_freq, 2)
    chann = chann[:, 0]

    nfft = np.ceil(np.log2(len(chann)))
    chann_freq = np.fft.fftshift(np.fft.fft(chann, int(2**nfft)))

    fig1 = plt.figure()
    ax01 = fig1.add_subplot(211)
    ax11 = fig1.add_subplot(212)

    ax01.plot(chann.real)
    ax11.plot(chann.imag)

    fig2 = plt.figure()
    ax02 = fig2.add_subplot()
    ax02.plot(20*np.log10(np.abs(chann_freq)))

    fig3 = plt.figure()
    ax03 = fig3.add_subplot()
    ax03.plot(np.correlate(chann.real, chann.real, mode='full')/(len(chann)/2))


    plt.show()




# EoF
