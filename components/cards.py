from dash import html
import dash_bootstrap_components as dbc

def create_card(title, card_id):
    return dbc.Card(
        [
            dbc.CardBody(
                [
                    html.H6(title),
                    html.H3(id=card_id)
                ]
            )
        ],
        className='shadow-sm'
    )