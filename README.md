# SEIR Model for Workplace Infection Spread

## Overview

This Python script simulates the spread of infections in a workplace using the SEIR (Susceptible-Exposed-Infectious-Recovered) model. The model takes into account various preventative measures, such as testing, social distancing, masking, ventilation, and more.

## Getting Started

### Prerequisites

- Python 3.x
- Required Python libraries: `numpy`, `scipy`, `matplotlib`, `tkinter` (for user interface)

### Installation

No installation is required beyond having a Python interpreter with the necessary libraries installed.

## Usage

1. Run the script in a Python environment.
2. The script will prompt you to input parameters for the SEIR model and preventative measures. You can either use default values or input your own.
3. The simulation results will be displayed in a plot, showing the projected spread of the virus over time.

## Parameters

The script prompts for the following parameters:

- **Testing**: Whether testing is performed.
- **Bubbling**: Whether staff is split into bubbles.
- **Social Distancing**: Whether social distancing is followed.
- **Masking**: Whether masks are worn.
- **Ventilation**: Whether ventilation is used.
- **Rota Schedule**: Whether a rota schedule is implemented.
- **Sanitization and Cleaning**: Whether sanitization and cleaning are performed.
- **Initial Infected Individuals**: Number of initially infected people.
- **Total Number of Staff**: Total number of staff in the workplace.
- **Working Day Hours**: Number of hours in a working day.

## Results

The script outputs the following information:

- **Chosen Parameters**: If default values are used, it displays the chosen example parameters.
- **Simulation Results**: Displays key metrics, including the infection risk, peak infection number, and the day infections become less than 1.

## Notes

- The script uses the SEIR model and considers various factors to project the spread of infections in a workplace.
- The user interface allows for easy input of parameters, making it flexible for different scenarios.

## Acknowledgments

- The SEIR model is a well-known epidemiological model, and this implementation is inspired by its principles.

Certainly! Below is a sample README file for your code. Please review and adjust it based on your specific project details and any additional information you want to provide.

---

# Stochastic SEIR Simulation

This Python script conducts a stochastic simulation of the Susceptible-Exposed-Infectious-Recovered (SEIR) model, considering various parameters and preventative measures. The simulation incorporates randomness in infection and recovery rates to model real-world uncertainties.

## Getting Started

### Prerequisites

- Python 3.x
- Required Python libraries: `numpy`, `matplotlib`

### Installation

No additional installation is required beyond having a Python interpreter with the necessary libraries installed.

## Usage

1. Run the script in a Python environment.
2. Adjust the `testing`, `bubbling`, `social_distancing`, `masking`, `ventilation`, `rotas`, `sanitiser`, `cleaning`, and other parameters based on your specific scenario.
3. The script will conduct a stochastic SEIR simulation and display the results in a set of plots, showing the evolution of susceptible, exposed, infected, and recovered individuals over time for multiple simulations.

## Parameters

The script includes the following key parameters:

- **Testing**: Indicator for testing (0 for no testing, 1 for testing).
- **Bubbling**: Whether staff is split into bubbles.
- **Social Distancing**: Indicator for social distancing (0 for no, 1 for yes).
- **Masking**: Indicator for wearing masks (0 for no, 1 for yes).
- **Ventilation**: Indicator for using ventilation (0 for no, 1 for yes).
- **Rotas**: Indicator for rota schedules (0 for no, 1 for yes).
- **Sanitiser and Cleaning**: Indicators for using sanitiser and cleaning surfaces.
- **Simulation Parameters**: Mean and standard deviation for infection (beta), exposed to infected (gamma), and infected to recovered (sigma) rates.
- **Preventative Measures**: Proportion of the day for wearing masks (mu), effectiveness of ventilation (ve), proportion of the day using ventilation (vu), number of people in each bubble (Nb), total number of people (NT_all_rota_days), number of rota groups (no_of_rota_groups), initial infected individuals (IT), social distancing length (sd), hours in a working day (W), cleans per day (c), sanitises per day (s), and testing frequency (freq_testing).

## Results

The script generates plots displaying the progression of susceptible, exposed, infected, and recovered individuals over time for multiple simulations. The stochastic nature of the simulation introduces variability in the outcomes.

## Acknowledgments

- The SEIR model is a standard epidemiological model, and this implementation introduces stochasticity to better capture real-world uncertainties.

## License

This project is licensed under the [MIT License](LICENSE).
