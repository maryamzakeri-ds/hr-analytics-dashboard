import dash
from dash import html

dash.register_page(__name__, path="/attrition")

layout = html.Div(
    [
        html.H2('Attrition Analytics')
    ]
)