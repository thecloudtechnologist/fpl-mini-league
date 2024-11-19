import requests
import pandas as pd
import streamlit as st
from functions import *
##

url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
r = requests.get(url)
json1 = r.json()
players_df = pd.DataFrame(json1['elements'])
events_df = pd.DataFrame(json1['events'])
gwplayed = events_df.loc[events_df['is_current'] == True]['id'].iloc[-1]
keep_cols = ["id","web_name","event_points","element_type"]
players_df = players_df[keep_cols]
players_df['element_type'] = players_df['element_type'].replace([1,2,3,4],['GKP','DEF','MID','FWD'])

league_id = st.session_state.league_id
##
url1 = "https://fantasy.premierleague.com/api/leagues-classic/%s/standings/" % (league_id)
json_minileague = requests.get(url1).json()
results = json_minileague['standings']['results']
df_results = pd.DataFrame(results)

##
# get picks list
def get_picks(id,gwplayed):
    url = "https://fantasy.premierleague.com/api/entry/%s/event/%s/picks/" % (id, gwplayed)
    json_pick = requests.get(url).json()
    picks_df = pd.DataFrame(json_pick['picks'])
    list = picks_df['element'].to_list()
    return list

def get_name(pick):
    name = players_df.loc[players_df['id']== pick]['web_name'].iloc[-1]
    position = players_df.loc[players_df['id']== pick]['element_type'].iloc[-1]
    points = players_df.loc[players_df['id']== pick]['event_points'].iloc[-1]
    return [name,position,points]


####
drop_list = df_results['entry_name']
#
col1, col2 = st.columns(2)
with col1:
    your_team = st.selectbox("Select Team1",drop_list,key='yours')
with col2:
    their_team = st.selectbox("Select Team2",drop_list)
##
your_team_id = df_results.loc[df_results['entry_name'] == your_team]['entry'].iloc[-1]
their_team_id = df_results.loc[df_results['entry_name'] == their_team]['entry'].iloc[-1]
#
your_list = get_picks(your_team_id,gwplayed)
opp_list = get_picks(their_team_id,gwplayed)

def compare_teams(your_id,their_id,gw):
    col1, col2 = st.columns(2)
    with col1:
        
        pbp = points_by_position(your_list)
        st.plotly_chart(pbp,theme=None,use_container_width=False)
        common = list(set(your_list).intersection(opp_list))
        common_picks = []
        for i in common:
            new = get_name(i)
            common_picks.append(new)
        df_common = pd.DataFrame(common_picks, columns=["Name","Position","GW points"]).sort_values(by=['Position'])
        st.header("Common Players")
        st.dataframe(df_common,hide_index=True,use_container_width=False)
        st.header("Differentials")
        yours = set(your_list).difference(opp_list)
        your_picks = []
        for i in yours:
            new = get_name(i)
            your_picks.append(new)
        df_yours = pd.DataFrame(your_picks, columns=["Name","Position","GW points"]).sort_values(by=['Position'])
        st.dataframe(df_yours, hide_index=True,height=600,use_container_width=False)
####
    with col2:
        
        pbp = points_by_position(opp_list)
        st.plotly_chart(pbp,theme=None,use_container_width=False)
        common = list(set(your_list).intersection(opp_list))
        common_picks = []
        for i in common:
            new = get_name(i)
            common_picks.append(new)
        df_common = pd.DataFrame(common_picks, columns=["Name","Position","GW points"]).sort_values(by=['Position'])
        st.header("Common Players")
        st.dataframe(df_common,hide_index=True,use_container_width=False)
        st.header("Differentials")
        theirs = set(opp_list).difference(your_list)
        their_picks = []
        for i in theirs:
            new = get_name(i)
            their_picks.append(new)
        df_theirs = pd.DataFrame(their_picks, columns=["Name","Position","GW points"]).sort_values(by=['Position'])
        st.dataframe(df_theirs,hide_index=True,height=600,use_container_width=False)
def points_by_position(picks_list):
    team_picks = []
    for i in picks_list:
        new = get_name(i)
        team_picks.append(new)
    df_team_picks = pd.DataFrame(team_picks, columns=["Name","Position","Points"]).groupby('Position',as_index=False).sum()
    fig_pos_scores = px.pie(df_team_picks,values='Points',names='Position',hover_data=['Name'],color='Position',hole=0.2)
    return fig_pos_scores
     
#
#
st.caption("* Additional captain points are not counted")
compare_teams(your_team_id,their_team_id,gwplayed)