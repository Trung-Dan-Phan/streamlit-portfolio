import streamlit as st
import pandas as pd
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
@st.cache_data
def load_data():
    dfs = [pd.read_csv(f'{source_url}/atp_matches_{year}.csv') for year in years]
    all_matches = pd.concat(dfs, ignore_index=True)
    all_matches['tourney_date'] = pd.to_datetime(all_matches['tourney_date'].astype(str), format='%Y%m%d').dt.date
    return all_matches.sort_values(by='tourney_date')

# Load csv files from github repository
data_load_state = st.text('Loading data...')
atp_data = load_data()
# Notify the reader that the data was successfully loaded.
data_load_state.text("Finished loading data")
    
st.title("ATP Head to Head")

def search_players(search_term):
    # Filter for matching player names in both winner_name and loser_name columns
    winners = atp_data[atp_data['winner_name'].str.contains(search_term, case=False, na=False)]['winner_name']
    losers = atp_data[atp_data['loser_name'].str.contains(search_term, case=False, na=False)]['loser_name']
    
    # Combine both series and drop duplicates (equivalent to UNION in SQL)
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
    # Filter matches where either player1 is the winner and player2 is the loser, or vice versa
    filtered_matches = atp_data[
        ((atp_data['loser_name'] == player1) & (atp_data['winner_name'] == player2)) |
        ((atp_data['loser_name'] == player2) & (atp_data['winner_name'] == player1))
    ]
    
    # Select the desired columns
    selected_columns = filtered_matches[['tourney_date', 'tourney_name', 'surface', 'round', 'winner_name', 'score']]
    
    # Sort by tourney_date in descending order
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

left, right = st.columns(2)

# Group by Surface
with left:
    st.markdown('#### By Surface')

    # Group by winner_name (player) and surface, and count wins
    by_surface = sorted_matches.groupby(['winner_name', 'surface']).size().reset_index(name='wins')

    # Pivot to make 'surface' the index and 'winner_name' the columns
    by_surface_pivot = by_surface.pivot(index='surface', columns='winner_name', values='wins')

    # Display the styled DataFrame in Streamlit
    st.dataframe(by_surface_pivot)

# Group by Round
with right:
    st.markdown('#### By Round')

    # Group by winner_name (player) and round, and count wins
    by_round = sorted_matches.groupby(['winner_name', 'round']).size().reset_index(name='wins')

    # Pivot to make 'round' the index and 'winner_name' the columns
    by_round_pivot = by_round.pivot(index='round', columns='winner_name', values='wins')

    # Display the result as a dataframe
    st.dataframe(by_round_pivot)
