import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from components.sidebar import create_sidebar

app = dash.Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)

app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(create_sidebar(), width=3),
                dbc.Col(dash.page_container, width=9)
            ]
        )
    ],
    fluid=True
)

import callbacks.overview_callbacks

if __name__ == '__main__':
    app.run(debug=True)