import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import datetime
from datetime import date
import plotly.express as px
import calendar


loc_dt = datetime.datetime.today() 
time_del = datetime.timedelta(hours=0) 
new_dt = loc_dt + time_del 
datetime_format = new_dt.strftime("%Y/%m/%d %H:%M:%S")
today = datetime.date.today()
day= datetime.date.today().strftime('%Y%m%d')

this_month=datetime.date.today().strftime('%Y%m')
now = datetime.datetime.now()
yesterdate = today - datetime.timedelta(days=1)
yesterday =yesterdate.strftime("%Y-%m-%d")
month=yesterdate.strftime('%Y%m')
this_month_start = datetime.datetime(yesterdate.year, yesterdate.month, 1).strftime("%Y-%m-%d")
this_month_end = datetime.datetime(yesterdate.year, yesterdate.month, calendar.monthrange(yesterdate.year, yesterdate.month)[1]).strftime("%Y-%m-%d")

this_month_start_day = datetime.datetime(yesterdate.year, yesterdate.month, 1)
#前一個月的最後一天
pre_month =this_month_start_day- datetime.timedelta(days = 1)
pre_month_day =pre_month.strftime('%Y-%m-%d')
pre_months =pre_month.strftime('%Y%m')
#前一個月的第一天
first_day_of_pre_month = datetime.date(pre_month.year, pre_month.month, 1)
first_day_of_pre_month_day =first_day_of_pre_month.strftime('%Y-%m-%d')

df='https://raw.githubusercontent.com/claireyang5588/app-dashborad/main/appdata/df.csv'
df2='https://raw.githubusercontent.com/claireyang5588/app-dashborad/main/appdata/df2.csv'
df3='https://raw.githubusercontent.com/claireyang5588/app-dashborad/main/appdata/df3.csv'
df4='https://raw.githubusercontent.com/claireyang5588/app-dashborad/main/appdata/df4.csv'
df5='https://raw.githubusercontent.com/claireyang5588/app-dashborad/main/appdata/df5.csv'
df6='https://raw.githubusercontent.com/claireyang5588/app-dashborad/main/appdata/df6.csv'
df7='https://raw.githubusercontent.com/claireyang5588/app-dashborad/main/appdata/df7.csv'

df=pd.read_csv(df)
df2=pd.read_csv(df2)
df3=pd.read_csv(df3)
df4=pd.read_csv(df4)
df5=pd.read_csv(df5)
df6=pd.read_csv(df6)
df7=pd.read_csv(df7)
df2['date'] = pd.to_datetime(df2['date'],dayfirst=True)
df6['使用年月']=df6['使用年月'].astype(str)
df7['開通年月']=df7['開通年月'].astype(str)



#當月活躍用戶數(計算到前一天)
month_total=df[df['登入年月']==int(month)].iloc[0]['使用門號數']
#前月活躍用戶
pre_month_total=df[df['登入年月']==int(pre_months)].iloc[0]['使用門號數']


#當月首登用戶數(計算到前一天)
appfirstlog=df3[df3['登入年月']==int(month)].iloc[0]['使用門號數']
#前月首登用戶
pre_appfirstlog=df3[df3['登入年月']==int(pre_months)].iloc[0]['使用門號數']

#使用項目Top10
CATEGORY=pd.merge(df4, df5, how="left", on=["CATEGORY"])
CATEGORY_01=CATEGORY[["CATEGORY","使用門號數_x"]].rename(columns={'使用門號數_x':'使用門號數'})
CATEGORY_01['Month'] = month
CATEGORY_02=CATEGORY[["CATEGORY","使用門號數_y"]].rename(columns={'使用門號數_y':'使用門號數'})
CATEGORY_02['Month'] = int(pre_months)
CATEGORY_03=CATEGORY_01.append(CATEGORY_02)
fig2 = px.bar(CATEGORY_03, x="使用門號數", y="CATEGORY",color="Month",orientation='h',barmode='group',template="plotly_dark",color_discrete_sequence=px.colors.qualitative.D3)
fig2 =fig2.update_layout(plot_bgcolor='#1f2c56',paper_bgcolor='#1f2c56')
unique_categorys = list(df6["CATEGORY"].unique())
filter_categorys=unique_categorys[1:3]

#每月各通路開通新首登用戶佔比
fig4=px.line(df7,x='開通年月',y='當月開通首登APP佔比(%)',color='銷售點',template="plotly_dark")
fig4=fig4.update_layout(plot_bgcolor='#1f2c56',paper_bgcolor='#1f2c56'
                        ,legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))



app = dash.Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}])
server=app.server

app.layout = html.Div([
    html.Div([
        html.Div([
            html.Img(src=app.get_asset_url('aptg.jpg'),
                     id='corona-image',
                     style={
                         "height": "60px",
                         "width": "auto",
                         "margin-bottom": "25px",
                     },
                     )
        ],
            className="one-third column",
        ),
    html.Div([
        html.Div([
            html.Div([
                html.H1("APP Analytics DashBorad", style={"margin-bottom": "0px", 'color': 'white'}),
                 ])
        ], className="one-half column", id="title"),
        
        html.Div([
            html.H6('Last Updated: ' + datetime_format,
                    style={'color': 'orange',
                       'fontSize': 10}),

        ], className="one-third column", id='title1'),

    ], id="header", className="row flex-display", style={"margin-bottom": "25px"}),
    
    html.Div([
        html.Div([
            html.H3(children='APP MAU',
                    style={
                        'textAlign': 'center',
                        'color': 'white',
                       'fontSize': 20} ),
            html.H3(children='('+this_month_start+'~'+yesterday+')',
                    style={
                        'textAlign': 'center',
                        'color': 'white',
                       'fontSize': 15} ),

            html.P(f"{month_total:,.0f}",
                   style={
                       'textAlign': 'center',
                       'color': 'orange',
                       'fontSize': 40,
                       'margin-top':'-18px'}
                   
                   )], className="card_container three columns",),
        html.Div([
            html.H3(children='Previous Month APP MAU',
                    style={
                        'textAlign': 'center',
                        'color': 'white',
                       'fontSize': 20} ),
            
             html.H3(children='('+first_day_of_pre_month_day+'~'+pre_month_day+')',
                    style={
                        'textAlign': 'center',
                        'color': 'white',
                       'fontSize': 15} ),

            html.P(f"{pre_month_total:,.0f}",
                   style={
                       'textAlign': 'center',
                       'color': '#e55467',
                       'fontSize': 40,
                       'margin-top':'-18px'}
                   
                   )], className="card_container three columns",),
        html.Div([
            html.H3(children='Previous Month APP Frist Log',
                    style={
                        'textAlign': 'center',
                        'color': 'white',
                       'fontSize': 20} ),
            
             html.H3(children='('+first_day_of_pre_month_day+'~'+pre_month_day+')',
                    style={
                        'textAlign': 'center',
                        'color': 'white',
                       'fontSize': 15} ),

            html.P(f"{pre_appfirstlog:,.0f}",
                   style={
                       'textAlign': 'center',
                       'color': '#dd1e35',
                       'fontSize': 40,
                       'margin-top':'-18px'}
                   
                   )], className="card_container three columns",),
        html.Div([
            html.H3(children='APP Frist Log',
                    style={
                        'textAlign': 'center',
                        'color': 'white',
                       'fontSize': 20}),
            
            html.H3(children='('+this_month_start+'~'+yesterday+')',
                    style={
                        'textAlign': 'center',
                        'color': 'white',
                       'fontSize': 15}),

            html.P(f"{appfirstlog:,.0f}",
                   style={
                       'textAlign': 'center',
                       'color': 'green',
                       'fontSize': 40,
                       'margin-top':'-18px'}
                   
                   )], className="card_container three columns",)

    ], className="row flex-display"),

    html.Div([
        html.Div([html.H3(children='APP Daily User',
                    style={
                        'textAlign': 'center',
                        'color': 'white'}
                    ),

                    html.P('Select Date range:', className='fix_label',  style={'color': 'white'}),

                     dcc.DatePickerRange(id='my-date-picker-range',
                                         min_date_allowed=date(2019, 1, 1),
                                         max_date_allowed=date(2022, 12, 21),
                                         initial_visible_month=date(2022, 1, 1),
                                         start_date=date(2022, 1, 1),
                                         end_date=date(today.year,today.month,today.day)),
                    dcc.Graph(id='graph',figure={})

        ], className="create_container seven columns"),
        html.Div([html.H3(children='Category Top10',
                    style={
                        'textAlign': 'center',
                        'color': 'white'}
                    ),
            dcc.Graph(
            id='bar-chart',
            figure=fig2),
 
        ], className="create_container six columns"),

        ], className="row flex-display"),

    html.Div([
        html.Div([html.H3(children='APP Monthly Category',
                    style={
                        'textAlign': 'center',
                        'color': 'white'}
                    ),

                    html.P('Select Category:', className='fix_label',  style={'color': 'white'}),
                    dcc.Dropdown(id='dropdown',
                                  multi=True,#將預設單選的下拉式選單擴增為多選的下拉式選單
                                  #clearable=True,
                                  value=filter_categorys,
                                  placeholder='Select Category',
                                  options=[{'label': c, 'value': c}
                                           for c in (df6['CATEGORY'].unique())], className='dcc_compon'),
                       dcc.Graph(id='fig1', figure={})], className="create_container seven columns"),
        html.Div([html.H3(children='New User By Pos_Type',
                    style={
                        'textAlign': 'center',
                        'color': 'white'}
                    ),
            dcc.Graph(
            id='bar-line',
            figure=fig4),
 
        ], className="create_container six columns"),

        ], className="row flex-display")
])])
    
@app.callback(
Output("graph", "figure"),
[Input('my-date-picker-range', 'start_date'),
Input('my-date-picker-range', 'end_date')])

def update_output(start_date, end_date):
    datafilter=df2[(df2['date']>=start_date) & (df2['date']<=end_date)]
    fig =px.line(datafilter, x="date", y="使用門號數",template="plotly_dark") 
    fig =fig.update_layout(plot_bgcolor='#1f2c56',paper_bgcolor='#1f2c56')
    return fig
    
@app.callback(Output('fig1', 'figure'),
              Input('dropdown', 'value'))

def update_graph(state):
   
    traces = []
    for i in state:
        df_state = df6[df6['CATEGORY'] == i]
        traces.append(go.Bar(x=df_state['使用年月'], y=df_state['使用門號數'],name=i))
    fig3 = go.Figure(data=traces).update_layout(plot_bgcolor='#1f2c56',paper_bgcolor='#1f2c56',font=dict(color='white')
                                                 ,xaxis=dict(color='white'),yaxis=dict(color='white')
                                                 ,legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))
    return fig3




if __name__ == '__main__':
          app.run_server(debug=True, use_reloader=False)