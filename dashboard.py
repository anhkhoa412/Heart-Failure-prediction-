#!/usr/bin/env python
# coding: utf-8

# In[1]:


import plotly.express as px
import pandas as pd

from jupyter_dash import JupyterDash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input,Output

import plotly.graph_objects as go


# In[2]:


df = pd.read_csv('heart.csv')

df.head()


# In[3]:


# Use the df.shape attribute to check the dimensions of the pandas DataFrame `df`.
df.shape


# In[4]:


# This provides useful information about the DataFrame, including the number of non-null values in each column,
# the data type of each column, and the memory usage of the DataFrame.
df.info()


# In[5]:


categorical_cols= df.select_dtypes(include=['object'])
categorical_cols.columns


# In[6]:


for col in categorical_cols.columns:
    print(col,'-', len(categorical_cols[col].unique()),'Labels')


# In[7]:


df2 = df.copy()
def x(c):
    if c == 0:
        return 'no'
    else:
        return 'yes'
df2['HeartDisease'] = df2['HeartDisease'].apply(x)
df2[df2['Sex']=='M' ]


# In[8]:


df_temp = df2.copy()
background_color = '#f1f1f1'
number_of_men = df_temp[df_temp['Sex'] == 'M'].count()[0]
number_of_women = df_temp[df_temp['Sex'] == 'F'].count()[0]
number_of_patients = df_temp[df_temp['HeartDisease'] == 'yes'].count()[0]
number_of_non_patients = df_temp[df_temp['HeartDisease'] == 'no'].count()[0]
number_of_ExerciseAngina = df_temp[df_temp['ExerciseAngina'] == 'yes'].count(0)
number_of_nonExerciseAngina = df_temp[df_temp['ExerciseAngina'] == 'no'].count(0)


# In[9]:


#Age rank
age_range = df2['Age'].unique()
slider = html.Div(children=[
    html.Center(html.B('age of individuals')),
    html.Div(dcc.RangeSlider(
        id='age_range',
        min=age_range.min(),
        max=age_range.max(),
        step=1,  # to make the slider not to stop in the middle
        allowCross=False,
        marks={int(age): str(age) for age in age_range if age % 10 == 0},
        value=[30, 35],
        vertical=False,
        verticalHeight=600
    )  # end slider
    )  # end div
])

#Gender selection 
drop_down_sex = html.Div([
    html.Center(html.B('sex of individuals')),
    html.Div(dcc.Dropdown(
        id='drop_down_sex',
        options={
            'Male': 'male',
            'Female': 'female',  # use the value to display and the key to be used in the callback
        },
        value=['Male', 'Female'],
        multi=True,
        style={'background-color': background_color, 'border-color': 'blue',
               'height': '60%', 'width': '75%', 'margin-left': '15%'}
    )  # end drop down
    )

])  # end div

#Number of men card
card_man = dbc.Card(
    id='card_men',
    children=[
        dbc.CardBody([
            html.Div([
                # ,  className="card-text" ),#style = {'color':'gray' }) ,
                html.P(['Number of MEN'],style={'text-align': 'center'}),
                html.Center([
                    # this negative is working (20 is large)
                    html.H3(number_of_men, id='number_of_men',
                            style={'margin-top': '-10px'})
                ]),
            ], className='card-text'),
        ]),],
    style={"height": 100, 'width': '17rem', "background-color": "white",
           'border-color': 'yellow', 'border-width': '0px 0px 3px 0px', },
)  # card


# Number of women card
card_woman = dbc.Card(
    id='card_women',
    children=[
        dbc.CardBody([
            html.Div([
                # ,  className="card-text" ),#style = {'color':'gray' }) ,
                html.P(['Number of WOMEN']),
                html.Center([
                    # this negative is working (20 is large)
                    html.H3(number_of_women, id='number_of_women',
                            style={'margin-top': '-10px'})
                ]),

            ], className='card-text'),
        ]),],
    style={"height": 100, 'width': '17rem', "background-color": "white",
           'border-width': '0px 0px 3px 0px', 'border-color': 'green', },
)  # card

#Number of patients card
card_patient = dbc.Card(
    id='card_patient',
    children=[
        dbc.CardBody([
            html.Div([
                # ,  className="card-text" ),#style = {'color':'gray' }) ,
                html.P(['Number of PATIENTS'], style={'text-align': 'center'}),
                html.Center([
                    html.H3(number_of_patients, id='number_of_patients', style={
                            'margin-top': '-10px'})  # this negative is working (20 is large)
                ]),

            ], className='card-text'),
        ]), ],
    style={"height": 100, 'width': '17rem', "background-color": "white", 'border-color': 'red',
           'border-width': '0px 0px 3px 0px', }  # 'box-shadow':'5px 5px 5px darkblue'}
    ,
)  # card

#Number of non_patients card 
card_non_patient = dbc.Card(
    id='card_non_patient',
    children=[
        dbc.CardBody([
            html.Div([
                # ,  className="card-text" ),#style = {'color':'gray' }) ,
                html.P(['Number of NON PATIENTS']),
                html.Center([
                    html.H3(number_of_non_patients, id='number_of_non_patients', style={
                            'margin-top': '-10px'})  # this negative is working (20 is large)
                ]),

            ], className='card-text'),
        ]),],
    style={"height": 100, 'width': '17rem', "background-color": "white", 'border-color': 'blue',
           'border-width': '0px 0px 3px 0px', }  # 'box-shadow':'5px 5px 5px darkblue'}
    ,
)  # card


# In[10]:


import dash_daq as daq
app =JupyterDash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])


# In[11]:


app.layout = html.Div(children=[                               
      dbc.Alert(
        "<<<< Heart Failure Prediction Data>>>>", className="m-5", style={'text-align':'center','font-size':25,'background-color':'bluish', 'top': '0'}),    
            html.Div([
                html.Div([ 
                    dbc.Container( [
                        dbc.Row(
                        [
                            dbc.Col(
                            drop_down_sex
                                , style={'width' : '33.33%'}
                            ),
                
                            dbc.Col(
                                slider ,
                            #width = 4
                            ) 
            
                            ],style={'margin-bottom':'-1px'} ),
        ###################
        ## second row ##
        ###################
                        html.Br(),
                        dbc.Row([
                            dbc.Col(
                                html.Div(
                                    card_man,
                                ) , #div 
            
                                width= 'auto' ,
                                #class_name='col-4',
                            ) ,#col
                
                        dbc.Col(
                            html.Div(
                            card_woman,
                            ),
                            #dcc.Graph(figure = graph_men , style = {'background-color':'lightgray'}) ,
                            width = 'auto',
                        ),
                        
                        dbc.Col(
                            html.Div(
                            card_patient,
                            ) ,#div 
                            #class_name='col-sm-6'
                            width='auto' ,
                        ) , #col
                        
                        dbc.Col(
                            html.Div(
                            card_non_patient,
                            ), #div ,
                            width = 'auto',
                            #class_name='col-4',
                        ),#col
                        
                        ] ,
                        style ={ 'margin-top':'-20px' , 'margin-left':'45px'} # I think default background color is transparent 
                        #'background-color' :'gray'
                        
                    ), #end row
                    ]) ]) ]),
    #third row
            html.Div([
                dbc.Container([
                        html.Br(),
                        dbc.Row([
                            dbc.Col([
                                dcc.Graph(id= 'figure_1_col_1'  , style = {'background-color':'lightgray','box-shadow':'0px 0px 10px 0px darkgray'}) 

                            ], style = {'width': '33.33%', 'display': 'inline-block', 'vertical-align': 'middle'}),

                            dbc.Col([
                                dcc.Graph(id= 'figure_1_col_2'  , style = {'background-color':'lightgray','box-shadow':'0px 0px 10px 0px darkgray'}) 
                                
                            ]
                            , style = {'width': '33.33%', 'display': 'inline-block', 'vertical-align': 'middle'}),

                             dbc.Col([
                                dcc.Graph(id= 'figure_2'  , style = {'background-color':'lightgray','box-shadow':'0px 0px 10px 0px darkgray'}) 
                                
                            ], style = {'width': '33.33%', 'display': 'inline-block', 'vertical-align': 'middle'})
                    ]), 
    #Fourth row
                        html.Br(),
                        dbc.Row([
                            dbc.Col([
                                dcc.Graph(id= 'figure_3_col_1'  , style = {'background-color':'lightgray','box-shadow':'0px 0px 30px 0px darkgray'}) 
                                    
                                ]
                                , style = {'width': '33.33%', 'display': 'inline-block', 'vertical-align': 'middle'}),
                                
                                dbc.Col([
                                    dcc.Graph(id= 'figure_3_col_2'  , style = {'background-color':'lightgray','box-shadow':'0px 0px 10px 0px darkgray'}) 
                                    
                                ]
                                , style = {'width': '33.33%', 'display': 'inline-block', 'vertical-align': 'middle'}),

                                dbc.Col([
                                    dcc.Graph(id= 'figure_3_col_3'  , style = {'background-color':'lightgray','box-shadow':'0px 0px 10px 0px darkgray'}) 
                                    
                                ]
                                , style = {'width': '33.33%', 'display': 'inline-block', 'vertical-align': 'middle'})
                        ])
            
                      
                    ], style={'margin-top': '0 auto', 'max-width': '100%'}) ])  ])

#call back for the cards ##
mapping_dict = {'Male' : 'M' , 'Female' : 'F'}
@app.callback(
    Output(component_id= 'number_of_men', component_property='children'),
    Output(component_id= 'number_of_women', component_property='children'),
    Output(component_id= 'number_of_patients', component_property='children'),
    Output(component_id= 'number_of_non_patients', component_property='children'),
    Output(component_id= 'figure_1_col_1', component_property='figure'),
    Output(component_id= 'figure_1_col_2', component_property='figure'),
    Output(component_id= 'figure_2', component_property='figure'),
    Output(component_id= 'figure_3_col_1', component_property='figure'),
    Output(component_id= 'figure_3_col_2', component_property='figure'),
    Output(component_id= 'figure_3_col_3', component_property='figure'),
   
    Input(component_id= 'age_range', component_property='value'),
    Input(component_id= 'drop_down_sex', component_property='value'),
) 
def update_Info(age_range , drop_down_values):
    df_temp = df2[ (df2['Age'] <= max(age_range) )& (df2['Age']>= min(age_range) )]
    if len(drop_down_values) == 1 :
        df_temp = df_temp[df_temp['Sex'] == mapping_dict[drop_down_values[0] ] ]
    number_of_men = df_temp[df_temp['Sex'] == 'M'].count()[0]
    number_of_women = df_temp[df_temp['Sex'] == 'F'].count()[0]
    number_of_patients = df_temp[df_temp['HeartDisease'] == 'yes'].count()[0]
    number_of_non_patients = df_temp[df_temp['HeartDisease'] == 'no'].count()[0]

    #Creat a pie chart distribution of heart desesa 
    labels = ['Men with heart disease', 'Men without heart disease', 'Women with heart disease', 'Women without heart disease']
    values = [df_temp[(df_temp['Sex'] == 'M') & (df_temp['HeartDisease'] == 'yes')].count()[0], 
              df_temp[(df_temp['Sex'] == 'M') & (df_temp['HeartDisease'] == 'no')].count()[0], 
              df_temp[(df_temp['Sex'] == 'F') & (df_temp['HeartDisease'] == 'yes')].count()[0], 
              df_temp[(df_temp['Sex'] == 'F') & (df_temp['HeartDisease'] == 'no')].count()[0]]
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
    fig.update_layout(title='Distribution of heart disease by sex and age',  title_x=0.5, height=300, margin=dict(l=0, r=0, t=50, b=0))
   
    #Creat a chest pain boxplot 
    labels = [x for x in df.ChestPainType.value_counts().index]
    values = df.ChestPainType.value_counts()
    figure_chest_pain_age = px.box(df_temp , x = 'ChestPainType',y='Age',title= 'which chest pain is critical ?' , color = 'HeartDisease', category_orders= {'HeartDisease' : ['no' ,'yes']})
    figure_chest_pain_age.update_layout(title= 'which chest pain is critical ?', title_x=0.5, height=300, margin=dict(l=0, r=0, t=50, b=0))

    #Creat a pie chart of Exercise Angina 
    labels_ExerciseAngina = ['Exercise + HeartD ', 'Exercise Angina + No HeartD', 'NoExercise + HeartD', 'NoExercise + NoHeartD']
    values_ExerciseAngina = [df_temp[(df_temp['ExerciseAngina'] == 'Y') & (df_temp['HeartDisease'] == 'yes')].count()[0], 
                            df_temp[(df_temp['ExerciseAngina'] == 'Y') & (df_temp['HeartDisease'] == 'no')].count()[0], 
                            df_temp[(df_temp['ExerciseAngina'] == 'N') & (df_temp['HeartDisease'] == 'yes')].count()[0], 
                            df_temp[(df_temp['ExerciseAngina'] == 'N') & (df_temp['HeartDisease'] == 'no')].count()[0]]
    fig_ex = go.Figure(data=[go.Pie(labels=labels_ExerciseAngina, values=values_ExerciseAngina, hole=.3)])
    fig_ex.update_layout(title='Distribution of heart disease by ExerciseAngina',  title_x=0.5, height=300, margin=dict(l=0, r=0, t=50, b=0))

    #Creat a scatter plot chart for max Choleterol
    figure_Cholesterol = px.scatter(df_temp, x = 'Age', y = 'Cholesterol',  color = 'HeartDisease',hover_data=['Sex'], category_orders= {'HeartDisease' : ['no' ,'yes']})
    figure_Cholesterol.update_layout(title = 'Cholesterol', title_x=0.5, height=300, margin=dict(l=0, r=0, t=50, b=0))

    #Creat a scatter plot chart for max RestingBP
    figure_RestingBP = px.scatter(df_temp, x = 'Age', y = 'RestingBP',  color = 'HeartDisease',hover_data=['Sex'], category_orders= {'HeartDisease' : ['no' ,'yes']})
    figure_RestingBP.update_layout(title = 'Resting Blood Preasure', title_x=0.5, height=300, margin=dict(l=0, r=0, t=50, b=0))

    #Creat a scatter plot chart for max Heart Rate 
    figure_MaxHR = px.scatter(df_temp, x = 'Age', y = 'MaxHR',  color = 'HeartDisease',hover_data=['Sex'], category_orders= {'HeartDisease' : ['no' ,'yes']})
    figure_MaxHR.update_layout(title = 'Max heart rate', title_x=0.5, height=300, margin=dict(l=0, r=0, t=50, b=0))
  
    return number_of_men , number_of_women , number_of_patients ,number_of_non_patients, fig, figure_chest_pain_age,fig_ex, figure_Cholesterol,  figure_RestingBP, figure_MaxHR 

print("Im running")

app.run_server(debug=True, port=8062)


# In[ ]:




