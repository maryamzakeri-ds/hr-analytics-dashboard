from dash import Input, Output
from app import app
from src.data_loader import load_hr_data

df = load_hr_data()

@app.callback(
    Output('total-employees', 'children'),
    Output('attrition-rate', 'children'),
    Output('average-income', 'children'),
    Input('department-filter', 'value'),
    Input('role-filter', 'value'),
    Input('gender-filter', 'value')
)
def update_cards(departemnt, role, gender):
    filtered_df = df.copy()

    if departemnt:
        filtered_df = filtered_df[filtered_df['Department'].isin(departemnt)]

    if role:
        filtered_df = filtered_df[filtered_df['JobRole'].isin(role)]

    if gender:
        filtered_df = filtered_df[filtered_df['Gender'].isin(gender)]

    total_employees = len(filtered_df)
    attrition_rate = (filtered_df['Attrition'] == 'Yes').mean()
    avg_income = filtered_df['MonthlyIncome'].mean()

    return total_employees, f'{attrition_rate:.1%}', f'{avg_income:,.0f}'