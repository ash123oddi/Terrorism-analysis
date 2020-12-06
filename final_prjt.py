import pandas as pd
import dash
import dash_html_components as html
import webbrowser
from dash.dependencies import Input, Output
import dash_core_components as dcc
import plotly.graph_objects as go
import plotly.express as px
from dash.exceptions import PreventUpdate
 
app1 = dash.Dash()# It's an reference object pointing at dash module

def load_data():
    # load all the required for UI
    dataset_name = 'global_terror.csv'
    
    month = {
        'January' : 1,
        'February' : 2,
        'March': 3,
        'April': 4,
        'May': 5,
        'June': 6,
        'July': 7,
        'August': 8,
        'September': 9,
        'October': 10,
        'November': 11,
        'December': 12
        }
    
    
    global df
    df = pd.read_csv(dataset_name)
    
    global month_list, date_list
    month_list = [ {'label': k, 'value': v}   for k, v in month.items()]
    
    
    global rgn_list
    temp_list = sorted(df['region_txt'].unique().tolist())
    rgn_list = [{'label': str(i), 'value': str(i)}  for i in temp_list]
    
    global state_list
    state_list = df.groupby("country_txt")["provstate"].unique().apply(list).to_dict()
    
    global ct_list
    ct_list = df.groupby("provstate")["city"].unique().apply(list).to_dict()
    
    global attck_list
    temp_list = sorted(df['attacktype1_txt'].unique().tolist())
    attck_list = [{'label': str(i), 'value': str(i)}  for i in temp_list]
    
    global country_list
    country_list = df.groupby("region_txt")["country_txt"].unique().apply(list).to_dict()
    
    global year_list
    year_list = sorted(df['iyear'].unique().tolist())
    
    global year_dict
    year_dict = {str(i): str(i) for i in year_list}
    
    global list_dropdown, chart_list
    list_dropdown = {
        "Terrorist Organization":'gname',
        "Target Nationality":'natlty1_txt',
        "Target Type":'targtype1_txt',
        "Type of Attack":'attacktype1_txt',
        "Weapon Type":'weaptype1_txt',
        "Region":'region_txt',
        "Country Attacked":'country_txt'
        }
    
    chart_list = [{'label': key, 'value': val}  for key, val in list_dropdown.items()]
    

def open_browser():
    # will open browser automatically
    webbrowser.open_new('http://127.0.0.1:8050/')


def create_app_ui():
    # Making layout of UI
    tabs_styles = {
    'height': '45px'
    }
    tab_style = {
        'borderBottom': '1px solid black',
        'backgroundColor': "lightyellow",
        'padding': '6px',
        'fontSize': '23px',
        'fontWeight': 'bold'
    }
    
    tab_selected_style = {
        'borderTop': '1px solid black',
        'borderBottom': '1px solid #d6d6d6',
        'backgroundColor': "Gold",
        'color': 'black',
        'fontSize': '25px',
        'padding': '6px',
        'fontFamily':'Times New Roman, Times, serif'
    }
    subtab_selected_style = {
        'backgroundColor':'lightblue',
        'color':'white',
        'fontSize': '25px',
        'fontWeight': 'bold',
        'fontFamily':'Open Sans, sans-serif'}
    
    main_layout = html.Div([html.H1(id = 'Main_title', 
                                    children = 'Terrorism Analysis with Insights', 
                                    style = {'color':'#2E5129', 'textAlign':'center','fontSize': '50px','textDecoration': 'underline'}),
                            dcc.Tabs(id = 'Tabs', value = 'map', children = [
                                dcc.Tab(label = 'Map tool', id = 'Map tool', value = 'map', 
                                        style=tab_style, selected_style=tab_selected_style, 
                                        children = [
                                    dcc.Tabs(id= 'subtab1', value = 'tab-1', children = [
                                        dcc.Tab(label = 'World Map tool', id = 'World', value = 'tab-1',style=tab_style,selected_style = subtab_selected_style),
                                        dcc.Tab(label = 'India Map tool', id = 'India', value = 'tab-2',style=tab_style,selected_style = subtab_selected_style)
                                        ]),
                                    dcc.Dropdown(id = 'month', 
                                                 options = month_list, 
                                                 placeholder = 'Select Month',
                                                 multi =True),
                                    dcc.Dropdown(id = 'date',  
                                                 placeholder = 'Select Date',
                                                 multi=True),
                                    dcc.Dropdown(id = 'region-dropdown', 
                                                 options = rgn_list, 
                                                 placeholder = 'Select Region',
                                                 multi = True),
                                    dcc.Dropdown(id = 'country-dropdown', 
                                                 options = [{'label': 'All', 'value': 'All'}], 
                                                 placeholder = 'Select Country',
                                                 multi = True),
                                    dcc.Dropdown(id = 'state-dropdown', 
                                                 options = [{'label': 'All', 'value': 'All'}], 
                                                 placeholder = 'Select State',
                                                 multi = True),
                                    dcc.Dropdown(id = 'city-dropdown', 
                                                 options = [{'label': 'All', 'value': 'All'}], 
                                                 placeholder = 'Select City',
                                                 multi = True),
                                    dcc.Dropdown(id = 'attact-type-dropdown', 
                                                 options = attck_list, 
                                                 placeholder = 'Select Attack type',
                                                 multi = True),
                                    html.H4(id = 'year_title', children = 'Select the Year:',style = {'textDecoration': 'underline'}),
                                                    
                                    dcc.RangeSlider(id = 'year-slider',
                                                                min = min(year_list),
                                                                max = max(year_list),
                                                                marks= year_dict,
                                                                value = [min(year_list), max(year_list)],
                                                                step = None
                                                                ),
                                    html.Br(),
                                    ]),
                                dcc.Tab(label = 'Chart tool', id = 'Chart tool', value = 'chart',
                                        style=tab_style, selected_style=tab_selected_style, 
                                        children = [
                                    dcc.Tabs(id= 'subtab2', value = 'tab-3', children = [
                                        dcc.Tab(label = 'World Chart tool', id = 'Worldc', value = 'tab-3',style=tab_style,selected_style = subtab_selected_style),
                                        dcc.Tab(label = 'India Chart tool', id = 'Indiac', value = 'tab-4',style=tab_style,selected_style = subtab_selected_style)
                                        ]),
                                    html.Br(),
                                    html.Br(),
                                    dcc.Dropdown(id = 'chart-dropdown', 
                                    options = chart_list,
                                    placeholder = 'Select...',
                                    value = 'region_txt'),
                                    html.Br(),
                                    html.Hr(),
                                    dcc.Input(id = 'search', placeholder = 'Search filter'),
                                    html.Hr(),
                                    html.H4(id = 'year_title_c', children = 'Select the Year:',style = {'textDecoration': 'underline'}),
                                    dcc.RangeSlider(id = 'chart-year-slider',
                                                min = min(year_list),
                                                max = max(year_list),
                                                marks= year_dict,
                                                value = [min(year_list), max(year_list)],
                                                step = None
                                                ),
                                    html.Br()
                                    ])
                                ],style=tabs_styles),
                             dcc.Loading(dcc.Graph(id='graph-object', figure = go.Figure()))
                             ],style={'backgroundColor':"#CEF49D"},)
    return main_layout   



@app1.callback(
    Output('graph-object', 'figure'),
    [
     Input('month', 'value'), 
     Input('date', 'value'),
     Input('region-dropdown', 'value'),
     Input('country-dropdown', 'value'),
     Input('state-dropdown', 'value'),
     Input('city-dropdown', 'value'),
     Input('attact-type-dropdown', 'value'),
     Input('year-slider', 'value'),
     Input('Tabs', 'value'),
     Input('chart-year-slider', 'value'),
     Input('chart-dropdown', 'value'),
     Input('search', 'value'),
     Input('subtab2', 'value'),
    ]
    )
def update_app_ui1(mon_val,date_val,rgn_val,cntry_val,stt_val,ct_val,attk_value,year_val,tabs,chart_s,chart_dp,fil_search,subtab2):
    # UI will updated according to tabs Selection
    figure = None
    
    if tabs == 'map':
        
        print('Data type of month  =', str(type(mon_val)))
        print('Value  = ', str(mon_val))
        
        print('Data type of date =', str(type(date_val)))
        print('Value  = ', str(date_val))
    
        print('Data type of region =', str(type(rgn_val)))
        print('Value  = ', str(rgn_val))
        
        print('Data type of country =', str(type(cntry_val)))
        print('Value  = ', str(cntry_val))
        
        print('Data type of state  =', str(type(stt_val)))
        print('Value  = ', str(stt_val))
        
        print('Data type of city  =', str(type(ct_val)))
        print('Value  = ', str(ct_val))
        
        print('Data type of attack type =', str(type(attk_value)))
        print('Value  = ', str(attk_value))
        
        print('Data type of year =', str(type(year_val)))
        print('Value  = ', str(year_val))
        
        print("datatype of tab = ",str(type(tabs)))
        print("datatype of tab = ",str(tabs))
    
        
       # year_filter
        year_range = range(year_val[0], year_val[1]+1)
        new_df = df[df["iyear"].isin(year_range)]
        
        # month_filter
        if mon_val==[] or mon_val is None:
            pass
        else:
            if date_val==[] or date_val is None:
                new_df = new_df[new_df["imonth"].isin(mon_val)]
            else:
                new_df = new_df[new_df["imonth"].isin(mon_val)
                                & (new_df["iday"].isin(date_val))]
        
        # region, country, state or province filter
        if rgn_val == [] or rgn_val is None:
            pass
        else: 
            if cntry_val == [] or cntry_val is None:
                new_df = new_df[new_df['region_txt'].isin(rgn_val)]
            else:
                if stt_val == [] or stt_val is None:
                    new_df = new_df[(new_df['region_txt'].isin(rgn_val)) &
                                    (new_df['country_txt'].isin(cntry_val))]
                else:
                    if ct_val == [] or ct_val is None:
                        new_df = new_df[(new_df['region_txt'].isin(rgn_val)) &
                                        (new_df['country_txt'].isin(cntry_val))&
                                        (new_df['provstate'].isin(stt_val))]
                    else:
                        new_df = new_df[(new_df['region_txt'].isin(rgn_val)) &
                                        (new_df['country_txt'].isin(cntry_val))&
                                        (new_df['provstate'].isin(stt_val))&
                                        (new_df['city'].isin(ct_val))]
                   
    
        #attack type filtering technique
        if attk_value== [] or attk_value is None:
            pass
        else:
            new_df = new_df[new_df['attacktype1_txt'].isin(attk_value)]
         
        map_figure = go.Figure()    
        if new_df.shape[0]:
            pass
        else:
            new_df = pd.DataFrame(columns=['iyear','imonth','iday','country_txt','region_txt','provstate',
            'city','latitude', 'longitude','attacktype1_txt','nkill'])
                
            new_df.loc[0] = [0, 0, 0, None, None, None, None, None, None, None, None]
    
        map_figure = px.scatter_mapbox(new_df,
                                   lat = 'latitude',
                                   lon = 'longitude',
                                   color='attacktype1_txt',
                                   hover_data=["region_txt", "country_txt", "provstate","city", "attacktype1_txt","nkill","iyear","imonth", "iday"],
                                   zoom = 1
                                   )
        map_figure.update_layout(
            mapbox_style = 'open-street-map',
            autosize = True,
            margin = dict(l=0, r=0, t=25, b=20)
            )
        figure = map_figure
        
    elif tabs == 'chart':
        figure = None
        print('Data type of chart_dropdown  =', str(type(chart_dp)))
        print('Value  = ', str(chart_dp))
        
        print('Data type of year slider  =', str(type(chart_s)))
        print('Value  = ', str(chart_s))
        
        print('Data type of search filter  =', str(type(fil_search)))
        print('Value  = ', str(fil_search))
        
        chart_yr_range = range(chart_s[0],chart_s[1]+1)
        chart_new_df = df[df["iyear"].isin(chart_yr_range)]
        
        if subtab2 == 'tab-3':
            pass
        elif subtab2 == 'tab-4':# filter data for India Chart tool i.e set region and country with South Asia and India
            chart_new_df = chart_new_df[(chart_new_df['region_txt']=='South Asia') & (chart_new_df['country_txt']=='India')]
        if chart_dp is not None and chart_new_df.shape[0]:
            if fil_search is not None:
                chart_new_df = chart_new_df.groupby('iyear')[chart_dp].value_counts().reset_index(name = 'count')
                chart_new_df = chart_new_df[chart_new_df[chart_dp].str.contains(fil_search, case = False)]
            else:
                chart_new_df = chart_new_df.groupby('iyear')[chart_dp].value_counts().reset_index(name = 'count')
                    
        if chart_new_df.shape[0]:
            pass
        else: 
            chart_new_df = pd.DataFrame(columns = ['iyear', 'count', chart_dp])
            chart_new_df.loc[0] = [0, 0,"No data"]
            
        
        chartfigure = px.area(chart_new_df,x = 'iyear',y = 'count',color = chart_dp)
        figure = chartfigure
        
    return figure


@app1.callback(
    Output( 'date', 'options'),
    [
     Input('month', 'value'),
     ]
    )
def update_date(month):
    # Making the Date Dropdown data
    date_list = [x for x in range(1, 32)]
    option = []
    if month:
        option= [{"label":m, "value":m} for m in date_list]
    return option
 

@app1.callback(
    [Output('region-dropdown', 'value'),
     Output('region-dropdown', 'disabled'),
     Output('country-dropdown', 'value'),
     Output('country-dropdown', 'disabled')],
    [Input('subtab1', 'value')]
    )
def update_india_part(tab):
    # Making the country Dropdown and region dropdown Disabled for india map tool
    region = None
    disabled_r = False
    country = None
    disabled_c = False
    if tab == 'tab-1':
        pass
    elif tab == 'tab-2':
        region = ["South Asia"]
        disabled_r = True
        country = ["India"]
        disabled_c = True
    return region, disabled_r, country, disabled_c    


   
@app1.callback(
    Output('country-dropdown', 'options'),
    [
     Input('region-dropdown','value')
     ]
    )
def set_country_opt (region_val):
    option = []
    # Making the country Dropdown data
    if region_val is  None:
        raise PreventUpdate
    else:
        for var in region_val:
            if var in country_list.keys():
                option.extend(country_list[var])
    return [{'label':m , 'value':m} for m in option]

 
@app1.callback(
    Output('state-dropdown', 'options'),
    [
     Input('country-dropdown','value')
     ]
    )
def set_state_opt (country_val):
    # Making the state Dropdown data
    option = []
    if country_val is None :
        raise PreventUpdate
    else:
        for var in country_val:
            if var in state_list.keys():
                option.extend(state_list[var])
    return [{'label':m , 'value':m} for m in option] 


@app1.callback(
    Output('city-dropdown', 'options'),
    [
     Input('state-dropdown','value')
     ]
    )
def set_city_opt (stt_val):
    # Making the city Dropdown data
    option = []
    if stt_val is None:
        raise PreventUpdate
    else:
        for var in stt_val:
            if var in ct_list.keys():
                option.extend(ct_list[var])
    return [{'label':m , 'value':m} for m in option]

    
def main():
    load_data()
    open_browser()
    
    global project_name
    project_name = "Terrorism Analysis with Insights"
    
    global app1
    app1.layout = create_app_ui()
    app1.title = project_name
    app1.run_server()# debug=True
    
    print("This would be print after the script is closed")
    
    app1 = None
    project_name = None


if (__name__ == '__main__'):
    main()
