from dash import html, dcc
import dash_bootstrap_components as dbc

def create_sidebar():
    sidebar = html.Div(
        [
            html.H3('HR Analytics'),
            html.Hr(),
            dbc.Nav(
                [
                    dbc.NavLink('Overview', href='/', active='exact'),
                    dbc.NavLink('Workforce', href='/workforce', active='exact'),
                    dbc.NavLink('Attrition', href='/attrition', active='exact'),
                    dbc.NavLink('Prediction', href='/prediction', active='exact')
                ],
                vertical=True,
                pills=True
            )
        ],
        style={
            'padding': '20px',
            'height': '100hv',
            'background-color': '#f8f9fa'
        }
    )

    return sidebar