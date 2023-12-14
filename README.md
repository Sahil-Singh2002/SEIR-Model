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

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

- The SEIR model is a well-known epidemiological model, and this implementation is inspired by its principles.
