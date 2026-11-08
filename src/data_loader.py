import pandas as pd

def load_hr_data():
    df = pd.read_csv('data/raw/IBM-HR-Analytics-Employee-Attrition-and-Performance.csv')
    return df