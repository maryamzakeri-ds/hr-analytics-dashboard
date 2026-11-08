import dash
from dash import html

dash.register_page(__name__, path="/prediction")

layout = html.Div(
    [
        html.H2('Prediction')
    ]
)