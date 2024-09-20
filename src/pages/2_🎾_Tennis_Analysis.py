import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from streamlit_searchbox import st_searchbox

st.title('Tennis Analytics 🎾')

st.markdown(
    """
    This application provides comprehensive analytics on ATP tennis matches, offering insights into historical player performances from 2000 to 2022. It allows users to explore head-to-head matchups between players, view match results, and analyze player performance across different surfaces and tournament rounds.

    - **Data Source:** The dataset contains ATP match results from 2000 to 2022, aggregated from [this GitHub repository](https://github.com/mneedham/tennis_atp).
    - **Player Search:** Use the search boxes to find specific players and compare their head-to-head records.
    - **Match Analysis:** Analyze past match results, including scores and tournament details, sorted by date.
    - **Surface & Round Breakdown:** Review player performance based on the surface (e.g., grass, clay, hard court) or tournament round.

    This tool is ideal for tennis enthusiasts, analysts, or anyone looking to dive deep into ATP match data and gain insights into player rivalries and trends.
    """
)

# Define the list of years for which you have CSV files
years = range(2000, 2023)  # This will cover from 2000 to 2022
source_url = "https://raw.githubusercontent.com/mneedham/tennis_atp/master"

# Add a checkbox for filtering Grand Slam matches
filter_grand_slams = st.checkbox('Keep only Grand Slam Matches')

@st.cache_data
def load_data(filter_grand_slams=False):
    """
    Load ATP match data from CSV files, optionally filtering to include only Grand Slam matches.

    Parameters:
    filter_grand_slams (bool): If True, filter data to include only Grand Slam tournaments.

    Returns:
    pd.DataFrame: A DataFrame containing the loaded and optionally filtered ATP match data.
    """
    grand_slams = ['Australian Open', 'Roland Garros', 'Wimbledon', 'US Open']
    dfs = [pd.read_csv(f'{source_url}/atp_matches_{year}.csv') for year in years]
    all_matches = pd.concat(dfs, ignore_index=True)
    all_matches['tourney_date'] = pd.to_datetime(all_matches['tourney_date'].astype(str), format='%Y%m%d').dt.date
    
    if filter_grand_slams:
        all_matches = all_matches[all_matches['tourney_name'].isin(grand_slams)]
    
    return all_matches.sort_values(by='tourney_date')

# Load data based on user selection
data_load_state = st.text('Loading data...')
atp_data = load_data(filter_grand_slams=filter_grand_slams)
data_load_state.text("Finished loading data")

st.title("ATP Head to Head")

def search_players(search_term):
    """
    Search for player names based on a search term, returning a list of unique player names found.

    Parameters:
    search_term (str): The term to search for in player names.

    Returns:
    list: A list of unique player names matching the search term.
    """
    winners = atp_data[atp_data['winner_name'].str.contains(search_term, case=False, na=False)]['winner_name']
    losers = atp_data[atp_data['loser_name'].str.contains(search_term, case=False, na=False)]['loser_name']
    
    players = pd.concat([winners, losers]).drop_duplicates().tolist()
    
    return players

left, right = st.columns(2)
with left:
    player1 = st_searchbox(search_players, label="Player 1", key="player1_search")
with right:
    player2 = st_searchbox(search_players, label="Player 2", key="player2_search")

st.markdown("***")

st.header(f"{player1} vs {player2}")

def matches_for_players(player1, player2):
    """
    Retrieve matches between two players and return a DataFrame of match details.

    Parameters:
    player1 (str): The name of the first player.
    player2 (str): The name of the second player.

    Returns:
    pd.DataFrame: A DataFrame containing match details between the two players.
    """
    filtered_matches = atp_data[
        ((atp_data['loser_name'] == player1) & (atp_data['winner_name'] == player2)) |
        ((atp_data['loser_name'] == player2) & (atp_data['winner_name'] == player1))
    ]
    
    selected_columns = filtered_matches[['tourney_date', 'tourney_name', 'tourney_level', 'surface', 'round', 'winner_name', 'score']]
    
    sorted_matches = selected_columns.sort_values(by='tourney_date', ascending=False)

    return sorted_matches

sorted_matches = matches_for_players(player1=player1, player2=player2)

# Using button to toggle data
if st.checkbox('Show latest match results'):
    st.subheader('Latest results:')
    st.write(sorted_matches.head())

player1_wins = sorted_matches[sorted_matches.winner_name == player1].shape[0]
player2_wins = sorted_matches[sorted_matches.winner_name == player2].shape[0]
st.header(f"{player1} {player1_wins}-{player2_wins} {player2}")

def plot_outcome_summary(player1_wins, player2_wins):
    """
    Plot a pie chart summarizing the win outcomes between two players.

    Parameters:
    player1_wins (int): The number of matches won by Player 1.
    player2_wins (int): The number of matches won by Player 2.
    """
    st.subheader('Match Outcome Summary')
    fig, ax = plt.subplots()
    labels = [player1, player2]
    sizes = [player1_wins, player2_wins]
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    ax.axis('equal')
    plt.title('Match Outcome Summary')
    st.pyplot(fig)

plot_outcome_summary(player1_wins, player2_wins)

left, right = st.columns(2)

def plot_performance_by_surface(by_surface_pivot):
    """
    Plot the performance of players by surface type using a stacked bar chart.

    Parameters:
    by_surface_pivot (pd.DataFrame): A DataFrame with win counts by surface and player.
    """
    st.subheader('Performance by Surface')
    fig, ax = plt.subplots()
    by_surface_pivot.plot(kind='bar', stacked=True, ax=ax)
    plt.title('Performance by Surface')
    plt.xlabel('Surface')
    plt.ylabel('Wins')
    plt.legend(title='Player')
    st.pyplot(fig)

def plot_performance_by_round(by_round_pivot):
    """
    Plot the performance of players by round type using a stacked bar chart.

    Parameters:
    by_round_pivot (pd.DataFrame): A DataFrame with win counts by round and player.
    """
    st.subheader('Performance by Round')
    fig, ax = plt.subplots()
    by_round_pivot.plot(kind='bar', stacked=True, ax=ax)
    plt.title('Performance by Round')
    plt.xlabel('Round')
    plt.ylabel('Wins')
    plt.legend(title='Player')
    st.pyplot(fig)

# Group by Surface
with left:
    st.markdown('#### By Surface')
    by_surface = sorted_matches.groupby(['winner_name', 'surface']).size().reset_index(name='wins')
    by_surface_pivot = by_surface.pivot(index='surface', columns='winner_name', values='wins')
    st.dataframe(by_surface_pivot)

# Group by Round
with right:
    st.markdown('#### By Round')
    by_round = sorted_matches.groupby(['winner_name', 'round']).size().reset_index(name='wins')
    by_round_pivot = by_round.pivot(index='round', columns='winner_name', values='wins')
    st.dataframe(by_round_pivot)

plot_performance_by_surface(by_surface_pivot)
plot_performance_by_round(by_round_pivot)

def plot_head_to_head_performance(sorted_matches):
    """
    Plot the head-to-head performance of players over time using a line chart.

    Parameters:
    sorted_matches (pd.DataFrame): A DataFrame containing match details between players.
    """
    sorted_matches['year'] = pd.to_datetime(sorted_matches['tourney_date']).dt.year
    sorted_matches['month'] = pd.to_datetime(sorted_matches['tourney_date']).dt.month
    
    head_to_head_by_year = sorted_matches.groupby(['year', 'winner_name']).size().reset_index(name='wins')
    head_to_head_by_year['wins'] = head_to_head_by_year['wins'].astype(int)

    head_to_head_pivot = head_to_head_by_year.pivot(index='year', columns='winner_name', values='wins').fillna(0)
    
    st.subheader('Head-to-Head Performance Over Time')
    fig, ax = plt.subplots()
    head_to_head_pivot.plot(kind='line', marker='o', ax=ax)
    plt.title('Head-to-Head Performance Over Time')
    plt.xlabel('Year')
    plt.ylabel('Wins')
    plt.legend(title='Player')
    st.pyplot(fig)

plot_head_to_head_performance(sorted_matches)
