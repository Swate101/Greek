import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from scipy.stats import norm
import numpy as np

# Define the Black-Scholes-Merton formula and the Greeks

def bsm_price(s, k, t, v, r, option_type='call'):
    d1 = (np.log(s/k) + (r + 0.5 * v**2) * t) / (v * np.sqrt(t))
    d2 = d1 - v * np.sqrt(t)
    
    if option_type == 'call':
        price = s * norm.cdf(d1) - k * np.exp(-r * t) * norm.cdf(d2)
    else:
        price = k * np.exp(-r * t) * norm.cdf(-d2) - s * norm.cdf(-d1)
    
    return price

def bsm_delta(s, k, t, v, r, option_type='call'):
    d1 = (np.log(s/k) + (r + 0.5 * v**2) * t) / (v * np.sqrt(t))
    
    if option_type == 'call':
        delta = norm.cdf(d1)
    else:
        delta = -norm.cdf(-d1)
    
    return delta

def bsm_gamma(s, k, t, v, r):
    d1 = (np.log(s / k) + (r + 0.5 * v ** 2) * t) / (v * np.sqrt(t))
    gamma = norm.pdf(d1) / (s * v * np.sqrt(t))
    return gamma

def bsm_vega(s, k, t, v, r):
    d1 = (np.log(s / k) + (r + 0.5 * v ** 2) * t) / (v * np.sqrt(t))
    vega = s * norm.pdf(d1) * np.sqrt(t)
    return vega

def bsm_theta(s, k, t, v, r, option_type='call'):
    d1 = (np.log(s / k) + (r + 0.5 * v ** 2) * t) / (v * np.sqrt(t))
    d2 = d1 - v * np.sqrt(t)
    
    if option_type == 'call':
        theta = - (s * norm.pdf(d1) * v) / (2 * np.sqrt(t)) - r * k * np.exp(-r * t) * norm.cdf(d2)
    else:
        theta = - (s * norm.pdf(d1) * v) / (2 * np.sqrt(t)) + r * k * np.exp(-r * t) * norm.cdf(-d2)
    
    return theta

def bsm_rho(s, k, t, v, r, option_type='call'):
    d1 = (np.log(s / k) + (r + 0.5 * v ** 2) * t) / (v * np.sqrt(t))
    d2 = d1 - v * np.sqrt(t)
    
    if option_type == 'call':
        rho = k * t * np.exp(-r * t) * norm.cdf(d2)
    else:
        rho = -k * t * np.exp(-r * t) * norm.cdf(-d2)
    
    return rho

# Create a Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

# Define the app layout
app.layout = dbc.Container(
    [
        dbc.Alert(
            [
                html.H1("Options Greeks Calculator and Explainer", className="display-4", style={"color": "white"}),
                html.P(
                    "Use the sliders and dropdowns to calculate and visualize different options Greeks.",
                    className="lead",
                    style={"color": "white"},
                ),
            ],
            color="dark",
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Label("Spot Price (S)", style={"color": "white"}),
                        dcc.Slider(
                            id="spot-price",
                            min=50,
                            max=150,
                            value=100,
                            step=1,
                            marks={i: str(i) for i in range(50, 151, 10)},
                            className="dark-slider",
                            tooltip={'always_visible': True, 'placement': 'top'}
                        ),
                    ],
                    md=6,
                ),
                dbc.Col(
                    [
                        html.Label("Strike Price (K)", style={"color": "white"}),
                        dcc.Slider(
                            id="strike-price",
                            min=50,
                            max=150,
                            value=100,
                            step=1,
                            marks={i: str(i) for i in range(50, 151, 10)},
                            className="dark-slider",
                            tooltip={'always_visible': True, 'placement': 'top'}
                        ),
                    ],
                    md=6,
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Label("Time to Expiry (T)", style={"color": "white"}),
                        dcc.Slider(
                            id="expiry-time",
                            min=0.1,
                            max=2,
                            value=1,
                            step=0.1,
                            marks={i: '{:.1f}'.format(i) for i in np.arange(0.1, 2.1, 0.5)},
                            className="dark-slider",
                            tooltip={'always_visible': True, 'placement': 'top'}
                        ),
                    ],
                    md=6,
                ),
                dbc.Col(
                    [
                        html.Label("Volatility (V)", style={"color": "white"}),
                        dcc.Slider(
                            id="volatility",
                            min=0,
                            max=1,
                            value=0.2,
                            step=0.01,
                            marks={i: '{:.1f}'.format(i) for i in np.arange(0, 1.1, 0.2)},
                            className="dark-slider",
                            tooltip={'always_visible': True, 'placement': 'top'}
                        ),
                    ],
                    md=6,
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Label("Risk-free Interest Rate (R)", style={"color": "white"}),
                        dcc.Slider(
                            id="interest-rate",
                            min=0,
                            max=0.1,
                            value=0.05,
                            step=0.01,
                            marks={i: str(i) for i in np.arange(0, 0.11, 0.01)},
                            className="dark-slider",
                            tooltip={'always_visible': True, 'placement': 'top'}
                        ),
                    ],
                    md=6,
                ),
                dbc.Col(
                    [
                        html.Label("Option Type", style={"color": "white"}),
                        dcc.Dropdown(
                            id="option-type",
                            options=[
                                {"label": "Call", "value": "call"},
                                {"label": "Put", "value": "put"},
                            ],
                            value="call",
                            className="dark-dropdown",
                            style={'color': '#000'}  # Set text color to black
                        ),
                    ],
                    md=6,
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Label("Select Greek", style={"color": "white"}),
                        dcc.Dropdown(
                            id="greek-selection",
                            options=[
                                {"label": greek, "value": greek.lower()}
                                for greek in [
                                    "Price",
                                    "Delta",
                                    "Gamma",
                                    "Theta",
                                    "Vega",
                                    "Rho",
                                ]
                            ],
                            value="delta",
                            className="dark-dropdown",
                            style={'color': '#000'}  # Set text color to black
                        ),
                    ],
                    md=6,
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div(
                            id="dynamic-description",
                            className="lead mt-4",
                            style={"color": "white"},
                        )
                    ],
                    md=12,
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Graph(
                            id="greeks-graph",
                            config={"displayModeBar": False},
                            style={"height": "400px"},
                        )
                    ],
                    md=12,
                )
            ]
        ),
    ],
    className="mt-4",
    style={"backgroundColor": "#212529"},
)


# Define the callback to update the dynamic description
@app.callback(
    Output("dynamic-description", "children"),
    [
        Input("spot-price", "value"),
        Input("strike-price", "value"),
        Input("expiry-time", "value"),
        Input("volatility", "value"),
        Input("interest-rate", "value"),
        Input("option-type", "value"),
        Input("greek-selection", "value"),
    ],
)
def update_dynamic_description(
    s, k, t, v, r, option_type, greek_selection
):
    greek_value = {
        "price": bsm_price(s, k, t, v, r, option_type),
        "delta": bsm_delta(s, k, t, v, r, option_type),
        "gamma": bsm_gamma(s, k, t, v, r),
        "theta": bsm_theta(s, k, t, v, r, option_type),
        "vega": bsm_vega(s, k, t, v, r),
        "rho": bsm_rho(s, k, t, v, r, option_type),
    }.get(greek_selection, 0)

    if (
        greek_selection == "delta"
        and np.abs(greek_value - 1) < 0.1
    ):
        return "Delta is close to 1. The option price is likely to move closely with the underlying asset."
    elif greek_selection == "gamma" and greek_value > 0.1:
        return "Gamma is above 0.1. The delta is sensitive to changes in the underlying asset's price."
    elif greek_selection == "theta" and greek_value < -0.1:
        return "Theta is less than -0.1. The option price is sensitive to time decay."
    elif greek_selection == "vega" and greek_value > 0.2:
        return "Vega is above 0.2. The option price is sensitive to changes in volatility."
    elif greek_selection == "rho" and greek_value > 0.05:
        return "Rho is above 0.05. The option price is sensitive to changes in the interest rate."

    return ""


# Define the callback to update the graph
@app.callback(
    Output("greeks-graph", "figure"),
    [
        Input("spot-price", "value"),
        Input("strike-price", "value"),
        Input("expiry-time", "value"),
        Input("volatility", "value"),
        Input("interest-rate", "value"),
        Input("option-type", "value"),
        Input("greek-selection", "value"),
    ],
)
def update_graph(
    s, k, t, v, r, option_type, greek_selection
):
    spot_range = np.linspace(0.5 * s, 1.5 * s, 100)

    if greek_selection == "price":
        greek_values = [
            bsm_price(spot, k, t, v, r, option_type) for spot in spot_range
        ]
    elif greek_selection == "delta":
        greek_values = [
            bsm_delta(spot, k, t, v, r, option_type) for spot in spot_range
        ]
    elif greek_selection == "gamma":
        greek_values = [
            bsm_gamma(spot, k, t, v, r) for spot in spot_range
        ]
    elif greek_selection == "theta":
        greek_values = [
            bsm_theta(spot, k, t, v, r, option_type) for spot in spot_range
        ]
    elif greek_selection == "vega":
        greek_values = [
            bsm_vega(spot, k, t, v, r) for spot in spot_range
        ]
    elif greek_selection == "rho":
        greek_values = [
            bsm_rho(spot, k, t, v, r, option_type) for spot in spot_range
        ]
    else:
        greek_values = [0 for spot in spot_range]

    # Prepare the figure
    figure = go.Figure()
    figure.add_trace(
        go.Scatter(
            x=spot_range,
            y=greek_values,
            mode="lines",
            name=greek_selection.title(),
        )
    )
    figure.update_layout(
        title=f"{greek_selection.title()} as a function of Spot Price",
        xaxis_title="Spot Price",
        yaxis_title="Value",
        yaxis_zeroline=False,
        plot_bgcolor="#212529",  # Dark background color
        paper_bgcolor="#212529",  # Dark background color
        font_color="white",  # Font color
    )

    return figure


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
