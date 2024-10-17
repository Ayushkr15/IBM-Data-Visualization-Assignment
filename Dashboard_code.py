#!/usr/bin/env python
# coding: utf-8

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load the data using pandas
data = pd.read_csv(
    'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv'
)
print("Data loaded successfully. Columns:", data.columns.tolist())

# Initialize the Dash app
app = dash.Dash(__name__, serve_locally=True)  # Serve assets locally

# Create the dropdown menu options
dropdown_options = [
    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
]

# List of years
year_list = sorted(data['Year'].unique())

# Create the layout of the app
app.layout = html.Div([
    # Add title to the dashboard
    html.H1(
        "Automobile Sales Statistics Dashboard",
        style={'color': '#503D36', 'font-size': 24, 'textAlign': 'center'}
    ),
    # Add dropdown menus
    html.Div([
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=dropdown_options,
            value='Yearly Statistics',
            placeholder='Select a Statistics Type'
        )
    ]),
    html.Div(
        dcc.Dropdown(
            id='select-year',
            options=[{'label': i, 'value': i} for i in year_list],
            value=year_list[0] if year_list else None
        )
    ),
    html.Div([
        html.Div(
            id='output-container',
            className='chart-grid',
            style={'display': 'flex', 'flex-direction': 'column'}
        )
    ])
])

# Callback to enable or disable the 'select-year' dropdown based on selected statistics
@app.callback(
    Output(component_id='select-year', component_property='disabled'),
    Input(component_id='dropdown-statistics', component_property='value')
)
def update_input_container(selected_statistics):
    if selected_statistics == 'Yearly Statistics':
        return False
    else:
        return True

# Callback to update the graphs based on selected statistics and year
@app.callback(
    Output(component_id='output-container', component_property='children'),
    [
        Input(component_id='dropdown-statistics', component_property='value'),
        Input(component_id='select-year', component_property='value')
    ]
)
def update_output_container(report_type, selected_year):
    try:
        if report_type == 'Recession Period Statistics':
            # Filter data for recession periods
            recession_data = data[data['Recession'] == 1]

            # Plot 1: Average Automobile Sales fluctuation over Recession Period
            yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
            R_chart1 = dcc.Graph(
                figure=px.line(
                    yearly_rec,
                    x='Year',
                    y='Automobile_Sales',
                    title="Average Automobile Sales During Recession Periods"
                )
            )

            # Plot 2: Average number of vehicles sold by vehicle type
            average_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
            R_chart2 = dcc.Graph(
                figure=px.bar(
                    average_sales,
                    x='Vehicle_Type',
                    y='Automobile_Sales',
                    title="Average Vehicles Sold by Type During Recessions"
                )
            )

            # Plot 3: Total expenditure share by vehicle type during recessions
            exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
            R_chart3 = dcc.Graph(
                figure=px.pie(
                    data_frame=exp_rec,
                    values='Advertising_Expenditure',
                    names='Vehicle_Type',
                    title="Advertising Expenditure Share by Vehicle Type During Recessions"
                )
            )

            # Plot 4: Effect of Unemployment Rate on Vehicle Type and Sales
            unemp_data = recession_data.groupby(['unemployment_rate', 'Vehicle_Type'])['Automobile_Sales'].mean().reset_index()
            R_chart4 = dcc.Graph(
                figure=px.bar(
                    unemp_data,
                    x='unemployment_rate',
                    y='Automobile_Sales',
                    color='Vehicle_Type',
                    labels={
                        'unemployment_rate': 'Unemployment Rate',
                        'Automobile_Sales': 'Average Automobile Sales'
                    },
                    title='Effect of Unemployment Rate on Vehicle Sales by Type'
                )
            )

            return [
                html.Div(
                    className='chart-item',
                    children=[R_chart1, R_chart2],
                    style={'display': 'flex'}
                ),
                html.Div(
                    className='chart-item',
                    children=[R_chart3, R_chart4],
                    style={'display': 'flex'}
                )
            ]

        elif report_type == 'Yearly Statistics' and selected_year:
            # Filter data for the selected year
            yearly_data = data[data['Year'] == selected_year]

            # Plot 1: Monthly Automobile sales for the selected year
            monthly_sales = yearly_data.groupby('Month')['Automobile_Sales'].sum().reset_index()
            Y_chart1 = dcc.Graph(
                figure=px.line(
                    monthly_sales,
                    x='Month',
                    y='Automobile_Sales',
                    title=f"Monthly Automobile Sales in {selected_year}"
                )
            )

            # Plot 2: Average Vehicles Sold by Vehicle Type in the selected year
            avr_vdata = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
            Y_chart2 = dcc.Graph(
                figure=px.bar(
                    avr_vdata,
                    x='Vehicle_Type',
                    y='Automobile_Sales',
                    title=f"Average Vehicles Sold by Type in {selected_year}"
                )
            )

            # Plot 3: Total Advertisement Expenditure by Vehicle Type
            exp_data = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
            Y_chart3 = dcc.Graph(
                figure=px.pie(
                    data_frame=exp_data,
                    names='Vehicle_Type',
                    values='Advertising_Expenditure',
                    title=f"Advertising Expenditure by Type in {selected_year}"
                )
            )

            # Plot 4: Unemployment Rate Impact on Sales
            unemp_data = yearly_data.groupby('unemployment_rate')['Automobile_Sales'].mean().reset_index()
            Y_chart4 = dcc.Graph(
                figure=px.line(
                    unemp_data,
                    x='unemployment_rate',
                    y='Automobile_Sales',
                    title=f"Unemployment Rate vs Automobile Sales in {selected_year}",
                    labels={
                        'unemployment_rate': 'Unemployment Rate',
                        'Automobile_Sales': 'Average Automobile Sales'
                    }
                )
            )

            return [
                html.Div(
                    className='chart-item',
                    children=[Y_chart1, Y_chart2],
                    style={'display': 'flex'}
                ),
                html.Div(
                    className='chart-item',
                    children=[Y_chart3, Y_chart4],
                    style={'display': 'flex'}
                )
            ]

        else:
            return [html.Div("No data to display.")]

    except Exception as e:
        print("Error in update_output_container:", str(e))
        return [html.Div("An error occurred while processing the data.")]

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True, port=8060)
