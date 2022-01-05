import dash
from dash import dash_table
from dash.dependencies import Input, Output, State
from dash import dcc
from dash import html

import pandas as pd
import numpy as np

# plotly 
import plotly.express as px
import plotly.graph_objects as go



# load data
df = pd.read_csv('data/GameSales_cleaned.csv')
df = df.dropna(axis=0, subset=['Plat_Brand'])
genres = np.sort(df['Genre'].unique().astype(str))
publishers = np.sort(df['Publisher'].unique().astype(str))

genre_options = [{'label' : i, 'value' : i} for i in genres]
publisher_options = [{'label': i, 'value': i} for i in publishers]

# Defaults
DEFAULT_USER_REVIEW = [0, 10]
DEFAULT_CRITICS_REVIEW = [0, 100]
DEFAULT_YEARS = [1994, 2016]
DEFAULT_SALES = [0, df['Global_Sales'].max()]
COLOR_MAP = {'Microsoft': '#107C10', 'Sony': '#003791', 'Nintendo': '#fe0016'}

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div(
    [
        dcc.Store(id='aggregate_data'),
        html.Div(
            [
                html.Div(
                    [
                        html.H2(
                            'Game Across Platforms',
                        )
                    ],
                    className='eight columns'
                )
            ],
            id="header",
            className='row',
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.P(
                            'Filter by release year:',
                            className="control_label"
                        ),
                        dcc.RangeSlider(
                            id='year_slider',
                            min=DEFAULT_YEARS[0],
                            max=DEFAULT_YEARS[1],
                            value=DEFAULT_YEARS,
                            marks={year : year for year in DEFAULT_YEARS},
                            tooltip={"placement": "bottom", "always_visible": True},
                            className="dcc_control"
                        ),

                        html.P(
                            'Filter by region:',
                            className="control_label"
                        ),
                        dcc.RadioItems(
                            id='region_radio',
                            options=[
                                {'label': 'All', 'value': 'Global_Sales'},
                                {'label': 'North America',
                                    'value': 'NA_Sales'},
                                {'label': 'Europe',
                                    'value': 'EU_Sales'},
                                {'label': 'Japan',
                                 'value': 'JP_Sales'},
                            ],
                            value='Global_Sales',
                            labelStyle={'display': 'inline-block'},
                            className="dcc_control"
                        ),

                        html.P(
                            'Filter by game genre:',
                            className="control_label"
                        ),
                        # dcc.RadioItems(
                        #     id='well_status_selector',
                        #     options=[
                        #         {'label': 'All ', 'value': 'all'},
                        #         {'label': 'Active only ', 'value': 'active'},
                        #         {'label': 'Customize ', 'value': 'custom'}
                        #     ],
                        #     value='active',
                        #     labelStyle={'display': 'inline-block'},
                        #     className="dcc_control"
                        # ),
                        dcc.Dropdown(
                            id='genres_dropdown',
                            options=genre_options,
                            multi=True,
                            value=[],
                            className="dcc_control"
                        ),
                        # dcc.Checklist(
                        #     id='lock_selector',
                        #     options=[
                        #         {'label': 'Lock camera', 'value': 'locked'}
                        #     ],
                        #     values=[],
                        #     className="dcc_control"
                        # ),f
                        html.P(
                            'Filter by publisher:',
                            className="control_label"
                        ),
                        # dcc.RadioItems(
                        #     id='publishers_radio',
                        #     options=[
                        #         {'label': 'All ', 'value': 'all'},
                        #         {'label': 'Productive only ',
                        #             'value': 'productive'},
                        #         {'label': 'Customize ', 'value': 'custom'}
                        #     ],
                        #     value='productive',
                        #     labelStyle={'display': 'inline-block'},
                        #     className="dcc_control"
                        # ),
                        dcc.Dropdown(
                            id='publishers_dropdown',
                            options=publisher_options,
                            multi=True,
                            value=[],
                            className="dcc_control"
                        ),
                        html.P(
                            'Filter by user reviews:',
                            className="control_label"
                        ),
                        dcc.RangeSlider(
                            id='user_review_slider',
                            min=0,
                            max=10,
                            value=[0, 10],
                            className="dcc_control",
                            marks={review : review for review in DEFAULT_USER_REVIEW},
                            tooltip={"placement": "bottom", "always_visible": True}
                        ),
                        html.P(
                            'Filter by critic reviews:',
                            className="control_label"
                        ),
                        dcc.RangeSlider(
                            id='critics_review_slider',
                            min=0,
                            max=100,
                            value=[0, 100],
                            className="dcc_control",
                            marks={review : review for review in DEFAULT_CRITICS_REVIEW},
                            tooltip={"placement": "bottom", "always_visible": True}
                        ),
                        html.P(
                            'Filter by Copies Sold:',
                            className="control_label"
                        ),
                        dcc.RangeSlider(
                            id='sales_slider',
                            min=0,
                            max=df['Global_Sales'].max(),
                            value=[0, df['Global_Sales'].max()],
                            className="dcc_control",
                            marks={
                                sales : sales for sales in DEFAULT_SALES},
                            tooltip={"placement": "bottom",
                                     "always_visible": True}
                        ),

                    ],
                    className="pretty_container four columns"
                ),
                html.Div(
                    [
                        html.Div(
                            [

                                html.Div(
                                    [

                                    ],
                                    id="tripleContainer",
                                ),
                            ],
                            id="infoContainer",
                            className="row"
                        ),

                        html.Div([html.Div(
                        [
                            html.Div(
                                [
                                    html.P("Total Sales", style={'fontSize': 25}),
                                    html.H6(
                                        id="total_text",
                                        className="info_text",
                                        style={'fontSize': 25}
                                        ),
                                    dcc.Graph(
                                        id='donut_graph',
                                    )
                                ],
                                id="donut_graph_container",
                                className="four columns"
                            ),

                            html.Div(
                                [
                                    html.P("Average Critic Score", style={'fontSize': 25}),
                                    html.H6(
                                        id="critic_score_text",
                                        className="info_text",
                                        style={'fontSize': 25}
                                    ),
                                    dcc.Graph(
                                        id='critics_review_bar',
                                    )
                                ],
                                id="critics_review_bar_container",
                                className="four columns"
                            ),
                            html.Div(
                                [   
                                    html.P("Average User Score", style={'fontSize': 25}),
                                    html.H6(
                                        id="user_score_text",
                                        className="info_text",
                                        style={'fontSize': 25}
                                    ),
                                    dcc.Graph(
                                        id='user_review_bar',
                                    )
                                ],
                                id="user_review_bar_container",
                                className="four columns"
                            ),
                        ],
                        id="donutbar",
                        className="row"
                        ),
                        
                        ],
                        className='pretty_container'),
                    ],
                    id="rightCol",
                    className="six columns"
                )
            ],
            className="row"
        ),
        html.Div(
            [
                html.Div(
                    [
                        dcc.Graph(
                            id='line_graph',
                        )
                    ],
                    className='pretty_container ten columns',
                ),
            ],
            className='row'
        ),
        
        html.Div(
            [
                
                html.Div(
                    [
                        dcc.Graph(id='heatmap'),
                        
                    ],
                    className='pretty_container four columns',
                ),

                html.Div(
                    [
                        html.H6(
                                        id="data_table_title",
                                        className="info_text",
                                        style={'fontSize': 25}
                                    ),
                        html.Div( id="data_table")
                    ],
                    id="data_table_division",
                    className='pretty_container six columns'
                )
            ],
            className='row'
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                dcc.RadioItems(
                                    id='review_radio',
                                    options=[
                                        {'label': 'User', 'value': 'User'},
                                        {'label': 'Critics',
                                         'value': 'Critics'},
                                    ],
                                    value='User',
                                    labelStyle={'display': 'inline-block'},
                                    className="dcc_control"
                                ),
                                dcc.Graph(id='boxplot')
                            ],
                            className='seven columns',
                        ),
                        html.Div(
                            [
                                dcc.Graph(id='scatterplot')
                            ],
                            className='four columns',
                        ),
                    ],
                    className='pretty_container ten columns'
                )
            ],
            className='row'
        ),
    ],
    id="mainContainer",
    style={
        "display": "flex",
        "flex-direction": "column"
    }
)


# Create callbacks

# Total Sales
@app.callback(Output('total_text', 'children'),
              [Input('year_slider', 'value'),
               Input('user_review_slider', 'value'),
               Input('critics_review_slider', 'value'),
               Input('genres_dropdown', 'value'),
               Input('publishers_dropdown', 'value'),
               Input('sales_slider', 'value'),
               Input('region_radio', 'value')])

def update_sales(year_slider, user_review_slider, critics_review_slider, genres_dropdown, publishers_dropdown, sales_slider, region_radio):
    filtered_df = filter_dataframe(df, genres_dropdown, publishers_dropdown, user_review_slider, critics_review_slider, year_slider, sales_slider)
    total_sales = round(filtered_df[region_radio].sum(),2)
    return str(f'{total_sales} Mi Copies')

# Average Critic Score
@app.callback(Output('critic_score_text', 'children'),
              [Input('year_slider', 'value'),
               Input('user_review_slider', 'value'),
               Input('critics_review_slider', 'value'),
               Input('genres_dropdown', 'value'),
               Input('publishers_dropdown', 'value'),
               Input('sales_slider', 'value'),
               Input('region_radio', 'value')])

def update_sales(year_slider, user_review_slider, critics_review_slider, genres_dropdown, publishers_dropdown, sales_slider, region_radio):
    filtered_df = filter_dataframe(df, genres_dropdown, publishers_dropdown, user_review_slider, critics_review_slider, year_slider, sales_slider)
    avg_critic_score = round(
        filtered_df['Critic_Score'].mean(), 2)
    return str(f'{avg_critic_score}/100')

# Average User Score

@app.callback(Output('user_score_text', 'children'),
              [Input('year_slider', 'value'),
               Input('user_review_slider', 'value'),
               Input('critics_review_slider', 'value'),
               Input('genres_dropdown', 'value'),
               Input('publishers_dropdown', 'value'),
               Input('sales_slider', 'value'),
               Input('region_radio', 'value')])
def update_sales(year_slider, user_review_slider, critics_review_slider, genres_dropdown, publishers_dropdown, sales_slider, region_radio):
    filtered_df = filter_dataframe(
        df, genres_dropdown, publishers_dropdown, user_review_slider, critics_review_slider, year_slider, sales_slider)
    avg_user_score = round(filtered_df['User_Score'].mean(), 2)
    return str(f'{avg_user_score}/10')

# NINTENDO Sales


# @app.callback(Output('NINTENDO_text', 'children'),
#               [Input('year_slider', 'value'),
#                Input('user_review_slider', 'value'),
#                Input('critics_review_slider', 'value'),
#                Input('genres_dropdown', 'value'),
#                Input('publishers_dropdown', 'value'),
#                Input('sales_slider', 'value'),
#                Input('region_radio', 'value')])
# def update_sales(year_slider, user_review_slider, critics_review_slider, genres_dropdown, publishers_dropdown, sales_slider, region_radio):
#     filtered_df = filter_dataframe(
#         df, genres_dropdown, publishers_dropdown, user_review_slider, critics_review_slider, year_slider, sales_slider)
#     total_sales = round(
#         filtered_df.loc[filtered_df['Plat_Brand'] == 'Nintendo'][region_radio].sum(), 2)
#     return str(f'{total_sales} Mi Copies')

# Line plot
@app.callback(Output('line_graph', 'figure'),
              [Input('year_slider', 'value'),
               Input('user_review_slider', 'value'),
               Input('critics_review_slider', 'value'),
               Input('genres_dropdown', 'value'),
               Input('publishers_dropdown', 'value'),
               Input('sales_slider', 'value'),
               Input('region_radio', 'value')])

def update_line_graph(year_slider, user_review_slider, critics_review_slider, genres_dropdown, publishers_dropdown, sales_slider, region_radio):
    line_graph_df = filter_dataframe(df, genres_dropdown, publishers_dropdown, user_review_slider, critics_review_slider, year_slider, sales_slider)
    chart_df = pd.DataFrame(line_graph_df.groupby('Year_of_Release')[region_radio].sum())
    for each in df['Plat_Brand'].unique():
        chart_df[region_radio + '_%s' % each] = line_graph_df[line_graph_df['Plat_Brand'] == each].groupby(
            'Year_of_Release')[region_radio].sum()
    fig = px.line(chart_df, x=chart_df.index, y=[region_radio, '%s_Nintendo'%region_radio, '%s_Microsoft'%region_radio,
                  '%s_Sony' % region_radio], title=f'Game Sales by Platform {year_slider[0]} - {year_slider[1]}'
                  )
    fig.update_layout(
                    yaxis= dict(
                        title='Sales',
                    ),
                    legend_title=''
                    )
    return fig

# boxplot
@app.callback(Output('boxplot', 'figure'),
              [Input('year_slider', 'value'),
               Input('user_review_slider', 'value'),
               Input('critics_review_slider', 'value'),
               Input('genres_dropdown', 'value'),
               Input('publishers_dropdown', 'value'),
               Input('sales_slider', 'value'),
               Input('region_radio', 'value'),
               Input('review_radio','value')])
def box_control(year_slider, user_review_slider, critics_review_slider, genres_dropdown, publishers_dropdown, sales_slider, region_radio, review_radio):
    if review_radio == 'User':
        return update_box2(year_slider, user_review_slider, critics_review_slider, genres_dropdown, publishers_dropdown, sales_slider)
    return update_box(year_slider, user_review_slider, critics_review_slider, genres_dropdown, publishers_dropdown, sales_slider)

def update_box(year_slider, user_review_slider, critics_review_slider, genres_dropdown, publishers_dropdown, sales_slider):
    boxplot_df = filter_dataframe(df, genres_dropdown, publishers_dropdown, user_review_slider, critics_review_slider, year_slider, sales_slider)
    # fig = px.histogram(histogram_df, x='Critic_Score', title='Distribution of Games by Critic Score', nbins=20)
    fig = px.box(boxplot_df,
                    x='Genre', 
                    y='Critic_Score', 
                    color='Plat_Brand', 
                    title='Critic Score by Genre and Platform')
    fig.update_xaxes(title='')
    fig.update_yaxes(title='')
    return fig

def update_box2(year_slider, user_review_slider, critics_review_slider, genres_dropdown, publishers_dropdown, sales_slider):
    boxplot_df = filter_dataframe(df, genres_dropdown, publishers_dropdown, user_review_slider, critics_review_slider, year_slider, sales_slider)
    # fig = px.histogram(histogram_df, x='Critic_Score', title='Distribution of Games by Critic Score', nbins=20)
    fig = px.box(boxplot_df,
                    x='Genre', 
                    y='User_Score', 
                    color='Plat_Brand', 
                    title='User Score by Genre and Platform')
    fig.update_xaxes(title='')
    fig.update_yaxes(title='')
    return fig

# Heatmap
@app.callback(Output('heatmap', 'figure'),
              [Input('year_slider', 'value'),
               Input('user_review_slider', 'value'),
               Input('critics_review_slider', 'value'),
               Input('genres_dropdown', 'value'),
               Input('publishers_dropdown', 'value'),
               Input('sales_slider', 'value'),
               Input('region_radio', 'value')])

def update_heatmap(year_slider, user_review_slider, critics_review_slider, genres_dropdown, publishers_dropdown, sales_slider, region_radio):
    heatmap_df = filter_dataframe(df, genres_dropdown, publishers_dropdown, user_review_slider, critics_review_slider, year_slider, sales_slider)
    chart_df = pd.crosstab(heatmap_df['Plat_Brand'], heatmap_df['Genre'], heatmap_df['Global_Sales'], aggfunc=np.mean)
    fig = px.imshow(chart_df, title='Average Sales by Genre')
    return fig

# Donut Graph


@app.callback(Output('donut_graph', 'figure'),
              [Input('year_slider', 'value'),
               Input('user_review_slider', 'value'),
               Input('critics_review_slider', 'value'),
               Input('genres_dropdown', 'value'),
               Input('publishers_dropdown', 'value'),
               Input('sales_slider', 'value'),
               Input('region_radio', 'value')])
def update_donut_graph(year_slider, user_review_slider, critics_review_slider, genres_dropdown, publishers_dropdown, sales_slider, region_radio):
    donut_graph_df = filter_dataframe(df, genres_dropdown, publishers_dropdown,
                                     user_review_slider, critics_review_slider, year_slider, sales_slider)
    fig = px.pie(donut_graph_df, values=region_radio, names='Plat_Brand', color='Plat_Brand', color_discrete_map=COLOR_MAP, title='Market Share')
    fig.update_traces(hole=.6)

    # Change the margin of the graph and the background color
    fig.update_layout(
    margin=dict(l=40, r=40, t=40, b=40),
    plot_bgcolor='rgba(0,0,0,0)')
    # fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
    # fig.update_layout(
    #     yaxis=dict(
    #         title='Sales',
    #     ),
    #     legend_title=''
    # )
    return fig

# Scatter Plot
@app.callback(Output('scatterplot', 'figure'),
              [Input('year_slider', 'value'),
               Input('user_review_slider', 'value'),
               Input('critics_review_slider', 'value'),
               Input('genres_dropdown', 'value'),
               Input('publishers_dropdown', 'value'),
               Input('sales_slider', 'value'),
               Input('region_radio', 'value'),
               Input('review_radio','value')])
def scatter_control(year_slider, user_review_slider, critics_review_slider, genres_dropdown, publishers_dropdown, sales_slider, region_radio, review_radio):
    if review_radio == 'User':
        return update_scatter2(year_slider, user_review_slider, critics_review_slider, genres_dropdown, publishers_dropdown, sales_slider, region_radio)
    return update_scatter(year_slider, user_review_slider, critics_review_slider, genres_dropdown, publishers_dropdown, sales_slider, region_radio)

def update_scatter(year_slider, user_review_slider, critics_review_slider, genres_dropdown, publishers_dropdown, sales_slider, region_radio):
    scatterData = filter_dataframe(df, genres_dropdown, publishers_dropdown, user_review_slider, critics_review_slider, year_slider, sales_slider)
    fig = px.scatter(scatterData, 
                        x="Critic_Score",
                        y=region_radio,
                        hover_data=['Name', 'Genre'],
                        color='Plat_Brand',
                        title=f'{region_radio} vs Critic_Score', 
                        color_discrete_map=COLOR_MAP,
                        # width=550, 
                        # height=550
                    )
    fig.update_layout(
                    yaxis= dict(
                        title='Sales',
                    ),
                    legend_title='Platform Brand'
                    )
    fig.update_traces(marker=dict(line=dict(width=0.5,
                                        color='DarkSlateGrey')))
    fig.update_traces(marker=dict(opacity=0.5))
    # fig.update_yaxes(
    #     scaleanchor="x",
    #     scaleratio=1,
    # )
    return fig

# Scatter Plot
# @app.callback(Output('scatterplot2', 'figure'),
#               [Input('year_slider', 'value'),
#                Input('user_review_slider', 'value'),
#                Input('critics_review_slider', 'value'),
#                Input('genres_dropdown', 'value'),
#                Input('publishers_dropdown', 'value'),
#                Input('sales_slider', 'value'),
#                Input('region_radio', 'value')])

def update_scatter2(year_slider, user_review_slider, critics_review_slider, genres_dropdown, publishers_dropdown, sales_slider, region_radio):
    scatterData = filter_dataframe(df, genres_dropdown, publishers_dropdown, user_review_slider, critics_review_slider, year_slider, sales_slider)
    fig = px.scatter(scatterData, 
                        x="User_Score",
                        y=region_radio,
                        hover_data=['Name', 'Genre'],
                        color='Plat_Brand',
                        title=f'{region_radio} vs User_Score',
                        color_discrete_map=COLOR_MAP,
                        # width=550,
                        # height=550
                    )
    fig.update_layout(
                    yaxis= dict(
                        title='Sales',
                    ),
                    legend_title='Platform Brand'
                    )
    fig.update_traces(marker=dict(line=dict(width=0.5,
                                            color='DarkSlateGrey')))
    fig.update_traces(marker=dict(opacity=0.5))
    # fig.update_yaxes(
    #     scaleanchor="x",
    #     scaleratio=1,
    # )
    return fig

#Critic Score bar

@app.callback(Output('critics_review_bar', 'figure'),
              [Input('year_slider', 'value'),
               Input('user_review_slider', 'value'),
               Input('critics_review_slider', 'value'),
               Input('genres_dropdown', 'value'),
               Input('publishers_dropdown', 'value'),
               Input('sales_slider', 'value'),
               Input('region_radio', 'value')])
def critic_score_bar(year_slider, user_review_slider, critics_review_slider, genres_dropdown, publishers_dropdown, sales_slider, region_radio):
    bar_data = filter_dataframe(df, genres_dropdown, publishers_dropdown,
                                user_review_slider, critics_review_slider, year_slider, sales_slider)
    bar_data = bar_data.groupby(by=['Plat_Brand'])['Critic_Score'].mean().round(1)
    fig = px.bar(bar_data, x=bar_data.index,
                 y='Critic_Score', text='Critic_Score',
                 color=bar_data.index,
                 color_discrete_map=COLOR_MAP,
                 title='By Platform:')
    fig.update_traces(textposition='outside')
    fig.update_layout(showlegend=False)
    fig.update_yaxes(visible=False, showticklabels=False)
    fig.update_xaxes(title='')
    # Change the margin of the graph and the background color
    fig.update_layout(
    margin=dict(l=50, r=50, t=50, b=50),
    plot_bgcolor='rgba(0,0,0,0)')

    return fig
# User Score bar


@app.callback(Output('user_review_bar', 'figure'),
              [Input('year_slider', 'value'),
               Input('user_review_slider', 'value'),
               Input('critics_review_slider', 'value'),
               Input('genres_dropdown', 'value'),
               Input('publishers_dropdown', 'value'),
               Input('sales_slider', 'value'),
               Input('region_radio', 'value')])
def user_score_bar(year_slider, user_review_slider, critics_review_slider, genres_dropdown, publishers_dropdown, sales_slider, region_radio):
    bar_data = filter_dataframe(df, genres_dropdown, publishers_dropdown,
                                user_review_slider, critics_review_slider, year_slider, sales_slider)
    bar_data = bar_data.groupby(by=['Plat_Brand'])['User_Score'].mean().round(2)
    fig = px.bar(bar_data, x=bar_data.index, y='User_Score', text='User_Score', color=bar_data.index,
                 color_discrete_map=COLOR_MAP, title='By Platform:')
    fig.update_traces(textposition='outside')
    fig.update_layout(showlegend=False)
    fig.update_yaxes(visible=False, showticklabels=False)
    fig.update_xaxes(title='')
    # Change the margin of the graph and the background color
    fig.update_layout(
    margin=dict(l=50, r=50, t=50, b=50),
    plot_bgcolor='rgba(0,0,0,0)')

    return fig

# Generate table


# @app.callback(Output('data_table', 'children'),
#               [Input('year_slider', 'value')])

@app.callback(Output('data_table', 'children'),
              [Input('year_slider', 'value'),
               Input('user_review_slider', 'value'),
               Input('critics_review_slider', 'value'),
               Input('genres_dropdown', 'value'),
               Input('publishers_dropdown', 'value'),
               Input('sales_slider', 'value'),
               Input('region_radio', 'value')])

def generate_table(year_slider, user_review_slider, critics_review_slider, genres_dropdown, publishers_dropdown, sales_slider, region_radio):
    filtered_df = filter_dataframe(df, genres_dropdown, publishers_dropdown,
                                user_review_slider, critics_review_slider, year_slider, sales_slider)
    dataframe = pd.crosstab(filtered_df['Plat_Brand'], filtered_df['Genre'])

    if len(dataframe.columns) > 1:
        total = pd.Series([0 for i in range(len(dataframe.iloc[:,0]))], index=dataframe.index)
        for col in dataframe.columns:
            total += dataframe[col]
        dataframe['Total'] = total

    dataframe.insert(0, column='Console', value=dataframe.index)

    table = dash_table.DataTable(columns=[{'name': i, 'id': i } for i in dataframe.columns],
    data=dataframe.to_dict('records'),
    style_table={'overflowX': 'auto'},
    style_cell={
        'height': '80px',
        # all three widths are needed
        'minWidth': '80px', 'width': '80px', 'maxWidth': '80px',
        'whiteSpace': 'normal',
        'fontSize':15,
        'textAlign': 'center',
        'font_family': 'sans-serif'
    }, 
    style_header={
        'color': 'black',
        'fontWeight': 'bold'
    },
    style_data_conditional=[
        {
            'if': {
                'column_id': 'Console','row_index': 0,
            },
            'color': '#107C10',
            'fontWeight': 'bold'
        },
        {
            'if': {
                'column_id': 'Console','row_index': 2,
            },
            'color': '#003791',
            'fontWeight': 'bold'
        },

        {
            'if': {
                'column_id': 'Console','row_index': 1,
            },
            'color': '#fe0016',
            'fontWeight': 'bold'
        },
        {
            'if': {
                'column_id': 'Total',
            },
            'fontWeight': 'bold'
        }])

    return table

# Data Table Title
@app.callback(Output('data_table_title', 'children'),
              [Input('year_slider', 'value')])

def update_table_title(year_slider):
    return f'Number of Games by Genre from {int(year_slider[0])} to {int(year_slider[1])}'

# helper functions
def filter_dataframe(df, genres_dropdown, publishers_dropdown, user_review_slider, critics_review_slider, year_slider, sales_slider):
    # If none is given for a filter value, we assume everything is selected.
    if not genres_dropdown:
        genres_dropdown = genres
    if not publishers_dropdown:
        publishers_dropdown = publishers
    if not user_review_slider:
        user_review_slider = DEFAULT_USER_REVIEW
    if not critics_review_slider:
        critics_review_slider = DEFAULT_CRITICS_REVIEW
    if not year_slider:
        year_slider = DEFAULT_YEARS
    if not sales_slider:
        sales_slider = DEFAULT_SALES

    return df[df['Genre'].isin(genres_dropdown) & df['Publisher'].isin(publishers_dropdown) & (df['Year_of_Release'] >= int(year_slider[0])) & (df['Year_of_Release'] <= int(year_slider[1])) & (df['User_Score'] >= user_review_slider[0]) & (df['User_Score'] <= user_review_slider[1]) & (df['Critic_Score'] >= critics_review_slider[0]) & (df['Critic_Score'] <= critics_review_slider[1]) & (df['Global_Sales'] >= sales_slider[0]) & (df['Global_Sales'] <= sales_slider[1])]


if __name__ == '__main__':
    app.server.run(debug=True, threaded=True)
