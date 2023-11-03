import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

# Load the dataset (replace 'YourDataset.csv' with your dataset file)
data = pd.read_csv("dataset/Annual_Surface_Temperature_Change.csv")

# Load the deforestation dataset
deforestation_data = pd.read_csv("dataset/annual-deforestation.csv")

# Sample data for seasonal change
season_data = pd.read_csv('dataset/season-wise-change.csv')
co2_emissions_data = pd.read_csv("dataset/co-emissions-per-capita.csv")
greenhouse = pd.read_csv(r'dataset/AGGI_Table.csv')

# Load the dataset for global threats to biodiversity
threat = pd.read_excel(r'dataset/threats.xlsx')
# Load Heat Content Anomaly data
anomaly_data = pd.read_csv("dataset/anamoly.csv")

# Create a pie chart for threats using Plotly Express
fig_threats = px.pie(threat, names='threats', values='percentage', title='Distribution of Threats to Biodiversity')
fig_threats.update_traces(textinfo='percent+label', pull=[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1],
                          textfont_size=14, marker=dict(
        colors=['#FF6F61', '#6B4226', '#F4A261', '#2A9D8F', '#F76D57', '#4A5359', '#5A4B49',
                '#005D67'], line=dict(color='#ffffff', width=2)))

# Load the hierarchical data from the provided dataset
tree = pd.read_csv(r'dataset/treemap.csv')
def create_indented_hierarchy(df, level_column, category_column, subcategory_column):
    hierarchy = []

    for index, row in df.iterrows():
        level = row[level_column]
        category = row[category_column]
        subcategory = row[subcategory_column]

        indentation = "  " * (level - 1)  # Adjust the number of spaces for indentation as needed
        if category != '-':
            hierarchy.append(f"{indentation}{category}")
        if subcategory != '-':
            hierarchy.append(f"{indentation}  {subcategory}")

    return "\n".join(hierarchy)
indented_hierarchy = create_indented_hierarchy(tree, 'Level', 'Category', 'Subcategory')


# Create a Dash web application
app = dash.Dash(__name__)

# Define the layout of the dashboard and set the background color
app.layout = html.Div(style={'backgroundColor': '#006994'}, children=[
    html.Div([
        html.H1("Visualizing Global Trends In Climate", className="title",
                style={'text-align': 'center', 'color': '#003153'}),
        dcc.Markdown('''
        In recent decades, the world has witnessed a concerning array of global trends in climate change. 
        Rising temperatures, increasingly frequent and severe weather events, and shifting climate patterns 
        have become unmistakable signs of a planet in flux. The burning of fossil fuels, deforestation, and 
        industrial processes have led to a rapid accumulation of greenhouse gases in the atmosphere, intensifying 
        the greenhouse effect and driving global warming. This has triggered a cascade of effects, including the 
        melting of polar ice caps, rising sea levels, and disruptions in ecosystems. The urgent need to address 
        these global trends in climate change has sparked international efforts to reduce emissions, transition to 
        renewable energy sources, and adapt to a changing climate. Understanding and visualizing these trends through 
        data analysis and visualization play a crucial role in informing policy decisions and mobilizing societies 
        to combat the challenges posed by climate change. Following are the data visualized to represent the global trends of climate:
        ''', className="description",
                     style={'text-align': 'center', 'color': '#0072bb', 'font-family': 'Courier New, monospace',
                            'font-size': '16px'}),
        # Links to other visualizations with anchor IDs
        html.Br(),
        html.A('Annual Surface Temperature Change', href='#temperature-section',
               style={'font-size': '16px', 'text-decoration': 'none', 'text-align': 'center'}),
        html.Br(),
        html.A('Annual Deforestation', href='#deforestation-section',
               style={'font-size': '16px', 'text-decoration': 'none', 'text-align': 'center'}),
        html.Br(),
        html.A('Seasonal Temperature Change', href='#season-section',
               style={'font-size': '16px', 'text-decoration': 'none', 'text-align': 'center'}),
        html.Br(),
        html.A('CO2 Emissions per Capita', href='#emissions-section',
               style={'font-size': '16px', 'text-decoration': 'none', 'text-align': 'center'}),
        html.Br(),
        html.A('Global Threats to Biodiversity', href='#threats-section',
               style={'font-size': '16px', 'text-decoration': 'none', 'text-align': 'center'}),
        html.Br(),
        html.A('Heat Content Anomaly', href='#anomaly-section',
               style={'font-size': '16px', 'text-decoration': 'none', 'text-align': 'center'}),
        html.Br(),
        html.A('Green-House gas concentration', href='#greenhouse-section',
               style={'font-size': '16px', 'text-decoration': 'none', 'text-align': 'center'}),
        html.Br(),
        html.A('Hierarchical Visualization', href='#hierarchical-section',
               style={'font-size': '16px', 'text-decoration': 'none', 'text-align': 'center'}),
    ], style={'backgroundColor': 'white', 'borderRadius': '15px', 'padding': '20px', 'margin': '20px','text-align': 'center'}),

    html.Div([
        html.H2("Annual Surface Temperature Change", className="title", id='temperature-section',
                style={'text-align': 'center', 'color': 'teal'}),
        html.P('''This indicator presents the mean surface temperature change during the period 1961-2021, using temperatures between 
                1951 and 1980 as a baseline. This data is provided by the Food and Agriculture 
                Organization Corporate Statistical Database (FAOSTAT) and is based 
                on publicly available GISTEMP data from the National Aeronautics and Space Administration Goddard Institute for Space Studies (NASA GISS).''',
               style={'text-align': 'center', 'color': 'teal'}),
        dcc.Graph(id='temperature-plot', className="visualization"),
        dcc.Dropdown(
            id='country-dropdown',
            options=[{'label': country, 'value': country} for country in data['Country'].unique()],
            value='India'  # Set a default country
        )
    ], style={'backgroundColor': 'white', 'borderRadius': '15px', 'padding': '20px', 'margin': '20px'}),

    html.Div([
        html.H2("Annual Deforestation", id='deforestation-section', className="title",
                style={'text-align': 'center', 'color': 'teal'}),
    html.P('''Net forest loss is not the same as deforestation – it measures deforestation plus any gains in forest over a given period.

                Over the decade since 2010, the net loss in forests globally was 4.7 million hectares per year.1However, deforestation rates were much significantly higher.

                The UN FAO estimate that 10 million hectares of forest were cut down each year.

                This interactive map shows deforestation rates across the world. ''',
               style={'text-align': 'center', 'color': 'teal'}),
        dcc.Graph(id='world-map', className="visualization"),
        dcc.Dropdown(
            id='year-dropdown',
            options=[
                {'label': year, 'value': year} for year in deforestation_data['Year'].unique()
            ],
            value=1990  # Set a default year
        )
    ], style={'backgroundColor': 'white', 'borderRadius': '15px', 'padding': '20px', 'margin': '20px'}),

    html.Div([
        html.H2("Seasonal Temperature Change", id='season-section', className="title",
                style={'text-align': 'center', 'color': 'teal'}),
        html.P('''This figure shows changes in the average temperature for each season across the contiguous 48 
        states from 1896 to 2021. Seasons are defined as follows: winter (December, January, February), spring (March, April,
         May), summer (June, July, August), and fall (September, October, November). This graph uses the 1901–2000 average as 
         a baseline for depicting change. ''',
               style={'text-align': 'center', 'color': 'teal'}),
        dcc.Graph(id='season-plot', className="visualization"),
        dcc.Dropdown(
            id='season-dropdown',
            options=[
                {'label': season, 'value': season} for season in season_data.columns[1:]
            ],
            value='Combined'  # Set a default season
        )
    ], style={'backgroundColor': 'white', 'borderRadius': '15px', 'padding': '20px', 'margin': '20px'}),

    html.Div([  # New section for CO2 emissions visualization
        html.H2("CO2 Emissions per Capita", id='emissions-section', className="title",
                style={'text-align': 'center', 'color': 'teal'}),
        dcc.Graph(id='emissions-map-1956', className="visualization"),
        dcc.Graph(id='emissions-map-2021', className="visualization"),
    ], style={'backgroundColor': 'white', 'borderRadius': '15px', 'padding': '20px', 'margin': '20px'}),

    html.Div([
        html.H2("Global Threats to Biodiversity", id='threats-section', className="title",
                style={'text-align': 'center', 'color': 'teal'}),
    html.P('''More than one in four species on Earth now faces extinction, and that will rise to 50% by the end of
     the century unless urgent action is taken. 37,400
    Scientists have labelled the biodiversity crisis has direct or indirect  relation to climate change. Over 37,000 species are 
    directly threatened with extinction. That is 28 % of all species assessed.
''',
               style={'text-align': 'center', 'color': 'teal'}),
        dcc.Graph(id='threats-pie-chart', figure=fig_threats),
    ], style={'backgroundColor': 'white', 'borderRadius': '15px', 'padding': '20px', 'margin': '20px'}),

    # New section for Heat Content Anomaly bar chart
    html.Div([
        html.H2("Heat Content Anomaly", id='anomaly-section', className="title",
                style={'text-align': 'center', 'color': 'teal'}),
        html.P('''Rising amounts of greenhouse gases are preventing heat radiated from Earth’s surface from 
        escaping into space as freely as it used to. Most of the excess atmospheric heat is passed back to the ocean. 
        As a result, upper ocean heat content has increased significantly over the past few decades. Seasonal (3-month)
         heat energy in the top half-mile of the ocean compared to the 1955-2006 average. Heat content in the global 
         ocean has been consistently above-average (red bars) since the mid-1990s. More than 90 percent of the excess 
         heat trapped in the Earth system due to human-caused global warming has been absorbed by the oceans. 
         NOAA Climate.gov graph, based on data (0-700m) from the NCEI Ocean Heat Content product collection.''',
               style={'text-align': 'center', 'color': 'teal'}),
        dcc.Graph(id='anomaly-bar-chart', className="visualization"),
        html.Button("Update Chart", id="update-button")  # Add an update button
    ], style={'backgroundColor': 'white', 'borderRadius': '15px', 'padding': '20px', 'margin': '20px'}),
    html.Div([
        # Greenhouse Gas Data line plot and area plot
html.H2("Greenhouse Gas Data", className="title", id='greenhouse-section',
                style={'text-align': 'center', 'color': 'teal'}),
    html.P('''Greenhouse gases warm the planet, which can lead to changes in precipitation patterns, storm severity,
 and sea level. For example, a stronger greenhouse effect can warm the oceans and partially melt glaciers and other ice,
  increasing sea level. Ocean water also will expand if it warms, contributing to further sea level rise.''',
               style={'text-align': 'center', 'color': 'teal'}),

        dcc.Dropdown(
            id='gas-dropdown',
            options=[{'label': gas, 'value': gas} for gas in greenhouse.columns[1:7]],
            value='CO2'
        ),
        dcc.Graph(id='line-plot'),
        dcc.Graph(id='total-area-plot')],
        style={'backgroundColor': 'white', 'borderRadius': '15px', 'padding': '20px', 'margin': '20px'}),

    # New section for Hierarchical Visualization
    html.Div([
        html.H2("Solution", id='hierarchical-section', className="title",
                style={'text-align': 'center', 'color': 'teal'}),
        dcc.Markdown(
            "visualization to represent strategies and actions to address the climate change crisis:",
            style={'text-align': 'center', 'color': 'teal'}),
        dcc.Markdown(
            "```plaintext\n" + indented_hierarchy + "\n```",
            style={
                'white-space': 'pre-line',
                'font-family': 'monospace',
                'color': 'teal',
                'border': '2px solid #006994',
                'border-radius': '10px',
                'padding': '10px',
                'background-color': 'lightgray',
                'box-shadow': '5px 5px 5px #888888',
                'font-size': '14px',
            }
        )

    ], style={'backgroundColor': 'white', 'borderRadius': '15px', 'padding': '20px', 'margin': '20px'}),
])

colorscale = [
    [0, 'lightyellow'],
    [1, 'crimson']
]

@app.callback(
    Output('emissions-map-1956', 'figure'),
    Output('emissions-map-2021', 'figure'),
    Input('emissions-map-1956', 'relayoutData'),
    Input('emissions-map-2021', 'relayoutData')
)
def update_emissions_maps(relayoutData1956, relayoutData2021):
    filtered_data_1956 = co2_emissions_data[co2_emissions_data['Year'] == 1956]
    filtered_data_2021 = co2_emissions_data[co2_emissions_data['Year'] == 2021]

    fig_1956 = px.choropleth(filtered_data_1956, locations='Code', color='emissions',
                             hover_name='Entity', title=f'CO2 Emissions per Capita (1956)',
                             color_continuous_scale=colorscale)

    fig_2021 = px.choropleth(filtered_data_2021, locations='Code', color='emissions',
                             hover_name='Entity', title=f'CO2 Emissions per Capita (2021)',
                             color_continuous_scale=colorscale)

    return fig_1956, fig_2021

# Define callback to update the temperature plot based on selected country
@app.callback(
    Output('temperature-plot', 'figure'),
    Input('country-dropdown', 'value')
)
def update_temperature_plot(selected_country):
    filtered_data = data[data['Country'] == selected_country]
    years = [col[1:] for col in filtered_data.columns[10:-1]]
    temperature_change = filtered_data.iloc[:, 10:-1].values[0]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=years, y=temperature_change, mode='lines+markers'))
    fig.update_layout(title=f"Temperature Change Over the Years for {selected_country}",
                      xaxis_title='Year',
                      yaxis_title='Temperature Change')
    return fig

# Define callback to update the world map based on the selected year
@app.callback(
    Output('world-map', 'figure'),
    Input('year-dropdown', 'value')
)
def update_world_map(selected_year):
    filtered_data = deforestation_data[deforestation_data['Year'] == selected_year]
    fig = px.choropleth(filtered_data,
                        locations='Code',
                        color='Deforestation',
                        hover_name='Entity',
                        title=f'Annual Deforestation ({selected_year})',
                        color_continuous_scale='YlGnBu')

    return fig

# Define callback to update the seasonal data plot based on selected season
@app.callback(
    Output('season-plot', 'figure'),
    Input('season-dropdown', 'value')
)
def update_season_plot(selected_season):
    xaxis_ranges = None  # You can add x-axis ranges if needed for the seasonal data plot

    if selected_season == 'Combined':
        fig = go.Figure()
        for season in season_data.columns[1:]:
            fig.add_trace(go.Scatter(x=season_data['Year'], y=season_data[season], mode='lines+markers', name=season))
    else:
        fig = go.Figure(go.Scatter(x=season_data['Year'], y=season_data[selected_season], mode='lines+markers'))

    fig.update_layout(title=f"Seasonal Data for {selected_season}",
                      xaxis_title='Year',
                      yaxis_title='Value')

    if xaxis_ranges:
        fig.update_xaxes(range=xaxis_ranges)

    return fig

@app.callback(
    Output('anomaly-bar-chart', 'figure'),
    [Input('update-button', 'n_clicks')]  # Added an input component (update button)
)
def update_anomaly_bar_chart(n_clicks):
    fig = go.Figure()

    for year in anomaly_data['year'].unique():
        for month in [3, 6, 9, 12]:
            filtered_data = anomaly_data[(anomaly_data['year'] == year) & (anomaly_data['month'] == month)]

            if not filtered_data.empty:  # Check if filtered_data is not empty
                color = 'red' if filtered_data['anamoly'].values[0] < 0 else 'green'
                label = f"{month}/{year}"

                fig.add_trace(go.Bar(x=[label], y=[filtered_data['anamoly'].values[0]],
                                     marker_color=color))

    fig.update_layout(title="Heat Content Anomaly",
                      xaxis_title='Year/Month',
                      yaxis_title='Anomaly',
                      xaxis={'categoryorder': 'total ascending'},
                      showlegend=False)

    return fig
# Define callback to update line plot
@app.callback(
    Output('line-plot', 'figure'),
    [Input('gas-dropdown', 'value')]
)
def update_line_plot(selected_gas):
    fig = go.Figure()
    for gas in greenhouse.columns[1:7]:
        if gas == selected_gas:
            fig.add_trace(go.Scatter(x=greenhouse['Year'], y=greenhouse[gas], mode='lines', name=gas, line=dict(width=2)))
        else:
            fig.add_trace(go.Scatter(x=greenhouse['Year'], y=greenhouse[gas], mode='lines', name=gas, line=dict(width=0.5)))

    fig.update_layout(title=f"{selected_gas} Concentration Over Time",
                      xaxis_title="Year",
                      yaxis_title=f"{selected_gas} Concentration (ppm)")
    return fig

# Define callback to update area plot
@app.callback(
    Output('total-area-plot', 'figure'),
    [Input('gas-dropdown', 'value')]
)
def update_total_area_plot(selected_gas):
    total_concentration = greenhouse.iloc[:, 1:7].sum(axis=1)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=greenhouse['Year'], y=total_concentration, fill='tozeroy', name='Total Concentration', line=dict(width=2)))
    fig.update_layout(title=f"Total Concentration of Greenhouse Gases Over Time",
                      xaxis_title="Year",
                      yaxis_title="Total Concentration (ppm)")
    return fig




if __name__ == '__main__':
    app.run_server(debug=True)