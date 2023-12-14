# -*- coding: utf-8 -*-
"""
@author: sahil
"""

import numpy as np
import matplotlib.pyplot as plt


testing = 0 #testing should be a 0 if no testing done or 1 if testing is done
bubbling = True #bubbling should be 0 if no bubbling, or 1 if there is bubbling
social_distancing = 0 #SD is 0 if not being used, and 1 if being used
masking = 0 #0 if not using, 1 if using
ventilation = 0 #0 if not using, 1 if using
rotas = 0 #0 if not using, 1 if using
sanitiser = 0 #0 if not using, 1 if using
cleaning = 0 #0 if not using, 1 if using


# Parameters for the SEIR model
MEAN_BETA = 2.87/5.2
STD_BETA = 2*MEAN_BETA

MEAN_SIGMA = 1/5.2
STD_SIGMA = (MEAN_SIGMA**2)/8.06276

MEAN_GAMMA = 1/5.1

#Best Case
mu = 0.8  # Proportion of the day they wear masks
ve = 0.73  # Effectiveness of the ventilation type
vu = 1.0  # Proportion of the day they use ventilation
Nb = 5  # Number of people in each bubble
NT_all_rota_days = 100 # Total number of people
no_of_rota_groups = 2   # number of different rota groups
IT = 1  # Total number of infected individual
NT = NT_all_rota_days/no_of_rota_groups
Ib = IT*Nb/(NT)
sd = 2
W = 8     # Hours in a working day
c = 3     # Cleans per day
s = 25     # Sanitises per day
freq_testing = 1

#Worst Case
'''
mu = 0.0
ve = 0.0
vu = 0
Nb = 5
NT_all_rota_days = 100
no_of_rota_groups = 1
IT = 1
NT = NT_all_rota_days/no_of_rota_groups
Ib = IT*Nb/(NT)
sd_length =0
w = 0
c = 0
s = 0
freq_testing =0
'''

def beta(t: float) -> float:
    """Infection rate as a function of time with stochasticity."""
    return np.random.normal(loc=MEAN_BETA, scale=STD_BETA)

def gamma(t: float) -> float:
    """Exposed to Infected rate as a function of time with stochasticity"""
    return np.random.poisson(lam=MEAN_GAMMA)

def sigma(t: float) -> float:
    """Infected to Recovered rate as a function of time."""
    return np.random.gamma((MEAN_SIGMA/STD_SIGMA)**2,MEAN_SIGMA/(MEAN_SIGMA/STD_SIGMA)**2)

def dW(delta_t: float) -> float:
    """Sample a random number at each call."""
    return np.random.normal(loc=0.0, scale=np.sqrt(delta_t))

def run_simulation():
    """Return the result of one full stochastic SEIR simulation."""
    T_INIT = 0
    T_END = 100
    N = 1000  # Compute at 1000 grid points
    DT = float(T_END - T_INIT) / N
    TS = np.arange(T_INIT, T_END + DT, DT)
    assert TS.size == N + 1

    S_INIT = 0.99
    E_INIT = 0.0
    I_INIT = 0.01
    R_INIT = 0.0

    compartments = np.zeros((TS.size, 4))
    compartments[0, :] = [S_INIT, E_INIT, I_INIT, R_INIT]

    for i in range(1, TS.size):
      t = T_INIT + (i - 1) * DT
      beta_val = beta(t)
      sigma_val = sigma(t)
      gamma_val = gamma(t)

      def infection_risk(beta_val, Ib, mu, ve, vu, Nb, IT, sd, NT, W, c, s):
          if bubbling == True:
            term1 = (beta_val * Ib * (1 - 0.79 * mu) * (1 - ve * vu) * Nb/NT)
          else:
            Nb = 0
            Ib = 0
            term1 = 0
          term2 = (beta_val * (IT - Ib) * (1 - 0.79 * mu) * (1 - ve * vu) * sd * (NT - Nb)/NT)
          term3 = (0.002 * W / ((c + 1) * (s + 1)))*IT/NT

          return (term1 + term2 + term3)

      lambda_r = infection_risk(beta_val, Ib, mu, ve, vu, Nb, IT, sd, NT, W, c, s)
      S, E, I, R = compartments[i - 1, :]

      dS = -lambda_r * S * DT
      dE = (-gamma_val * E + lambda_r * S) * DT
      dI = (gamma_val * E - sigma_val * I - (1-0.056**freq_testing)*((1-sigma_val) * I)) * DT
      dR = (sigma_val * I + (1-0.056**freq_testing)*((1-sigma_val) * I))* DT

#      dW_val = dW(DT)

      compartments[i, :] = [S + dS, E + dE, I + dI, R + dR]

    return TS, compartments

def plot_simulations(num_sims: int):
    fig, axs = plt.subplots(4, 1, figsize=(10, 12))

    for sim_index in range(num_sims):
        TS, compartments = run_simulation()
        axs[0].plot(TS, compartments[:, 0], label=f'Susceptible {sim_index + 1}')
        axs[1].plot(TS, compartments[:, 1], label=f'Exposed {sim_index + 1}')
        axs[2].plot(TS, compartments[:, 2], label=f'Infected {sim_index + 1}')
        axs[3].plot(TS, compartments[:, 3], label=f'Recovered {sim_index + 1}')

    for ax in axs:
        ax.set_xlabel("Time (days)")
        ax.set_ylabel("Proportion (%)")
        ax.legend()
        ax.axis(ymin=0.0,ymax=1.0)
    plt.show()


if __name__ == "__main__":
    NUM_SIMS = 5
    plot_simulations(NUM_SIMS)