import streamlit as st
import pandas as pd
import altair as alt
from datetime import date

color_dict = {'Los Angeles Dodgers':'#002f6c','San Francisco Giants':'#fa4616','San Diego Padres':'#4d3d36','Arizona Diamondbacks':'#a71930','Colorado Rockies':'#33006F'
              ,'Chicago Cubs':'#002f6c','Cincinnati Reds':'#d50032','St. Louis Cardinals':'#ba0c2f','Milwaukee Brewers':'#13294b','Pittsburgh Pirates':'#ffc72c'
              ,'New York Mets':'#fc4c02','Philadelphia Phillies':'#ba0c2f','Miami Marlins':'#00a3e0','Atlanta Braves':'#002855','Washington Nationals':'#ba122b'
              ,'Seattle Mariners':'#00685e','Oakland Athletics':'#003831','Houston Astros':'#002d62','Los Angeles Angels':'#ba0021','Texas Rangers':'#003278'
              ,'Chicago White Sox':'#27251f','Cleveland Guardians':'#0f223e','Detroit Tigers':'#0c2340','Minnesota Twins':'#0c2341','Kansas City Royals':'#004687'
              ,'Boston Red Sox':'#c8102e','Tampa Bay Rays':'#8fbce6','New York Yankees':'#162546','Toronto Blue Jays':'#134a8e','Baltimore Orioles':'#fc4c02'
            }

baseball_data = pd.read_csv('baseball_team_killers_clean2.csv')

baseball_data = baseball_data.replace(['Anaheim Angels','Los Angeles Angels of Anaheim'],'Los Angeles Angels')
baseball_data = baseball_data.replace(['Florida Marlins'],'Miami Marlins')
baseball_data = baseball_data.replace(['Tampa Bay Devil Rays'],'Tampa Bay Rays')
baseball_data = baseball_data.replace(['Cleveland Indians'],'Cleveland Guardians')
baseball_data = baseball_data.replace(['Montreal Expos'],'Washington Nationals')

values = st.slider(
     'Active Player Years',
     1997, 2022, (1997, 2022),
     help='Players active for any year selected will display their career totals')

option = st.selectbox(
    'Team',
    baseball_data.sort_values(by = ['Split'])['Split'].unique()
)

chart_data = baseball_data[(baseball_data['Split'] == option) & (baseball_data['mlb_played_last'] >= values[0]) & (baseball_data['mlb_played_first'] <= values[1])]

c = alt.Chart(chart_data,title="Top Player tOPS+ & HR Splits (min 100 AB) vs. the "+option).mark_circle(color=color_dict[option]).encode(
    alt.X('tOPS+',scale=alt.Scale(zero=False))
    , y='HR'
    , size='AB'#, color=alt.color()
    , tooltip=['Player Name','HR','BA','OBP','SLG','OPS','tOPS+','AB'])

st.altair_chart(c,use_container_width=True)

col1, col2 = st.columns(2)

hr_data = chart_data.sort_values(by='HR',ascending=False).reset_index()
tops_data = chart_data.sort_values(by='tOPS+',ascending=False).reset_index()

with col1:
    st.subheader("HR Leaders Against the "+option)
    st.table(hr_data[['Player Name','HR','AB']])

with col2:
    st.subheader("tOPS+ Leaders Against the "+option)
    st.table(tops_data[['Player Name','tOPS+','AB']])

st.caption('All data from pybaseball and Baseball Reference.')
st.caption('https://github.com/jldbc/pybaseball')
st.caption('https://www.baseball-reference.com/')
