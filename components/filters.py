from dash import html, dcc
import dash_bootstrap_components as dbc

def create_filter(label, component_id, options):
    filter = dbc.Col(
        [
            html.Label(label),
            dcc.Dropdown(
                id=component_id,
                options=[
                    {
                        'label': item, 'value': item
                    }
                    for item in options
                ],
                multi=True,
                placeholder=f'Select {label}'
            )
        ],
        width=4
    )
    return filter