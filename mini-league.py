# Imports 
import requests
from prettytable import PrettyTable
from IPython.display import display
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from jinja2 import Template
from functions import *

##############################
# prettytable headers 
##############################
headers = ['Team_Name','GW_Points','Season_Points','current_rank','last_rank','GW_bench_points','season_bench_points','GW_transfers','GW_transfers_cost',
           'Season_transfers','Season_transfers_cost','Team_Value','Bank','Total_Value','GW_Captain','GW_Captain_points','team_XGI','nxp']
table = PrettyTable(headers)

##############################
# input league ID
##############################
league_id = input("Enter your mini league ID:")

##############################
# bootstrap data
##############################
url = 'https://fantasy.premierleague.com/api/bootstrap-static'
json_live = requests.get(url).json()

# Import all player data in premier league
# Player Name
player_d = {}
for each in json_live['elements']:
    pl_position = each['element_type']
    pl_id = each['id']
    pl_name = each['web_name']
    player_d[pl_id] = pl_name
tot_player = len(player_d)

# Player XGI
player_xgi = {}
for each in json_live['elements']:
    pl_position = each['element_type']
    pl_id = each['id']
    pl_xgi = each['expected_goal_involvements']
    player_xgi[pl_id] = pl_xgi

# Player Points
player_ep = {}
for each in json_live['elements']:
    pl_position = each['element_type']
    pl_id = each['id']
    pl_ep = each['event_points']
    player_ep[pl_id] = pl_ep

# Player XP next GW
player_nxp = {}
for each in json_live['elements']:
    pl_position = each['element_type']
    pl_id = each['id']
    pl_xp = each['ep_next']
    player_nxp[pl_id] = pl_xp

##############################
#League data and entry history
############################## 
url1 = "https://fantasy.premierleague.com/api/leagues-classic/%s/standings/" % (league_id)
json_minileague = requests.get(url1).json()

team_entry = {}

# League Name
league_name = json_minileague['league']['name']
print("League name is: " + league_name)

for each in json_minileague['standings']['results']:
    team_name = each['entry_name']
    team_id = each['entry']
    team_entry[team_id] = team_name

# Fetch
appended_history = []
for each in json_minileague['standings']['results']:
    team_name = each['entry_name']
    team_id = each['entry']
    gw_points = each['event_total']
    total_points = each['total']
    current_rank = each['rank']
    last_rank = each['last_rank'] 
    data = [team_name,gw_points,total_points,current_rank,last_rank,]

# Fetching individual team data
    url2 = "https://fantasy.premierleague.com/api/entry/%s/history" % (team_id)
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
        pl_name = player_d[player_id]
        plist = {player_id: pl_name}
        player_idnew = str(player_id)

        if captain == True:
            data.append(pl_name)
            
    
    for each1 in json_pick['picks']:
        player_id = each1['element']
        captain = each1['is_captain']
        pl_name = player_d[player_id]
        plist = {player_id: pl_name}
        player_idnew = str(player_id)
        if captain == True:
            pl_ep = player_ep[player_id]
            data.append(pl_ep * 2)
    
# Team XGI
    total_xgi = 0
    for each1 in json_pick['picks']:
        player_id = each1['element']
        multiplier = each1['multiplier']
        pl_xgi = player_xgi[player_id]
        if multiplier != 0:
            total_xgi = total_xgi + float(pl_xgi)
    total_xgi = round(total_xgi, 2)
    data.append(total_xgi)

# Next GW XP
    total_nxp = 0
    for each1 in json_pick['picks']:
        player_id = each1['element']
        pl_nxp = player_nxp[player_id]
        total_nxp = total_nxp + float(pl_nxp)
        if captain == True:
            total_nxp = float(total_nxp) + float(pl_nxp *2)
        total_nxp = round(total_nxp, 2)
    data.append(total_nxp)

    ##
    df_history = pd.json_normalize(json_history['current'])
    df_history["entry"] = team_name
    appended_history.append(df_history)

    table.add_row(data)

appended_history = pd.concat(appended_history,ignore_index=True)

##############################
# Save data
##############################
tbl_as_csv = table.get_csv_string().replace('\r','')
text_file = open("mini-league.csv", "w")
n = text_file.write(tbl_as_csv)
text_file.close()
##############################
# Read data to pandas dataframe
##############################
df = pd.read_csv('mini-league.csv')
##############################
# Save league table HTML page 
##############################
df2 = df[['Team_Name','Season_Points','GW_Points','GW_bench_points','GW_transfers','GW_Captain','current_rank','last_rank','Total_Value']]
# SAVE table to HTML
html = df2.to_html(index=False)

with open('web/templates/table.html', 'r') as file :
    filedata = file.read()

filedata = filedata.replace('mini_league', html)
filedata = filedata.replace('<table border="1" class="dataframe">', '<table class="sortable-theme-finder" data-sortable>')

with open('web/table.html', 'w') as file:
    file.write(filedata)

##############################
# plotly - League race 
##############################
fig = go.Figure()

for c in appended_history['entry'].unique():
    dfp = appended_history[appended_history['entry']==c].pivot(index='event', columns='entry', values='total_points') 
    fig.add_traces(go.Scatter(x=dfp.index, y=dfp[c], mode='lines+markers', name = str(c)))

fig.update_layout(
    autosize=False,
    width=1200,
    height=1200,)
fig.show()
fig.write_image("web/images/season_League_race.png")

# SAVE HTML
output_html_path=r"web/index.html"
input_template_path = r"web/templates/index.html"

plotly_jinja_data = {"fig":fig.to_html(full_html=False,include_plotlyjs="cdn")}
#consider also defining the include_plotlyjs parameter to point to an external Plotly.js as described above

with open(output_html_path, "w", encoding="utf-8") as output_file:
    with open(input_template_path) as template_file:
        j2_template = Template(template_file.read())
        output_file.write(j2_template.render(plotly_jinja_data))

##############################
# Plotly - plots
##############################
# total points
plot_total_points(df)
#
# Points left on bench (season)
plot_total_bench_points(df)
#
# Points left on bench (GW)
plot_gw_bench_points(df)
#
# Total vs bench points
plot_total_vs_bench_points(df)
#
# Team + In the bank
plot_team_vs_bench_value(df)
#
# Team XGI
plot_gw_team_xgi(df)
#
# Captain vs Team points
df["cap_vs_team"] = df["GW_Points"] - df["GW_Captain_points"]
df_cap_vs_team = df.sort_values("cap_vs_team", ascending=False)
plot_gw_team_vs_captain(df_cap_vs_team)
#
# Next GW expected points
plot_gw_nGW_xp(df)
#
# Captain
df_cap_count = df.groupby(['GW_Captain'])['GW_Captain'].count().reset_index(name='count')
plot_gw_captain(df_cap_count)