import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from src.data_loader import load_hr_data
from components.cards import create_card
from components.charts import attrition_by_department, attrition_by_role, age_distribution
from components.filters import create_filter

dash.register_page(__name__, path="/")

df = load_hr_data()

layout = dbc.Container(
    [
        html.H2('Executive Overview'),
        dbc.Row(
            [
                create_filter('Department', 'department-filter', df['Department'].unique()),
                create_filter('Job Role', 'role-filter', df['JobRole'].unique()),
                create_filter('Gender', 'gender-filter', df['Gender'].unique())
            ]
        ),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(create_card('Total Employees', 'total-employees'), width=4),
                dbc.Col(create_card('Attrition Rate', 'attrition-rate'), width=4),
                dbc.Col(create_card('Average Income', 'average-income'), width=4),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(dcc.Graph(figure=attrition_by_department(df)), width=6),
                dbc.Col(dcc.Graph(figure=attrition_by_role(df)), width=6),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(dcc.Graph(figure=age_distribution(df)), width=12)
            ]
        )

    ],
    fluid=True
)