"""Script to generate channel tapped-delay-lines according to ITU-R
Models.

Ref:
[1] Simulation of Communication Systems: Modeling, Methodology, and
Techniques, by Michael C. Jeuchim, Philip Balaban, and K. Sam Shanmugan,
2nd Ed., 2000, Kluwer Academic/Plenum Publishers.
[2] Andreas F. Molisch, "Channel Models," in Wireless Communications,
IEEE, 2011, pp.125-143, doi: 10.1002/9781119992806.ch7.


Author: Luiz Felipe da S. Coelho - luizfelipe.coelho@smt.ufrj.br
Jul 1, 2023
"""


import numpy as np
from scipy.constants import speed_of_light


def gen_vehicular(channel_model:str, velocity:float, carrier_freq:float,
                  sampling_freq:float):
    """Method to generate a vehicular channel according to ITU-R Models.
    
    By now, only two models are implemented:
    VehicularA -> Vehicular Test Environment with low delay spread.
    VehicularB -> Vehicular Test Environment with high delay spread.

    Parameters
    ----------
    channel_model : str
        Selected channel model.
    velocity : float
        Relative speed between transmitter and receiver.
    carrier_freq : float
        Carrier frequency of the transmitted signal.
    sampling_freq : float
        Channel's sampling frequency (same as the transmitted).

    Returns
    -------
    channel_tdl : np.ndarray
        Channel tapped-delay-line model.
    """

    possible_channels = ('VehicularA', 'VehicularB')
    assert channel_model in possible_channels, 'The possible channels are ' \
        + ', '.join(possible_channels) + '.'
    # Define model parameters
    if channel_model == 'VehicularA':
        channel_delay = np.array((0, 310, 710, 1090, 1730, 2510),
                                 dtype=np.float64)*1e-9
        channel_avg_power = np.array((0, -1, -9, -10, -15, -20),
                                     dtype=np.float64)
        doppler_spectrum = ['Jakes']*6
    elif channel_model == 'VehicularB':
        channel_delay = np.array((0, 300, 8900, 12900, 17100, 20000),
                                 dtype=np.float64)*1e-9
        channel_avg_power = np.array((-2.5, 0, -12.8, -10, -25.2, -16),
                                     dtype=np.float64)
        doppler_spectrum = ['Jakes']*6

    # Start calculation:
    doppler_freq = velocity*carrier_freq/speed_of_light


if __name__ == '__main__':

    channel_delay = np.array((0, 300, 8900, 12900, 17100, 20000),
                             dtype=np.float64)*1e-9
    dist = channel_delay - np.hstack((0, channel_delay[:-1]))
    print(dist)



# EoF
