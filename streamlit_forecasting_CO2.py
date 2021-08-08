# -*- coding: utf-8 -*-
"""
Created on Thu Jul 22 16:34:29 2021

@author: Nishi
"""

# -*- coding: utf-8 -*-


import streamlit as st
import pandas as pd
import pickle
import plotly.express as px


st.markdown("<h1 style='text-align: center; color: White;background-color:#e84343'>Co2 Emission Forecasting</h1>", unsafe_allow_html=True)

pickle_in = open('forecasting_arima.pkl', 'rb') 
forecast = pickle.load(pickle_in)


def user_input_features():
    global Startyear
    global Endyear
    Startyear =st.slider("Input Your Minimum Range",2010,2015)
    Endyear =st.slider("Input your Maximum Range",2015,2030)
    
    df = {'Startyear': Startyear,
            'Endyear':Endyear}
    df = pd.DataFrame(df,index = [0])
    st.write(df)
    Startyear =str(Startyear)
    Endyear = str(Endyear)
    start_year = Startyear[:1]+  Startyear[2:]
    end_year = Endyear[:1]+  Endyear[2:]
    Startyear = int(start_year)
    Endyear = int(end_year)
    data = {'Startyear': Startyear,
            'Endyear':Endyear}
    
    features = pd.DataFrame(data,index = [0])
    return features 



df = user_input_features()
st.sidebar.header("What is this Project about?")
st.sidebar.text("It a Web app that would help the user in forecasting CO2 Emisssion.")


dateparse = lambda x: pd.to_datetime(x, format='%Y', errors = 'coerce')
CO2_1 = pd.read_excel("CO2 dataset.xlsx", parse_dates=['Year'], index_col='Year', date_parser=dateparse) 


future_pred=forecast.predict(start=Startyear,end = Endyear,typ = 'levels')
future_pred_df = future_pred.to_frame().reset_index()
future_pred_df.rename(columns = {'index':'Year',0:'CO2'},
          inplace = True)

future_df=pd.concat([CO2_1,future_pred_df])
CO2_1.reset_index(inplace=True)
current_future_df=pd.concat([CO2_1,future_pred_df])

if st.button("Predict"): 
    future_pred_df 
    #st.line_chart(future_pred_df['CO2'])
    fig = px.line(future_pred_df,
                y=future_pred_df['CO2'],
                x=future_pred_df['Year'])

    st.plotly_chart(fig)



