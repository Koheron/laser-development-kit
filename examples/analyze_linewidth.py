import initExample
import numpy as np
from scipy.optimize import curve_fit
from scipy.special import wofz
import matplotlib.pyplot as plt

from ldk import DataReader

def lorentzian(f, df):
    return 1 / (1 + (f / df)**2)

def lorentzian_log(f, df):
    return 10 * np.log10(lorentzian(f, df))

def voigt(f, alpha, gamma, A):
    sigma = alpha / np.sqrt(2 * np.log(2))
    return A * np.real(wofz((f + 1j*gamma)/sigma/np.sqrt(2)))

if __name__ == "__main__":
    # reader = DataReader('../linewidth_90mA.zip')
    # rseader = DataReader('../linewidth_90mA_2.zip')
    # reader = DataReader('../linewidth_thorlabs_130mA.zip')
    # reader = DataReader('../linewidth_thorlabs_90mA.zip')
    reader = DataReader('../linewidth_thorlabs_100mA_4.zip')
    # reader = DataReader('../linewidth_thorlabs_130mA_3.zip')
    reader.print_all()
    reader.get_plot_data()
    freq = np.transpose(reader.data_x)
    psd = np.transpose(reader.data_y)

    # Normalize data
    size = len(freq)
    f0 = size/2 # central frequency index
    psd0 = psd[f0]
    # psd0 = (psd[f0-2] + psd[f0+2]) / 2
    # psd[f0] = psd0
    # psd[f0-1] = psd0
    # psd[f0+1] = psd0

    psd_norm = psd/psd0

    # Lorentzian fit
    N = 128
    freq_lim = freq[f0-size/N:f0+size/N]
    psd_lim = psd_norm[f0-size/N:f0+size/N]
    # popt_lor, pcov = curve_fit(lorentzian, freq_lim, psd_lim)
    
    psd_lim_dBc = 10 * np.log10(psd_lim)
    popt_lor, pcov = curve_fit(lorentzian_log, freq_lim, psd_lim_dBc)

    print popt_lor

    # Voigt fit
    # popt_voigt, pcov = curve_fit(voigt, freq, psd_norm)
    # print popt_voigt

    psd_dBc = 10 * np.log10(psd_norm)
    psd_lim_dBc = 10 * np.log10(psd_lim)
    psd_lor_dBc = 10 * np.log10(lorentzian(freq, *popt_lor))
    # psd_voigt_dBc = 10 * np.log10(voigt(freq, *popt_voigt))

    plt.plot(freq, psd_dBc, 
             freq, psd_lor_dBc,
             freq_lim, psd_lim_dBc )
             # freq, psd_voigt_dBc)
    # plt.plot(freq, psd_dBc)
    plt.xlabel('Frequency (MHz)')
    plt.ylabel('Power spectral density (dB)')
    plt.show()



    reader.close()