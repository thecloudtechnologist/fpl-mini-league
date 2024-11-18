import streamlit as st
import requests
import pandas as pd
from prettytable import PrettyTable
import plotly.express as px
import plotly.graph_objects as go
from functions import *
from io import StringIO
##############################
# page config
st.set_page_config(
    page_title="Welcome to FPL mini-league analyser", page_icon=":soccer:",layout="wide"
)

# sidebar
with st.sidebar:
    st.title(""":soccer: *Mini-League Analyser*""")
    st.caption("Your mini-league insights as graphs")
    st.caption("--------------------")
    st.markdown(""" *Checkout my other FPL tools* """)
    st.link_button("FPL Infographics", "https://fpl-infographics.streamlit.app", icon=":material/search_insights:")
    st.caption("FPL data, stats as graphs and Charts")
    st.link_button("Personalised watchlist", "https://fplmate.streamlit.app", icon=":material/eye_tracking:")
    st.caption("Get your team performance, mini-league performance and Watch list picks based on expected goal involvements, points per game, Form, next gameweek expected points and Infuence+Creativity+Threat rank ")
    
##############################
# prettytable headers 
##############################
headers = ['Team_Name','GW_Points','Season_Points','current_rank','last_rank','GW_bench_points','season_bench_points','GW_transfers','GW_transfers_cost',
           'Season_transfers','Season_transfers_cost','Team_Value','Bank','Total_Value','GW_Captain','GW_Captain_points','team_XGI','nxp']
table = PrettyTable(headers)

url = 'https://fantasy.premierleague.com/api/bootstrap-static'
json_live = requests.get(url).json()
elements = json_live['elements']
df_elements = pd.DataFrame(elements)
#############################
def leage_analysys(league_id):
    url1 = "https://fantasy.premierleague.com/api/leagues-classic/%s/standings/" % (league_id)
    json_minileague = requests.get(url1).json()
    results = json_minileague['standings']['results']
    df_results = pd.DataFrame(results)

    appended_history = []
    for i in df_results['entry']:
        team_name = df_results.loc[df_results['entry'] == i]['entry_name'].iloc[-1]
        team_id = i
        gw_points = df_results.loc[df_results['entry'] == i]['event_total'].iloc[-1]
        total_points = df_results.loc[df_results['entry'] == i]['total'].iloc[-1]
        current_rank = df_results.loc[df_results['entry'] == i]['rank'].iloc[-1]
        last_rank = df_results.loc[df_results['entry'] == i]['last_rank'].iloc[-1]
        data = [team_name,gw_points,total_points,current_rank,last_rank,]
    # Entry history
        url2 = "https://fantasy.premierleague.com/api/entry/%s/history" % (i)
        json_history = requests.get(url2).json()
        gwplayed = int(len(json_history['current'])-1)
    # Points benched
        points_benched = json_history['current'][gwplayed]['points_on_bench']
        data.append(points_benched)
    # Season bench points
        season_bench_points = 0
        for gw in range(0,gwplayed+1):
            gw_bench_points = json_history['current'][gw]['points_on_bench']
            season_bench_points = season_bench_points + gw_bench_points
        data.append(season_bench_points)
# Event Transfers Made / Cost
        transfers_made = json_history['current'][gwplayed]['event_transfers']
        transfers_cost = json_history['current'][gwplayed]['event_transfers_cost']
        data.append(transfers_made)
        data.append(transfers_cost)
# Season transfers Made
        season_transfers = 0
        for gw in range(0,gwplayed+1):
            gw_transfers = json_history['current'][gw]['event_transfers']
            season_transfers = season_transfers + gw_transfers
        data.append(season_transfers)
# Season transfers cost
        season_transfers_cost = 0
        for gw in range(0,gwplayed+1):
            gw_transfers = json_history['current'][gw]['event_transfers_cost']
            season_transfers = season_transfers + gw_transfers
        data.append(season_transfers_cost)
# Team Values
        team_value = json_history['current'][gwplayed]['value']
        tv = team_value/10
        in_the_bank = json_history['current'][gwplayed]['bank']
        itb = in_the_bank/10
        total_value = (tv+itb)
        data.append(tv)
        data.append(itb)
        data.append("%.1f" % total_value)
# Cap and vCap
        url4 = "https://fantasy.premierleague.com/api/entry/%s/event/%s/picks/" % (team_id, gwplayed+1)
        json_pick = requests.get(url4).json()
        for each1 in json_pick['picks']:
            player_id = each1['element']
            captain = each1['is_captain']
            vicecapt = each1['is_vice_captain']
            multiplier = each1['multiplier']
            pl_name = df_elements.loc[df_elements['id']== player_id]['web_name'].iloc[-1]
            plist = {player_id: pl_name}
            player_idnew = str(player_id)
            if captain == True:
                data.append(pl_name)
            
        for each1 in json_pick['picks']:
            player_id = each1['element']
            captain = each1['is_captain']
            pl_name = df_elements.loc[df_elements['id']== player_id]['web_name'].iloc[-1]
            plist = {player_id: pl_name}
            player_idnew = str(player_id)
            if captain == True:
                pl_ep = df_elements.loc[df_elements['id']== player_id]['event_points'].iloc[-1]
                data.append(pl_ep * 2)
# Team XGI
        total_xgi = 0
        for each1 in json_pick['picks']:
            player_id = each1['element']
            multiplier = each1['multiplier']
            pl_xgi = df_elements.loc[df_elements['id']== player_id]['expected_goal_involvements'].iloc[-1]
            if multiplier != 0:
                total_xgi = total_xgi + float(pl_xgi)
        total_xgi = round(total_xgi, 2)
        data.append(total_xgi)
# Next GW XP
        total_nxp = 0
        for each1 in json_pick['picks']:
            player_id = each1['element']
            pl_nxp = df_elements.loc[df_elements['id']== player_id]['ep_next'].iloc[-1]
            total_nxp = total_nxp + float(pl_nxp)
            if captain == True:
                total_nxp = float(total_nxp) + float(pl_nxp *2)
            total_nxp = round(total_nxp, 2)
        data.append(total_nxp)
        table.add_row(data)
##
        df_history = pd.json_normalize(json_history['current'])
        df_history["entry"] = team_name
        appended_history.append(df_history)
    appended_history = pd.concat(appended_history,ignore_index=True)
##############################
# Create DF
##############################
    tbl_as_csv = table.get_csv_string().replace('\r','')
    string_data = StringIO(tbl_as_csv)
    df = pd.read_csv(string_data, sep=",")
##############################
# Plots
##############################
## League race
    fig = go.Figure()
    for c in appended_history['entry'].unique():
        dfp = appended_history[appended_history['entry']==c].pivot(index='event', columns='entry', values='total_points') 
        fig.add_traces(go.Scatter(x=dfp.index, y=dfp[c], mode='lines+markers', name = str(c)))
    fig.update_layout(autosize=False,width=1600,height=1200,)
# total points
    fig_tp = plot_total_points(df)
    
# Points left on bench (season)
    fig_s_bench = plot_total_bench_points(df)
    
# Points left on bench (GW)
    fig_w_bench = plot_gw_bench_points(df)
    
# Total vs bench points
    fig_points = plot_total_vs_bench_points(df)
    
# Team + In the bank
    fig_tv = plot_team_vs_bench_value(df)
    
# Team XGI
    fig_xgi = plot_gw_team_xgi(df)
    
# Captain vs Team points
    df["cap_vs_team"] = df["GW_Points"] - df["GW_Captain_points"]
    df_cap_vs_team = df.sort_values("cap_vs_team", ascending=False)
    fig_team = plot_gw_team_vs_captain(df_cap_vs_team)
    
# Next GW expected points
    fig_ep = plot_gw_nGW_xp(df)
    
# Captain
    df_cap_count = df.groupby(['GW_Captain'])['GW_Captain'].count().reset_index(name='count')
    fig_cap = plot_gw_captain(df_cap_count)
    
##############################
# streamlit tabs
##############################
    st.header("League Race")
    st.plotly_chart(fig,theme=None, use_container_width=False)
    st.header("Gameweek stats")
    tab1,tab2,tab3,tab4,tab5,tab6 = st.tabs(["Captain choice","Team vs Captain points","Points on bench","Team+bench points","Team xGI","Next GW expected points"])
    with tab1:
        st.plotly_chart(fig_cap,theme=None, use_container_width=False)
    with tab2:
        st.plotly_chart(fig_team,theme=None, use_container_width=False)
    with tab3:
        st.plotly_chart(fig_w_bench,theme=None, use_container_width=False)
    with tab4:
        st.plotly_chart(fig_points,theme=None, use_container_width=False)
    with tab5:
        st.plotly_chart(fig_xgi,theme=None, use_container_width=False)
    with tab6:
        st.plotly_chart(fig_ep,theme=None, use_container_width=False)
    st.header("Season stats")
    taba,tabb,tabc = st.tabs(["Total Points","points on bench(season)","Team Value"])
    with taba:
        st.plotly_chart(fig_tp,theme=None, use_container_width=False)
    with tabb:
        st.plotly_chart(fig_s_bench,theme=None, use_container_width=False)
    with tabc:
        st.plotly_chart(fig_tv,theme=None, use_container_width=False)
##############################
# league ID
##############################
league_id = st.text_input("Enter mini-league ID")
##############################
if st.button('Analyse..'):
    with st.spinner("Analysis ongoing"):
        leage_analysys(league_id)
        st.balloons()
        st.text("success")
##############################