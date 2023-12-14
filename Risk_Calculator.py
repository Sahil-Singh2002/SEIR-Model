import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import simpledialog

#Create UI window
root = tk.Tk()
root.withdraw()

default = simpledialog.askinteger("Input", "Do you want to input the preventative measures yourself or do you want to use our recommended values to see how the calculator works? (0 to use ours, 1 to use your own)", parent=root)
if default == 0:
    #Example bools
    testing = 1 #testing should be a 0 if no testing done or 1 if testing is done 
    bubbling = 1 #bubbling should be 0 if no bubbling, or 1 if there is bubbling
    social_distancing = 1 #SD is 0 if not being used, and 1 if being used
    masking = 1 #0 if not using, 1 if using
    ventilation = 1 #0 if not using, 1 if using
    rotas = 0 #0 if not using, 1 if using
    sanitiser = 1 #0 if not using, 1 if using
    cleaning = 1 #0 if not using, 1 if using

    #Example Parameters for the SEIR model
    R0 = 2.87  # Base reproduction number
    beta = R0 / 5.2  # Transmission rate
    gamma = 1 / 5.1    # latent period rate
    sigma = 1 / 5.2   # infection period rate
    mu = 0.4  # Proportion of the day they wear masks
    ve = 0.3  # Effectiveness of the ventilation type
    vu = 0.5  # Proportion of the day they use ventilation
    Nb = 10  # Number of people in each bubble
    NT_all_rota_days = 100 # Total number of people
    no_of_rota_groups = 0   # number of different rota groups
    IT = 1  # Total number of infected individuals
    Sd_length = 1
    W = 8     # Hours in a working day
    c = 2     # Cleans per day
    s = 4     # Sanitises per day
    freq_testing = 0.25   # frequency of testing (number of times a day, i.e =2 is twice a day, and =0.5 is every 2 days)
else:
    testing = simpledialog.askinteger("Input", "Do you do LFD testing? (0 for no, 1 for yes):", parent=root)
    if testing == 1:
        freq_testing = simpledialog.askfloat("Input", "How often do staff test? (number of times per day)", parent=root)
    else:
        freq_testing = 0
        
    bubbling = simpledialog.askinteger("Input", "Do you split staff into bubbles? (0 for no, 1 for yes):", parent=root)
    if bubbling == 1:
        Nb = simpledialog.askfloat("Input", "How many people in each bubble?", parent=root)
    else:
        Nb = 0
        
    social_distancing = simpledialog.askinteger("Input", "Do you follow social distancing? (0 for no, 1 for yes):", parent=root)
    if social_distancing == 1:
        Sd_length = simpledialog.askfloat("Input", "What distance do you advise in metres?", parent=root)
    else:
        Sd_length = 0
        
    masking = simpledialog.askinteger("Input", "Do you wear masks? (0 for no, 1 for yes):", parent=root)
    if masking == 1:
        mu = simpledialog.askfloat("Input", "What proportion of the day do you wear masks for? (0,1]", parent=root)
    else:
        masking = 0
        
    ventilation = simpledialog.askinteger("Input", "Do you use ventilation? (0 for no, 1 for yes):", parent=root)
    if ventilation == 1:
        venttype = simpledialog.askinteger("Input", "Do you open windows or have air filters? (0 for windows, 1 for air filters, 2 for both)", parent=root)
        if venttype == 0:
            ve = 0.1
        else:
            filtercount = simpledialog.askinteger("Input", "How many air filters do you have?", parent=root)
            ve = filtercount * 0.1
            if ve > 0.7:
                ve = 0.73
            if venttype == 2:
                ve += 0.1
        vu = simpledialog.askfloat("Input", "What proportion of the day do you use ventilation for? (0,1] ", parent=root)
                
    rotas = simpledialog.askinteger("Input", "Do you have a rota schedule? (0 for no, 1 for yes):", parent=root)
    if rotas == 1:
        no_of_rota_groups = simpledialog.askinteger("Input", "How many rota groups do you have?", parent=root)
    else:
        no_of_rota_groups = 0
    
    sanitiser = simpledialog.askinteger("Input", "Do staff sanitise their hands during the day? (0 for no, 1 for yes):", parent=root)
    if sanitiser == 1:
        s = simpledialog.askinteger("Input", "How many times do you advise that staff sanitise their hands in a day?", parent=root)
    else:
        s = 0
        
    cleaning = simpledialog.askinteger("Input", "Do you clean surfaces? (0 for no, 1 for yes):", parent=root)
    if cleaning == 1:
        c = simpledialog.askinteger("Input", "How many times do you advise that surfaces are cleaned per day?", parent=root)
    else:
        c = 0
        
    IT = simpledialog.askinteger("Input", "How many infected people do you have initially? (If unsure then assume it's 1)", parent=root)
    
    NT_all_rota_days = simpledialog.askinteger("Input", "What is the total number of staff at your company?", parent=root)
    
    W = simpledialog.askinteger("Input", "How many hours are in a working day?", parent=root)
    
root.destroy()
    
# Parameters for the SEIR model
R0 = 2.87  # Base reproduction number
beta = R0 / 5.2  # Transmission rate
gamma = 1 / 5.1    # latent period rate
sigma = 1 / 5.2   # infection period rate

# carry out logic checks
if rotas:
    NT = NT_all_rota_days/no_of_rota_groups # Total number of people in the workplace per day
else:
    NT = NT_all_rota_days # Total number of people in the workplace per day

if bubbling:
    Ib = IT/(NT/Nb) # Number of infected people in a bubble
else:
    Ib = 0
    Nb = 0
    
# Social distancing rate
if social_distancing:
    if 0<Sd_length<=1:
        sd = 0.128
    else:
        sd = 0.026
else:
    sd = 1
    
if testing == 0:
    freq_testing = 0
if masking == 0:
    mu = 0.0
    
if ventilation == 0:
    ve = 0.0
    vu = 0.0

if sanitiser == 0:
    s = 0.0
        
if cleaning == 0:
    c = 0.0

# Infection risk lambda
def infection_risk(beta, Ib, mu, ve, vu, Nb, IT, sd, NT, W, c, s):
    if bubbling:
        term1 = (beta * Ib * (1 - 0.79 * mu) * (1 - ve * vu) * Nb/NT) 
    else:
        Nb = 0
        Ib = 0
        term1 = 0
    term2 = (beta * (IT - Ib) * (1 - 0.79 * mu) * (1 - ve * vu) * sd * (NT - Nb)/NT)
    term3 = (0.002 * W / ((c + 1) * (s + 1)))*IT/NT
    return (term1 + term2 + term3)

# SEIR model differential equations
def seir_model(y, t, N, beta, gamma, sigma, lambda_r):
    S, E, I, R = y
    dSdt = -lambda_r * S
    dEdt = -gamma * E + lambda_r * S
    dIdt = gamma * E - sigma * I - (1-0.056**freq_testing)*((1-sigma) * I)
    dRdt = sigma * I + (1-0.056**freq_testing)*((1-sigma) * I)
    return dSdt, dEdt, dIdt, dRdt

# Initial number of infected and recovered individuals
I0 = IT
R0 = 0
E0 = 0

S0 = NT - I0 - R0 - E0

N = S0 + E0 + I0 + R0

t = np.linspace(0, 100, 100)

# Calculate infection risk lambda
lambda_r = infection_risk(beta, Ib, mu, ve, vu, Nb, IT, sd, NT, W, c, s)

y0 = S0, E0, I0, R0

temp = odeint(seir_model, y0, t, args=(N, beta, gamma, sigma, lambda_r))
S, E, I, R = temp.T

plt.figure(figsize=(10, 6))
plt.plot(t, S, 'b', alpha=0.7, linewidth=2, label='Susceptible')
plt.plot(t, E, 'y', alpha=0.7, linewidth=2, label='Exposed')
plt.plot(t, I, 'g', alpha=0.7, linewidth=2, label='Infected')
plt.plot(t, R, 'r', alpha=0.7, linewidth=2, label='Recovered')
plt.xlabel('Time (days)')
plt.ylabel('Number of people')
plt.title('SEIR Model Simulation')
plt.legend()
plt.show()

#Output
if default == 0:
    print("""\nThe values we have chosen as an example are:
          R0 = 2.87  (Base reproduction number)
          beta = R0 / 5.2  (Transmission rate)
          gamma = 1 / 5.1    (Latent period rate)
          sigma = 1 / 5.2   (Infection period rate)
          mu = 0.4  (Proportion of the day they wear masks)
          ve = 0.3  (Effectiveness of the ventilation type)
          vu = 0.5  (Proportion of the day they use ventilation)
          Nb = 10  (Number of people in each bubble)
          NT_all_rota_days = 100 (Total number of people)
          no_of_rota_groups = 0   (Number of different rota groups)
          IT = 1  (Total number of infected individuals)
          Sd_length = 1 (Distance of social distancing in metres)
          W = 8     (Hours in a working day)
          c = 2     (Cleans per day)
          s = 4     (Sanitises per day)
          freq_testing = 0.25   (Frequency of testing)""")
else:
    print(f"""
          \nThese are the values you have:
          \nR0 = 2.87 (Base reproduction number)
          beta = R0 / 5.2  (Transmission rate)
          gamma = 1 / 5.1    (Latent period rate)
          sigma = 1 / 5.2   (Infection period rate)
          mu = {mu} (Proportion of the day they wear masks)
          ve = {ve} (Effectiveness of the ventilation type)
          vu = {vu} (Proportion of the day they use ventilation)
          Nb = {Nb} (Number of people in each bubble)
          NT_all_rota_days = {NT_all_rota_days} (Total number of people)
          no_of_rota_groups = {no_of_rota_groups} (Number of different rota groups)
          IT = {IT} (Total number of infected individuals)
          Sd_length = {Sd_length} (Distance of social distancing in metres)
          W = {W} (Hours in a working day)
          c = {c} (Cleans per day)
          s = {s} (Sanitises per day)
          freq_testing = {freq_testing} (Frequency of testing)
          """)

print("\nThe infection risk per day (lambda) is", lambda_r, ", this is the average number of new infections per day.")
print("The peak infection number is", max(I))
print("The first day that infections becomes less than 1 is", np.where(I < 1)[0][0], ", this indicates that the pandemic is nearly finished as the chance of infection is minimal")
print("The plot shows the projected spread of the virus through your workplace using an SEIR model based on the preventative measures you have in place.")


        