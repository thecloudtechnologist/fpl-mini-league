import plotly.express as px
import plotly.graph_objects as go

def plot_total_points(df):
    fig = px.bar(
        df, x="Team_Name", y="Season_Points",color="Season_Points",color_continuous_scale='Rainbow', title="Total Points",text_auto=True
    )
    fig.update_xaxes(title_text="Team name")
    fig.update_yaxes(title_text="Total season points")
    fig.update_layout(xaxis={'categoryorder':'total descending'})
    fig.show()
    fig.update_layout(
    autosize=False,
    width=1200,
    height=600,)
    fig.write_image("web/images/season_points.png")

def plot_total_bench_points(df):
    fig = px.bar(
        df, x="Team_Name", y="season_bench_points",color="season_bench_points",color_continuous_scale='Rainbow', title="Season points on benc",text_auto=True
    )
    fig.update_xaxes(title_text="Team name")
    fig.update_yaxes(title_text="Season points on bench")
    fig.update_layout(xaxis={'categoryorder':'total descending'})
    fig.show()
    fig.update_layout(
    autosize=False,
    width=1200,
    height=600,)
    fig.write_image("web/images/season_bench_points.png")

def plot_gw_bench_points(df):
    fig = px.bar(
        df, x="Team_Name", y="GW_bench_points",color="GW_bench_points",color_continuous_scale='Rainbow', title="Gameweek points left on bench",text_auto=True
    )
    fig.update_xaxes(title_text="Team name")
    fig.update_yaxes(title_text="Gameweek points on bench")
    fig.update_layout(xaxis={'categoryorder':'total descending'})
    fig.show()
    fig.update_layout(
    autosize=False,
    width=1200,
    height=600,)
    
    fig.write_image("web/images/gw_bench_points.png")

def plot_total_vs_bench_points(df):
    # Create a new column that is the sum of total_points and bench_points
    df["total_and_bench_points"] = df["Season_Points"] + df["season_bench_points"]

    # Sort DataFrame by total_and_bench_points from greatest to least
    df = df.sort_values("total_and_bench_points", ascending=False)

    fig = px.bar(
        df,
        x="Team_Name",
        y=["Season_Points", "season_bench_points"],
        title="Total Points vs Points Left on Bench",
        text_auto=True,
    )
    fig.update_xaxes(title_text="Team Name")
    fig.update_yaxes(title_text="Points")
    fig.update_layout(xaxis={'categoryorder':'total descending'})
    fig.show()
    fig.update_layout(
    autosize=False,
    width=1200,
    height=600,)
    fig.write_image("web/images/season_team_bench_points.png")

def plot_team_vs_bench_value(df):
    # Create a new column that is the sum of total_points and bench_points
    df["team_and_bench_value"] = df["Team_Value"] + df["Bank"]

    # Sort DataFrame by total_and_bench_points from greatest to least
    df = df.sort_values("team_and_bench_value", ascending=False)

    fig = px.bar(
        df,
        x="Team_Name",
        y=["Team_Value", "Bank"],
        title="Team value vs bench value",
        text_auto=True,
    )
    fig.update_xaxes(title_text="Team Name")
    fig.update_yaxes(title_text="team_and_bench_value")
    fig.update_layout(xaxis={'categoryorder':'total descending'})
    fig.show()
    fig.update_layout(
    autosize=False,
    width=1200,
    height=600,)
    fig.write_image("web/images/season_team_bank_value.png")

def plot_gw_team_xgi(df):
    fig = px.bar(
        df, x="Team_Name", y="team_XGI",color="team_XGI",color_continuous_scale='Rainbow', title="Gameweek team XGI",text_auto=True
    )
    fig.update_xaxes(title_text="Team name")
    fig.update_yaxes(title_text="expected goal involvements")
    fig.update_layout(xaxis={'categoryorder':'total descending'})
    fig.show()
    fig.update_layout(
    autosize=False,
    width=1200,
    height=600,)
    fig.write_image("web/images/gw_xgi.png")

def plot_gw_team_vs_captain(df):
    fig = px.bar(
        df,
        x="Team_Name",
        y=["cap_vs_team", "GW_Captain_points"],
        title="Team vs Captain points",
        text_auto=True,
)
    fig.update_xaxes(title_text="Team Name")
    fig.update_yaxes(title_text="team_and_captain_points")
    fig.update_layout(xaxis={'categoryorder':'total descending'})
    fig.show()
    fig.update_layout(
    autosize=False,
    width=1200,
    height=600,)
    fig.write_image("web/images/gw_team_vs_captain.png")

def plot_gw_nGW_xp(df):
    fig = px.bar(
        df,
        x="Team_Name",
        y="nxp",
        title="Next GW XP based on same captain choice",
        color="nxp",
        color_continuous_scale='Rainbow',
        text_auto=True,
    )
    fig.update_xaxes(title_text="Team Name")
    fig.update_yaxes(title_text="Next GW expected points")
    fig.update_layout(xaxis={'categoryorder':'total descending'})
    fig.update_layout(
        autosize=False,
        width=1200,
        height=600,)
    fig.show()
    fig.write_image("web/images/gw_nGW_xp.png")

def plot_gw_captain(df):
    fig = px.pie(df, values='count', names='GW_Captain', title='Gameweek captain choice',labels='GW_Captain')
    fig.update_traces(textposition='inside', textinfo='percent+value')
    fig.update_layout(
        autosize=True)
    fig.show()
    fig.write_image("web/images/gw_captain.png")

