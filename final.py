
import pandas as pd
import dash   # !pip install dash
import dash_html_components as html
import webbrowser
import dash_core_components as dcc
from dash.dependencies import Input,Output,State
import plotly.graph_objects as go
import plotly.express as px

# Global Variables
from dash.exceptions import PreventUpdate

app = dash.Dash()  # Creating your object
def load_data():
    dataset_name = 'global_terror1.csv'
    global df
    global india_df
    df = pd.read_csv(dataset_name)
    india_df=df[df['country_txt']=='India']
    global country_list
    global year_dict
    global year_list

    year_list=sorted(df['iyear'].unique().tolist())
    year_dict={str(i):str(i) for i in year_list}
    #print(year_list)

    temp={'January':1,
          'February':2,
          'March':3,
          'April':4,
          'May':5,
          'June':6,
          'July':7,
          'August':8,
          'September':9,
          'October':10,
          'November':11,
          'December':12,
    }
    global month_list
    month_list=[{'label':key,'value':values} for key,values in temp.items()]
    #print(month_list)

    global day_list
    day_list=[{'label':str(i),'value':str(i)} for i in range(1,32)]
    #print(day_list)

    global region_list
    temp=sorted(df['region_txt'].unique().tolist())
    region_list=[{'label':str(i),'value':str(i)} for i in temp]
    #print(region_list)

    global country_list
    #temp_list = sorted(df['country_txt'].unique().tolist())
    country_list =df.groupby('region_txt')['country_txt'].unique().apply(list).to_dict()
    # print(country_list)

    global state_list
    state_list = df.groupby('country_txt')['provstate'].unique().apply(list).to_dict()
    # print(state_list)

    global city_list
    city_list = df.groupby('provstate')['city'].unique().apply(list).to_dict()
    #print(city_list)

    global attack_type
    attack_type = [{"label": str(i), "value": str(i)} for i in df['attacktype1_txt'].unique().tolist()]
    # print(attack_type)

    global chart_dropdown_values
    chart_dropdown_values={"Terrorist Organisation":'gname',
                             "Target Nationality":'natlty1_txt',
                             "Target Type":'targtype1_txt',
                             "Type of Attack":'attacktype1_txt',
                             "Weapon Type":'weaptype1_txt',
                             "Region":'region_txt',
                             "Country Attacked":'country_txt'}
    chart_dropdown_values=[{'label':key,'value':value} for key,value in chart_dropdown_values.items()]

    global chart_dropdown_values_india
    chart_dropdown_values_india = {"Terrorist Organisation": 'gname',
                             "Target Nationality": 'natlty1_txt',
                             "Target Type": 'targtype1_txt',
                             "Type of Attack": 'attacktype1_txt',
                             "Weapon Type": 'weaptype1_txt'}

    chart_dropdown_values_india = [{'label': key, 'value': value} for key, value in chart_dropdown_values_india.items()]

    #print(df.sample(5))
def open_browser():
    # Opening the Browser
    webbrowser.open_new('http://127.0.0.1:8050/')


def create_app_ui():
    # Heading and a Button
    main_layout = html.Div(
    [
    html.H1(id='Main_title', children='Terrorism Analysis with Insights'),
    dcc.Tabs(id="Tabs", value="map", children=[
        dcc.Tab(label="Map tool", id="Map tool", value="map", children=[
            dcc.Tabs(id="subtabs1", value="worldmap", children=[
                dcc.Tab(label="World Map tool", id="World", value="worldmap"),
                dcc.Tab(label="India Map tool", id="India", value="indiamap")
            ]),
            dcc.Dropdown(id='month_dropdown',
                         options=month_list,
                         placeholder='Month',
                         multi=True),
            dcc.Dropdown(id='date_dropdown',
                         placeholder='Date',
                         multi=True),
            dcc.Dropdown(id='region_dropdown',
                         options=region_list,
                         placeholder='Region',
                         multi=True),
            dcc.Dropdown(id='country_dropdown',
                         options=[{'label': 'All', 'value': 'All'}],
                         placeholder='Country',
                         multi=True),
            dcc.Dropdown(id='state_dropdown',
                         options=[{'label': 'All', 'value': 'All'}],
                         placeholder='State',
                         multi=True),
            dcc.Dropdown(id='city_dropdown',
                         options=[{'label': 'All', 'value': 'All'}],
                         placeholder='City',
                         multi=True),
            dcc.Dropdown(id='attack_dropdown',
                         options=attack_type,
                         placeholder='Attact Type',
                         multi=True),

            html.H5('Select the Year', id='year_title'),
            dcc.RangeSlider(
                id='year_slider',
                min=min(year_list),
                max=max(year_list),
                value=[min(year_list), max(year_list)],
                marks=year_dict),
        html.Br(),
        ]),

        dcc.Tab(label="Chart Tool", id="chart tool", value="Chart", children=[
            dcc.Tabs(id="subtabs2", value="Worldchart", children=[
                dcc.Tab(label="World Chart tool", id="WorldC", value="Worldchart",children=[
                    html.Br(),
                    dcc.Dropdown(id='chart_dropdown',
                                  options=chart_dropdown_values,
                                  placeholder='Select Option',
                                  value='region_txt'),
                    html.Br(),
                    html.Hr(),
                    dcc.Input(id='search',placeholder='Search Filter'),
                    html.Hr(),
                    html.Br(),
                ]),
                dcc.Tab(label="India Chart tool", id="IndiaC", value="Indiachart",children=[
                    html.Br(),
                    dcc.Dropdown(id='india_dropdown',
                                 options=chart_dropdown_values_india,
                                 placeholder='select Option',
                                 value='targtype1_txt'),
                    html.Br(),
                    html.Hr(),
                    dcc.Input(id='search_india',placeholder='Search Filter'),
                    html.Hr(),
                    html.Br(),

                ])
            ])
        ]),
    ]),
        html.Div(id='graph_object',children='Graph will be shown here')
        ])
    return main_layout

@app.callback(
    dash.dependencies.Output('graph_object','children'),
    [
    dash.dependencies.Input('Tabs','value'),
    dash.dependencies.Input('month_dropdown', 'value'),
    dash.dependencies.Input('date_dropdown', 'value'),
    dash.dependencies.Input('region_dropdown', 'value'),
    dash.dependencies.Input('country_dropdown', 'value'),
    dash.dependencies.Input('state_dropdown', 'value'),
    dash.dependencies.Input('city_dropdown', 'value'),
    dash.dependencies.Input('attack_dropdown', 'value'),
    dash.dependencies.Input('year_slider', 'value'),
    dash.dependencies.Input('chart_dropdown','value'),
    dash.dependencies.Input('india_dropdown','value'),
    dash.dependencies.Input('subtabs2','value'),
    dash.dependencies.Input('search','value'),
    dash.dependencies.Input('search_india','value')
    ]

)

def update_app_ui(tab,month_value, date_value,region_value,country_value,state_value,city_value,
                  attack_value,year_value,chart_d_value,d_value,subtabs2,search,search_value):
    fig=None

    if tab=='map':

        print("Data Type of month value = ", str(type(month_value)))
        print("Data of month value = ", month_value)

        print("Data Type of Day value = ", str(type(date_value)))
        print("Data of Day value = ", date_value)

        print("Data Type of region value = ", str(type(region_value)))
        print("Data of region value = ", region_value)

        print("Data Type of country value = ", str(type(country_value)))
        print("Data of country value = ", country_value)

        print("Data Type of state value = ", str(type(state_value)))
        print("Data of state value = ", state_value)

        print("Data Type of city value = ", str(type(city_value)))
        print("Data of city value = ", city_value)

        print("Data Type of Attack value = ", str(type(attack_value)))
        print("Data of Attack value = ", attack_value)

        print("Data Type of year value = ", str(type(year_value)))
        print("Data of year value = ", year_value)


        #year filter
        year_range=range(year_value[0],year_value[1]+1)
        df1=df[df['iyear'].isin(year_range)]

        #month filter
        if month_value==[] or month_value is None:
          pass
        else:
          if date_value==[] or date_value is None:
            df1=df[df['imonth'].isin(month_value)]
          else:
            df1=df1[(df1['imonth'].isin(month_value))&
                (df1['iday'].isin(date_value))]


        #region, country, state, city filter
        if region_value==[] or region_value is None:
          pass
        else:
          if country_value==[] or country_value is None:
            df1=df1[df1['region_txt'].isin(region_value)]
          else:
            if state_value==[] or state_value is None:
              df1=df1[(df1['region_txt'].isin(region_value))&
                      (df1['country_txt'].isin(country_value))]
            else:
              if city_value==[] or city_value is None:
                df1 = df1[(df1['region_txt'].isin(region_value)) &
                          (df1['country_txt'].isin(country_value))&
                          (df1['provstate'].isin(state_value))]
              else:
                df1 = df1[(df1['region_txt'].isin(region_value)) &
                          (df1['country_txt'].isin(country_value))&
                          (df1['provstate'].isin(state_value))&
                          (df1['city'].isin(city_value))]
        #print(df1.head(5))
            #attack type filter
        if attack_value == [] or attack_value is None:
          pass
        else:
          df1=df1[df1['attacktype1_txt'].isin(attack_value)]

        map_figure = go.Figure()
        if df1.shape[0]:
          pass
        else:
          df1 = pd.DataFrame(columns=['iyear', 'imonth', 'iday', 'country_txt', 'region_txt', 'provstate',
                                           'city', 'latitude', 'longitude', 'attacktype1_txt', 'nkill'])

          df1.loc[0] = [0, 0, 0, None, None, None, None, None, None, None, None]

        map_figure=px.scatter_mapbox(df1,
                            lat="latitude",
                            lon="longitude",
                            color='attacktype1_txt',
                            hover_data=["region_txt", "country_txt", "provstate","city", "attacktype1_txt","nkill","iyear"],
                            zoom=1
                )
        map_figure.update_layout(mapbox_style="open-street-map",
                             autosize=True,
                             margin=dict(l=0, r=0, t=25, b=20),
                             )

        fig=map_figure

    elif tab=='Chart':

        if subtabs2=='Worldchart':
            if chart_d_value is not None:
                if search is not None:
                    chart_df=df.groupby('iyear')[chart_d_value].value_counts().reset_index(name='count')
                    chart_df=chart_df[chart_df[chart_d_value].str.contains(search,case=False)]
                else:
                    chart_df=df.groupby('iyear')[chart_d_value].value_counts().reset_index(name='count')
            else:
                raise PreventUpdate
            chart_figure=px.area(chart_df,x='iyear',y='count',color=chart_d_value)
            fig=chart_figure

        elif subtabs2=='Indiachart':
            if d_value is not None:
                if search_value is not None:
                    chart_df=india_df.groupby('iyear')[d_value].value_counts().reset_index(name='count')
                    chart_df=chart_df[chart_df[d_value].str.contains(search_value,case=False)]
                else:
                    chart_df=df.groupby('iyear')[d_value].value_counts().reset_index(name='count')
            else:
                raise PreventUpdate
            chart_figure=px.area(chart_df,x='iyear',y='count',color=d_value)
            fig=chart_figure
        else:
            return None

    return dcc.Graph(figure=fig)

@app.callback(
  Output("date_dropdown", "options"),
  [
  Input("month_dropdown", "value")
  ]
  )
def update_date(month):
    date_list = [x for x in range(1, 32)]
    option=[]
    if month :
        option=[{'label':str(m),'value':str(m)} for m in date_list]
    return option

@app.callback(
   [ Output('country_dropdown','value'),
    Output('country_dropdown','disabled'),
    Output('region_dropdown','value'),
    Output('region_dropdown','disabled')],
    [
    Input('subtabs1','value')
    ]
)
def update_r(tab_value):
    region=None
    country=None
    disabled_r=False
    disabled_c=False
    if tab_value=='worldmap':
        pass
    if tab_value=='indiamap':
        region=['South Asia']
        disabled_r=True
        country=['India']
        disabled_c=True
    return country,disabled_c,region,disabled_r

@app.callback(
    Output('country_dropdown','options'),
    [
        Input('region_dropdown','value')
    ]
)
def set_country_option(region_value):
    option=[]
    if region_value is None:
        raise PreventUpdate
    else:
        for val in region_value:
            if val in country_list.keys():
                option.extend(country_list[val])

    return [{'label':i,'value':i} for i in option]

@app.callback(
    Output('state_dropdown', 'options'),
    [Input('country_dropdown', 'value')])
def set_state_options(country_value):
  # Making the state Dropdown data
    option = []
    if country_value is None :
        raise PreventUpdate
    else:
        for var in country_value:
            if var in state_list.keys():
                option.extend(state_list[var])
    return [{'label':m , 'value':m} for m in option]

@app.callback(
    Output('city_dropdown', 'options'),
    [
    Input('state_dropdown', 'value')
    ]
    )
def set_city_options(state_value):
  # Making the city Dropdown data
  option=[]
  if state_value is None:
      raise PreventUpdate
  else:
      for var in state_value:
          if var in city_list.keys():
              option.extend(city_list[var])
  return [{'label':i,'value':i} for i in option]


def main():
    print("Welcome to the Project Season 3 ")
    load_data()
    open_browser()
    global app
    app.layout = create_app_ui()  # blank Container Page
    # change the title
    app.title = "Terrorism Analysis with Insights"
    # Change the favicon
    app.run_server()
    print("Thanks for using my Project ")

    app = None
    df = None

if __name__ == '__main__' :
    main()