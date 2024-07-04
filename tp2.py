from cgi import test
from random import Random
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.signal import find_peaks

# Number of samples in between each peak for each circuit
DIFF_PEAKS_100 = 1130
DIFF_PEAKS_200 = 836
DIFF_PEAKS_1000 = 1771
DIFF_PEAKS_4700 = 2539

# Maximum current of the circuit in mA
MAX_I_100 = 8.79
MAX_I_200 = 7.34
MAX_I_1000 = 2.35
MAX_I_4700 = 0.076

# Time at which the current is maximum for each circuit
MAX_I_TIME_100 = 3.37
MAX_I_TIME_200 = 3
MAX_I_TIME_1000 = 2.53
MAX_I_TIME_4700 = 2.92

# Range of time to take in for tau calculation for each circuit
RANGE_100 = (3.2, 4.2)
RANGE_200 = (2.8, 3.4)
RANGE_1000 = (2.5, 4)
RANGE_4700 = (2.5, 7.5)

# Electric potential difference due to the capacitor's discharge for each circuit
DELTA_V_100 = 1.8
DELTA_V_200 = 2.9
DELTA_V_1000 = 4.6
DELTA_V_4700 = 0.7

def read_data(filename):
    data = pd.read_csv(filename)
    return data['CH1 [V]']

def test_plot(resistance):
    voltage = np.array(read_data(f'resistencia{resistance}.csv'))
    plt.plot(voltage)
    plt.show()

def theory_current(r, c, epsilon, delta_v, t):
    return -(1/(r*c)) * ((c*delta_v) - (epsilon*c)) * np.exp(-(t/(r*c)))

def closest_time(t, time):
    aux_list = [abs(t - time[i]) for i in range(0, len(time))]
    return aux_list.index(min(aux_list))

def graph_experimental(resistance, diff_peaks, time, max_current, t_range, max_i_t):
    voltage = np.array(read_data(f'resistencia{resistance}.csv'))
    current = 1000 * voltage/resistance
    
    frec = diff_peaks/time
    total_time = len(current)/frec
    time_axis = np.linspace(0, total_time, len(current))

    # current_in_theory = [theory_current(resistance, c, epsilon, delta_v, t) for t in time_axis]
    plt.plot(time_axis, current)
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Corriente [mA]")
    plt.title(f"Corriente experimental en función del tiempo\nResistencia de {resistance} ohms")
    plt.grid()

    tau = 0
    time_range = np.arange(t_range[0], t_range[1], 0.01)
    for t in time_range:
        _idx = closest_time(t, time_axis)
        # idx = list(time_axis).index(_idx)
        current_at_time_t = current[_idx]
        current_left = current_at_time_t / max_current
        if current_left < 0.368:
            tau = t
            plt.scatter(tau, current_at_time_t, color='red', label='Tiempo tau')
            plt.legend()
            break

    # plt.plot(time_axis, current_in_theory)
    print(f"Tau teorico con resistencia {resistance} ohms: {resistance * 0.00047} segundos")
    print(f"Tau experimental con resistenciata {resistance} ohms: {tau - max_i_t} segundos\n")
    plt.show()
    return tau - max_i_t

tau_100 = graph_experimental(100, DIFF_PEAKS_100, 3, MAX_I_100, RANGE_100, MAX_I_TIME_100)
tau_200 = graph_experimental(200, DIFF_PEAKS_200, 2.4, MAX_I_200, RANGE_200, MAX_I_TIME_200)
tau_1000 = graph_experimental(1000, DIFF_PEAKS_1000, 5.22, MAX_I_1000, RANGE_1000, MAX_I_TIME_1000)
tau_4700 = graph_experimental(4700, DIFF_PEAKS_4700, 9.5, MAX_I_4700, RANGE_4700, MAX_I_TIME_4700)