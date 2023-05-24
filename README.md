# Greek
Bringing the Greeks to Life
Options Greeks Calculator and Explainer

This is an interactive application built with Dash and Plotly, designed to calculate and visualize options Greeks.
Table of Contents

    Installation
    Usage
    Contribution
    License

Installation

Follow these steps to install and run the project:

    Ensure you have Python 3.7 or newer installed on your machine.

    Clone this repository to your local machine:

    bash

git clone https://github.com/yourusername/Options-Greeks-Calculator.git

Navigate to the project directory and install the required packages using pip:

bash

cd Options-Greeks-Calculator
pip install -r requirements.txt

Run the application:

bash

    python app4.py

Usage

After launching the application, you will find a web interface with sliders and dropdowns.

Here is a brief overview of each component:

    Spot Price (S): Use the slider to adjust the current price of the underlying asset.

    Strike Price (K): Use the slider to adjust the strike price of the option.

    Time to Expiry (T): Use the slider to adjust the time to expiry of the option, in years.

    Volatility (V): Use the slider to adjust the volatility of the underlying asset.

    Risk-free Interest Rate (R): Use the slider to adjust the risk-free interest rate.

    Option Type: Use the dropdown to select the type of option (Call or Put).

    Select Greek: Use the dropdown to select the Greek you want to calculate and visualize (Price, Delta, Gamma, Theta, Vega, Rho).

The calculation results and the graph visualization will be updated in real-time as you change the parameters.
Contribution

Contributions are welcome! Please feel free to submit a Pull Request.
License

This project is licensed under the terms of the MIT license
