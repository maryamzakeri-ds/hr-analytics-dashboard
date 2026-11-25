from dash import Dash, Input, Output, State, dash_table, dcc, html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestClassifier

df = pd.read_csv("data/IBM-HR-Analytics-Employee-Attrition-and-Performance.csv")
df["AttritionFlag"] = (df["Attrition"] == "Yes").astype(int)     
df["AgeBand"] = pd.cut(df["Age"], [17, 25, 35, 45, 55, 100], labels=["<=25", "26-35", "36-45", "46-55", "55+"])
df["IncomeBand"] = pd.qcut(df["MonthlyIncome"], 4, labels=["Q1 low", "Q2", "Q3", "Q4 high"])

app = Dash(__name__)

CARD_STYLE = {"background": "#f4f6fa", "padding": "12px 16px", "borderRadius": "8px", "flex": "1"}
def create_kpi(id, title):
    kpi = html.Div(
        [
            html.Div(
                title,
                style={"color": "#666", "fontSize": "13px"}
            ),
            html.H2(id=id, style={"margin": "4px 0 0 0"})
        ],
        style=CARD_STYLE
    )
    return kpi

sidebar = html.Div(
    [
        html.H3("Filters"),
        html.Label("Department"),
        dcc.Dropdown(
            id="filter-department",
            options=sorted(df["Department"].unique()),
            value=sorted(df["Department"].unique()),
            multi=True
        ),
        html.Br(),
        html.Label("Gender"),
        dcc.Dropdown(
            id="filter-gender",
            options=sorted(df["Gender"].unique()),
            value=sorted(df["Gender"].unique()),
            multi=True,
        ),
        html.Br(),
        html.Label("Age"),
        dcc.RangeSlider(
            id="filter-age",
            min=int(df["Age"].min()),
            max=df["Age"].max(),
            step=1,
            value=[int(df["Age"].min()), int(df["Age"].max())],
            marks={a: str(a) for a in range(20, 61, 10)},
            tooltip={"placement": "bottom", "always_visible": False}
        )
    ],
    style={"width": "250px", "padding": "16px", "background": "#fafafa", "minHeight": "100vh"}
)

tab_overview = html.Div(
    [
        html.Div(
            [
                dcc.Graph(id="age-graph"),
                dcc.Graph(id="department-graph"),
            ],
            # style={"display": "flex"}
        ),
        dcc.Graph(id="role-graph")
    ]
)

DIMS = ["OverTime", "BusinessTravel", "AgeBand", "MaritalStatus", "Department", "JobLevel", "IncomeBand", "Gender"]
tab_drivers = html.Div(
    [
        html.Label("Break attrition by:"),
        dcc.Dropdown(id="dim", options=DIMS, value="OverTime", clearable=False, style={"width": "300px"}),
        dcc.Graph(id="drivers-graph"),
        html.Div(id="insight", style={"background": "#e8f1fb", "padding": "10px", "borderRadius": "6px"})
    ],
    style={"padding": "16px"}
)

tab_comp = html.Div(
    [
        html.Div(
            [
                dcc.Graph("box-graph"),
                dcc.Graph("scatter-graph"),
            ],
            # style={"display": "flex"}
        ),
        dcc.Graph("gender-graph")
    ]
)

tab_sat = html.Div(
    [
        dcc.Graph("heat-graph"),
        dcc.Graph("corr-graph")
    ]
)

X = pd.get_dummies(df.drop(columns=["Attrition", "AttritionFlag", "EmployeeNumber", "AgeBand", "IncomeBand"]), drop_first=True)
y = df["AttritionFlag"]
rf_model = RandomForestClassifier(n_estimators=200, random_state=42, class_weight="balanced")
rf_model.fit(X, y)
feature_importance = (pd.Series(rf_model.feature_importances_, index=X.columns)
                        .sort_values()
                        .tail(10)
                        .reset_index(name="importance")
                        .rename(columns={"index": "feature"}))

fig_model = px.bar(feature_importance, x="importance", y="feature", orientation="h", title="Top 10 attrition predictors (Random Forest)")
tab_model = html.Div(
    [
        dcc.Graph(id="model-graph", figure=fig_model),
        html.Button("Download filtered CSV", id="btn-dl"),
        dcc.Download(id="download"),
        dash_table.DataTable(id="table", columns=[{"name": c, "id": c} for c in df.columns], page_size=10, style_table={"overflowX": "auto"})
    ],
    style={"padding": "16px"}
)

app.layout = html.Div(
    [
        sidebar,
        html.Div(
            [
                html.H1("HR Analytics Dashboard"),
                html.Div(
                    [
                        create_kpi("k-head", "Headcount"),
                        create_kpi("k-attr", "Attrition Rate"),
                        create_kpi("k-inc", "Average Monthly Income"),
                        create_kpi("k-ten", "Average Tenure (years)")
                    ],
                    style={"display": "flex", "gap": "12px"}
                ),
                dcc.Tabs(
                    [
                        dcc.Tab(tab_overview, label="Overview"),
                        dcc.Tab(tab_drivers, label="Attrition Drivers"),
                        dcc.Tab(tab_comp, label="Compensation"),
                        dcc.Tab(tab_sat, label="Satisfaction"),
                        dcc.Tab(tab_model, label="Model & Data"),
                    ],
                    style={"marginTop": "16px"}
                )
            ],
            style={"flex": "1", "padding": "16px", "minWidth": "0"}   
        )
    ],
    style={"display": "flex", "fontFamily": "sans-serif"}
)


def empty_fig(msg="No data for these filters"):
    return go.Figure().update_layout(title=msg)

def attrition_by(f, col):
    g = f.groupby(col)["AttritionFlag"].agg(["mean", "count"]).reset_index()
    g["Attrition %"] = (g["mean"] * 100).round(1)
    return g
    

@app.callback(
    Output("k-head", "children"),
    Output("k-attr", "children"),
    Output("k-inc", "children"),
    Output("k-ten", "children"),
    Input("filter-department", "value"),
    Input("filter-gender", "value"),
    Input("filter-age", "value")
)
def update_cards(department, gender, age):
    filtered_df = df[df["Department"].isin(department or []) & df["Gender"].isin(gender or [])& df["Age"].between(age[0], age[1])]
    if filtered_df.empty:
        return 0, "-", "-", "-"

    headcount = len(filtered_df)
    attrition_rate = round((filtered_df['AttritionFlag'] == 1).mean(), 2)
    avg_monthly_income = round(filtered_df["MonthlyIncome"].mean(), 2)
    avg_tenure = round(filtered_df["YearsAtCompany"].mean(), 2)

    return headcount, attrition_rate  , avg_monthly_income, avg_tenure,

@app.callback(
    Output("age-graph", "figure"),
    Output("department-graph", "figure"),
    Output("role-graph", "figure"),
    Input("filter-department", "value"),
    Input("filter-gender", "value"),
    Input("filter-age", "value")
)
def update_overview(department, gender, age):
    filtered_df = df[df["Department"].isin(department or []) & df["Gender"].isin(gender or [])& df["Age"].between(age[0], age[1])]
    if filtered_df.empty:
        return empty_fig(), empty_fig(), empty_fig()


    age_graph = px.histogram(filtered_df, x="Age", color="Attrition", nbins=25, barmode="overlay", title="Age distribution by attrition")
    dept_graph = px.pie(filtered_df, names="Department", hole=.4, title="Headcount by department")
    role = attrition_by(filtered_df, "JobRole").sort_values("mean")
    role_graph = px.bar(role, x="Attrition %", y="JobRole", orientation="h", text="Attrition %", title="Attrition by job role")

    return age_graph, dept_graph, role_graph

@app.callback(
    Output("drivers-graph", "figure"),
    Output("insight", "children"),
    Input("dim", "value"),
    Input("filter-department", "value"),
    Input("filter-gender", "value"),
    Input("filter-age", "value")
)
def update_drivers(dim, department, gender, age):
    filtered_df = df[df["Department"].isin(department or []) & df["Gender"].isin(gender or [])& df["Age"].between(age[0], age[1])]
    if filtered_df.empty:
        return empty_fig(), ""

    g = attrition_by(filtered_df, dim)
    fig = px.bar(g, x=dim, y="Attrition %", text="Attrition %", hover_data=["count"], title=f"Attrition % by {dim}")
    top = g.sort_values("Attrition %", ascending=False).iloc[0]
    msg = (f"Highest attrition in {dim} = {top[dim]}: {top['Attrition %']}% "
            f"(overall {filtered_df.AttritionFlag.mean():.1%}), count={int(top['count'])}")
    return fig, msg

@app.callback(
    Output("box-graph", "figure"),
    Output("scatter-graph", "figure"),
    Output("gender-graph", "figure"),
    Input("filter-department", "value"),
    Input("filter-gender", "value"),
    Input("filter-age", "value")
)
def update_compensation(department, gender, age):
    filtered_df = df[df["Department"].isin(department or []) & df["Gender"].isin(gender or [])& df["Age"].between(age[0], age[1])]
    if filtered_df.empty:
        return empty_fig(), empty_fig(), empty_fig()

    box_graph = px.box(filtered_df, x="JobLevel", y="MonthlyIncome", color="Attrition", title="Income by Job Level")
    scatter_graph = px.scatter(filtered_df, x="TotalWorkingYears", y="MonthlyIncome", color="Attrition",
                      opacity=.6, title="Income vs Experience")
    gap = filtered_df.groupby("Gender")["MonthlyIncome"].mean().round(0).reset_index()
    gender_graph = px.bar(gap, x="Gender", y="MonthlyIncome", text="MonthlyIncome",
                   title="Average Income by Gender (not controlled for level)")

    return box_graph, scatter_graph, gender_graph

@app.callback(
    Output("heat-graph", "figure"),
    Output("corr-graph", "figure"),
    Input("filter-department", "value"),
    Input("filter-gender", "value"),
    Input("filter-age", "value")
)
def update_satisfaction(department, gender, age):
    filtered_df = df[df["Department"].isin(department or []) & df["Gender"].isin(gender or [])& df["Age"].between(age[0], age[1])]
    if filtered_df.empty:
        return empty_fig(), empty_fig()

    pv = filtered_df.pivot_table(index="JobSatisfaction", columns="WorkLifeBalance", values="AttritionFlag", aggfunc="mean").mul(100).round(1)
    heat_graph = px.imshow(pv, text_auto=True, color_continuous_scale="Reds", aspect="auto", title="Attrition % : JobSatisfaction × WorkLifeBalance")
    num = filtered_df.select_dtypes("number").drop(columns=["EmployeeNumber"])
    corr_graph = px.imshow(num.corr().round(2), text_auto=True, color_continuous_scale="RdBu_r", zmin=-1, zmax=1, title="Correlation matrix")
    return heat_graph, corr_graph

@app.callback(
    Output("table", "data"),
    Input("filter-department", "value"),
    Input("filter-gender", "value"),
    Input("filter-age", "value")
)
def update_data(department, gender, age):
    filtered_df = df[df["Department"].isin(department or []) & df["Gender"].isin(gender or [])& df["Age"].between(age[0], age[1])]
    if filtered_df.empty:
        return [[]]

    return filtered_df.to_dict("records")

@app.callback(
    Output("download", "data"),
    Input("btn-dl", "n_clicks"),
    State("filter-department", "value"),
    State("filter-gender", "value"), 
    State("filter-age", "value"),
    prevent_initial_call=True
)
def download(n_clicks, department, gender, age):
    filtered_df = df[df["Department"].isin(department or []) & df["Gender"].isin(gender or [])& df["Age"].between(age[0], age[1])]
    return dcc.send_data_frame(filtered_df.to_csv, "hr_filtered.csv", index=False)

if __name__ == "__main__":
    app.run(debug=True)