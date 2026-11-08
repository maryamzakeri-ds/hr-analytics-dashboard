import dash
from dash import html

dash.register_page(__name__, path="/workforce")

layout = html.Div(
    [
        html.H2('Workforce Analytics')
    ]
)