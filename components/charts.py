import plotly.express as px

def attrition_by_department(df):
    data = (
        df.groupby('Department')['Attrition']
        .apply(lambda x: (x == 'Yes').mean())
        .reset_index()
    )

    data.columns = ['Department', 'Attrition Rate']

    fig = px.bar(
        data,
        x='Department',
        y='Attrition Rate',
        title='Attrition Rate by Department'
    )

    fig.update_yaxes(tickformat='.0%')
    return fig

def attrition_by_role(df):
    data = (
        df.groupby('JobRole')['Attrition']
        .apply(lambda x: (x == 'Yes').mean())
        .reset_index()
    )

    data.columns = ['Job Role', 'Attrition Rate']

    fig = px.bar(
        data, 
        x='Job Role',
        y='Attrition Rate',
        title='Attrition Rate by Job Role'
    )

    fig.update_yaxes(tickformat='.0%')
    return fig

def age_distribution(df):
    fig = px.histogram(
        df, 
        x='Age',
        nbins=20,
        title='Employee Age Distribution'
    )
    return fig
