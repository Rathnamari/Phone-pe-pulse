import pandas as pd
import psycopg2
import streamlit as st
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import webbrowser
from streamlit_option_menu import option_menu
import plotly.graph_objects as go

mydb = psycopg2.connect(host = 'localhost',user = 'postgres',password = 'Tkkrathna26@',port = 5432,database = 'phonepe') 
mycursor = mydb.cursor()

st.set_page_config(
    page_title="PhonePe Data Visualization",
    page_icon="chart_with_upwards_trend",
    initial_sidebar_state="expanded",)

with st.sidebar:
  main = option_menu(None, ["Home","About","Visualization","Map_Visualization"],menu_icon='cast')

if main == "Home": 
   st.title(":violet[Phonepe Pulse Data Visualization]")  
   url = "https://download.logo.wine/logo/PhonePe/PhonePe-Logo.wine.png"
   st.image(url)

if main == "About":
    st.title(":violet[ABOUT]")
    st.markdown("### Welcome to the PhonePe Pulse Dashboard ,This PhonePe Pulse Data Visualization and Exploration dashboard is a user-friendly tool designed to provide insights and information about the data in the PhonePe Pulse GitHub repository. This dashboard offers a visually appealing and interactive interface for users to explore various metrics and statistics.")
    st.write("Email Id: tkkrathna26@gmail.com")
    st.write("Linkedin Id: https://www.linkedin.com/in/rathna-mari-041aa4251")
  
if main== "Visualization":
   with st.sidebar:
      main1 = option_menu(None, ["Transactions","Users"],menu_icon='cast')

   if main1 == "Transactions":
        with st.sidebar:
          Topic = ["Aggregated","Map","Top"]
          choice_topic = st.selectbox("Transactions", Topic)

        with st.sidebar:
          Topic = ["2018","2019","2020","2021","2022"]
          year = st.selectbox("Year",Topic)
          Topic = ["1","2","3","4"]
          quarter = st.selectbox("Quarter",Topic)
          Topic = ['ladakh','nagaland''chhattisgarh','jammu-&-kashmir','gujarat','lakshadweep','uttarakhand','punjab','chandigarh','maharashtra',
                          'jharkhand','delhi','kerala','tamil-nadu','meghalaya', 'puducherry', 'himachal-pradesh','mizoram','manipur','rajasthan',
                          'west-bengal','andhra-pradesh','uttar-pradesh','sikkim','madhya-pradesh','odisha','karnataka','tripura','goa','haryana',
                          'andaman-&-nicobar-islands','telangana','arunachal-pradesh','dadra-&-nagar-haveli-&-daman-&-diu','assam','bihar']
          state = st.selectbox("State",Topic)

        if choice_topic == "Aggregated":   
              st.title('Aggregrated_Transaction')          
              mycursor.execute(f"SELECT sum(Transaction_amount) as Transaction_amount,sum(Total_transaction) as Total_transaction,Transaction_type FROM aggregated_transactions  where Year = {year} and Quarter = {quarter} and State = '{state}' group by Transaction_type")
              records1 = mycursor.fetchall()
              aggregated_transactions = pd.DataFrame(records1,
                                              columns=[i[0] for i  in mycursor.description])
              st.dataframe(aggregated_transactions)

              df = px.bar(aggregated_transactions,
                                                  x = 'transaction_type',
                                                  y = 'total_transaction',
                                                  color = 'transaction_type',  
                                                  color_continuous_scale='oranges' )
              df.update_traces(width = 0.8)
              st.plotly_chart(df) 
              
              fig = px.scatter (aggregated_transactions,
                                x = 'transaction_type', 
                                y = 'total_transaction',
                                color = 'transaction_type')
              st.plotly_chart(fig)

        if choice_topic == "Map":  
              st.title("Map_Transactions")                      
              mycursor.execute(f"SELECT District ,User_Count,Total_Amount FROM map_transactions where Year = {year} and Quarter = {quarter} and state = '{state}' order by Total_Amount desc limit 10")
              records2 = mycursor.fetchall()
              map_transactions = pd.DataFrame(records2,
                                              columns=[i[0] for i  in mycursor.description])
              st.dataframe(map_transactions)
              
              df2 = px.bar(map_transactions,
                                                  x = 'district',
                                                  y = 'user_count',
                                                  color = 'district',
                                                  color_continuous_scale='blue' )
              df2.update_traces(width = 0.8)
              st.plotly_chart(df2) 
              
              fig1 = px.scatter (map_transactions,
                                x = 'total_amount', 
                                y = 'user_count',
                                color = 'district')
              st.plotly_chart(fig1)

          
        if choice_topic == "Top": 
              st.title('Top_Transaction')            
              mycursor.execute(f"SELECT District,topuser_Count,Amount FROM top_transactions where Year = {year} and Quarter = {quarter} and State = '{state}' order by Amount desc limit 10")
              records3 = mycursor.fetchall()
              top_transactions = pd.DataFrame(records3,
                                              columns=[i[0] for i  in mycursor.description])
              st.dataframe(top_transactions)
              
              df3 = px.bar(top_transactions,
                                                  x = 'district',
                                                  y = 'topuser_count',
                                                  color = 'district',
                                                  color_continuous_scale='blue' )
              df3.update_traces(width = 0.8)
              st.plotly_chart(df3) 
              
              fig2 = px.scatter (top_transactions,
                                x = 'amount', 
                                y = 'topuser_count',
                                color = 'district')
              st.plotly_chart(fig2)              
   
   if main1 == "Users":
        with st.sidebar:
          Topic = ["Aggregated","Map","Top"]
          select_topic = st.selectbox("Users", Topic)

        with st.sidebar:
          Topic = ["2018","2019","2020","2021","2022"]
          year = st.selectbox("Year",Topic)
          Topic = ["1","2","3","4"]
          quarter = st.selectbox("Quarter",Topic)
          Topic = ['ladakh','nagaland''chhattisgarh','jammu-&-kashmir','gujarat','lakshadweep','uttarakhand','punjab','chandigarh','maharashtra',
                          'jharkhand','delhi','kerala','tamil-nadu','meghalaya', 'puducherry', 'himachal-pradesh','mizoram','manipur','rajasthan',
                          'west-bengal','andhra-pradesh','uttar-pradesh','sikkim','madhya-pradesh','odisha','karnataka','tripura','goa','haryana',
                          'andaman-&-nicobar-islands','telangana','arunachal-pradesh','dadra-&-nagar-haveli-&-daman-&-diu','assam','bihar']
          state = st.selectbox("State",Topic)


        if select_topic == "Aggregated": 
                    st.title('Aggregated_User')            
                    mycursor.execute(f"SELECT User_brand,User_Count,User_Percentage FROM aggregated_user1  where Year = {year} and Quarter = {quarter} and state = '{state}'order by user_count desc limit 10")
                    records4 = mycursor.fetchall()
                    aggregated_user1 = pd.DataFrame(records4,
                                                    columns=[i[0] for i  in mycursor.description])
                    st.dataframe(aggregated_user1)

            
            
                    fig = go.Figure(go.Scatter( x=aggregated_user1['user_count'],
                                                y=aggregated_user1['user_brand'], 
                                                mode='markers+text+lines',
                                                text=aggregated_user1['user_percentage'],
                                                textposition="bottom left"))
                    st.plotly_chart(fig)

                    fig = px.pie(aggregated_user1, names = "user_brand",values = "user_percentage")
                    st.plotly_chart(fig)

        if select_topic == "Map":
                    st.title("Map_Users")             
                    mycursor.execute(f"SELECT District,Registered_user,App_open  FROM map_users  where Year = {year} and Quarter = {quarter} and State = '{state}' order by App_open desc limit 10")
                    records5 = mycursor.fetchall()
                    map_users = pd.DataFrame(records5,
                                                    columns=[i[0] for i  in mycursor.description])
                    st.dataframe(map_users)

              
                    fig = go.Figure(go.Scatter( x=map_users['district'],
                                                y=map_users['registered_user'], 
                                                mode='markers+text+lines',
                                                text=map_users['app_open'],
                                                textposition="bottom left"))
                    st.plotly_chart(fig)

                    fig = px.pie(map_users, names = "district",values = "registered_user")
                    st.plotly_chart(fig)

        if select_topic == "Top": 
                    st.title("Top_Users")            
                    mycursor.execute(f"SELECT District,Registered_user  FROM top_users  where Year = {year} and Quarter = {quarter}  and state = '{state}' order by Registered_user desc limit 10")
                    records6 = mycursor.fetchall()
                    top_users = pd.DataFrame(records6,
                                                    columns=[i[0] for i  in mycursor.description])
                    st.dataframe(top_users)
            
                    fig = go.Figure(go.Scatter( x=top_users['district'],
                                                y=top_users['registered_user'], 
                                                mode='markers+text+lines',
                                                text=top_users['district'],
                                                textposition="bottom left"))
                    st.plotly_chart(fig)

                    fig = px.pie(top_users, names = "district",values = "registered_user")
                    st.plotly_chart(fig)

if main == "Map_Visualization":
      state = pd.read_csv(r"C:\Users\HP\Downloads\Phonepe-Pulse-Data-Visualization-and-Exploration\Longitude_Latitude_State_Table.csv")
      
      with st.sidebar:
        main2 = option_menu(None, ["Transactions","Users"],menu_icon='cast')

      if main2 == "Transactions":
        with st.sidebar:
          Topic = ["Aggregated","Map","Top"]
          select_topic = st.selectbox("Transactions", Topic)

        with st.sidebar:
          Topic = ["2018","2019","2020","2021","2022"]
          year = st.selectbox("Year",Topic)
          Topic = ["1","2","3","4"]
          quarter = st.selectbox("Quarter",Topic)
        
        if select_topic == "Aggregated":
           
           st.title("Aggregated_Transaction")

           mycursor.execute(f"select state,sum(total_transaction) as total_transaction,sum(transaction_amount)as transaction_amount  from aggregated_transactions where year = {year} and quarter = {quarter} group by state")
           records1 = mycursor.fetchall()
           aggregated_transactions = pd.DataFrame(records1,
                                                        columns=[i[0] for i  in mycursor.description])

           aggregated_transactions1 = aggregated_transactions.copy()
           aggregated_transactions1.drop(aggregated_transactions1.index[(aggregated_transactions1['state']=='india')],axis=0,inplace =True)

           state =state.sort_values(by=['state'], ascending=False) 
           Transaction_Amount=[]
           for i in aggregated_transactions1['transaction_amount']:
              Transaction_Amount.append(i)

           state['Transaction_Amount']=Transaction_Amount

           Total_Transaction=[]
           for i in aggregated_transactions1['total_transaction']:
              Total_Transaction.append(i)

           state['Total_Transaction'] = Total_Transaction
      

           fig_ch = px.choropleth(
                              state,
                              geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                              featureidkey='properties.ST_NM',                
                              locations='state',
                              color="Total_Transaction",                                       
                              )
           fig_ch.update_geos(fitbounds="locations", visible=False,)
           st.plotly_chart(fig_ch)
           

        if select_topic == "Map":
            
           st.title("Map_Transaction")

           mycursor.execute(f"select state,sum(total_amount) as total_amount from map_transactions where year = {year} and quarter = {quarter} group by state")
           records2 = mycursor.fetchall()
           map_transactions = pd.DataFrame(records2,
                                                        columns=[i[0] for i  in mycursor.description])

           map_transactions1 = map_transactions.copy()
           map_transactions1.drop(map_transactions1.index[(map_transactions1['state']=='india')],axis=0,inplace =True)

           state =state.sort_values(by=['state'], ascending=False) 
           
           Total_Amount=[]
           for i in map_transactions1['total_amount']:
              Total_Amount.append(i)

           state['Total_Amount']=Total_Amount

           fig1_ch = px.choropleth(
                              state,
                              geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                              featureidkey='properties.ST_NM',                
                              locations='state',
                              color="Total_Amount",                                       
                              )
           fig1_ch.update_geos(fitbounds="locations", visible=False,)
           st.plotly_chart(fig1_ch)

        if select_topic == "Top":
          
           st.title("Top_Transaction")

           mycursor.execute(f"select state,sum(amount) as amount from top_transactions where year = {year} and quarter = {quarter} group by state")

           records3 = mycursor.fetchall()
           top_transactions = pd.DataFrame(records3,
                                                        columns=[i[0] for i  in mycursor.description])

           top_transactions1 = top_transactions.copy()
           top_transactions1.drop(top_transactions1.index[(top_transactions1['state']=='india')],axis=0,inplace =True)

           state =state.sort_values(by=['state'], ascending=False) 
           
           Total_Amount=[]
           for i in top_transactions1['amount']:
              Total_Amount.append(i)

           state['Total_Amount']=Total_Amount

           fig3_ch = px.choropleth(
                              state,
                              geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                              featureidkey='properties.ST_NM',                
                              locations='state',
                              color="Total_Amount",                                       
                              )
           fig3_ch.update_geos(fitbounds="locations", visible=False,)
           st.plotly_chart(fig3_ch)

      if main2 == "Users":
        with st.sidebar:
          Topic = ["Aggregated","Map","Top"]
          choice_topic = st.selectbox("Transactions", Topic)

        with st.sidebar:
          Topic = ["2018","2019","2020","2021","2022"]
          year = st.selectbox("Year",Topic)
          Topic = ["1","2","3","4"]
          quarter = st.selectbox("Quarter",Topic)
        
        if choice_topic == "Aggregated":
           
          st.title("Aggregated_User")
          
          mycursor.execute(f"select state,sum(user_count) as user_count from aggregated_user1 where year = {year} and quarter = {quarter} group by state")

          records4 = mycursor.fetchall()
          aggregated_user1 = pd.DataFrame(records4,
                                                        columns=[i[0] for i  in mycursor.description])

          aggregated_user = aggregated_user1.copy()
          aggregated_user.drop(aggregated_user.index[(aggregated_user['state']=='india')],axis=0,inplace =True)

          state =state.sort_values(by=['state'], ascending=False) 
           
          user_count=[]
          for i in aggregated_user['user_count']:
              user_count.append(i)

          state['user_count']=user_count

          fig4_ch = px.choropleth(
                              state,
                              geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                              featureidkey='properties.ST_NM',                
                              locations='state',
                              color="user_count",                                       
                              )
          fig4_ch.update_geos(fitbounds="locations", visible=False,)
          st.plotly_chart(fig4_ch)

        if choice_topic == "Map":
           
          st.title("Map_User")
          
          mycursor.execute(f"select state,sum(registered_user) as registered_user from map_users where year = {year} and quarter = {quarter} group by state")

          records5 = mycursor.fetchall()
          map_users = pd.DataFrame(records5,
                                               columns=[i[0] for i  in mycursor.description])

          map_users1 = map_users.copy()
          map_users1.drop(map_users1.index[(map_users1['state']=='india')],axis=0,inplace =True)

          state =state.sort_values(by=['state'], ascending=False) 
           
          registered_user=[]
          for i in map_users1['registered_user']:
              registered_user.append(i)

          state['registered_user']=registered_user

          fig5_ch = px.choropleth(
                              state,
                              geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                              featureidkey='properties.ST_NM',                
                              locations='state',
                              color="registered_user",                                       
                              )
          fig5_ch.update_geos(fitbounds="locations", visible=False,)
          st.plotly_chart(fig5_ch)

        
        if choice_topic == "Top":
           
          st.title("Top_User")
          
          mycursor.execute(f"select state,sum(registered_user) as registered_user from top_users where year = {year} and quarter = {quarter} group by state")

          records6 = mycursor.fetchall()
          top_users = pd.DataFrame(records6,
                                               columns=[i[0] for i  in mycursor.description])

          top_users1 = top_users.copy()
          top_users1.drop(top_users1.index[(top_users1['state']=='india')],axis=0,inplace =True)

          state =state.sort_values(by=['state'], ascending=False) 
           
          registered_user=[]
          for i in top_users1['registered_user']:
              registered_user.append(i)

          state['registered_user']=registered_user

          fig6_ch = px.choropleth(
                              state,
                              geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                              featureidkey='properties.ST_NM',                
                              locations='state',
                              color="registered_user",                                       
                              )
          fig6_ch.update_geos(fitbounds="locations", visible=False,)
          st.plotly_chart(fig6_ch)
