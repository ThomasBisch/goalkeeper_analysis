import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.patheffects as path_effects
from highlight_text import fig_text
import requests

# Function to download a file from a URL
def download_file(url, filename):
    response = requests.get(url)
    response.raise_for_status()  # Check for request errors
    with open(filename, 'wb') as file:
        file.write(response.content)

# URLs of the font files
free_sans_url = "https://raw.githubusercontent.com/ThomasBisch/goalkeeper_analysis/main/FreeSans.ttf"
alegreya_sans_bold_url = "https://raw.githubusercontent.com/ThomasBisch/goalkeeper_analysis/main/AlegreyaSans-Bold.ttf"

# Download the font files
download_file(free_sans_url, "FreeSans.ttf")
download_file(alegreya_sans_bold_url, "AlegreyaSans-Bold.ttf")

# Load data from GitHub
file_url = "https://raw.githubusercontent.com/ThomasBisch/goalkeeper_analysis/main/GK_MAIN_DB.xlsx"
df = pd.read_excel(file_url)

# Calculate the means for the x and y axes
mean_x = df['Shots Against per 90'].mean()
mean_y = df['Goals Prevented %'].mean()

# Load the custom font from the downloaded files
custom_font_path = "FreeSans.ttf"
custom_font = fm.FontProperties(fname=custom_font_path, size=24)  # Increased font size

# Load the custom bold font for the title from the downloaded files
bold_font_path = "AlegreyaSans-Bold.ttf"
bold_font = fm.FontProperties(fname=bold_font_path, size=40)  # Increased font size

# Streamlit app
st.title("Goalkeeper Goals Prevented % Analysis")

# Instructions
st.markdown("""
## Instructions

1. **Load Data**: Locate the player you want. There is a search toggle in the top right, where you can search for the player or club.
2. **Input Player Details**: You can copy and paste from the table above, related to the player, team, and age.
3. **Generate Plot**: Once all the relevant information is inputted, press enter, and the scatter plot will automatically update to highlight the selected player.
""")

# Display the table of players
st.subheader("Players List")
# Include 'Height' and 'Passport country' columns, and sort by 'Player'
players_table = df[['Player', 'Team', 'Age', 'Height', 'Passport country']].sort_values(by='Player')
# Limit the number of rows displayed and add scrolling (height adjusted for 10 rows)
st.dataframe(players_table, height=400)  # Height adjusted to show 10 rows

# User inputs
st.subheader("Search for a Player")
player_name = st.text_input("Enter Player's Name")
player_team = st.text_input("Enter Player's Team")
player_age = st.number_input("Enter Player's Age", min_value=15, max_value=50, step=1)

# Function to create and display the plot
def create_plot(player_name, player_team, player_age):
    filtered_df = df[(df['Player'] == player_name) & (df['Team'] == player_team) & (df['Age'] == player_age)]

    if not filtered_df.empty:
        goals_prevented = filtered_df['Goals Prevented %'].values[0]
        st.write(f"Goals Prevented %: {goals_prevented}")

        # Plot the scatter plot
        fig, ax = plt.subplots(figsize=(20, 12), dpi=300, facecolor='#1e1b21')  # Increased figure size

        # Plot each player with dark blue
        plt.scatter(df['Shots Against per 90'], df['Goals Prevented %'], color='#2a282c', s=150, alpha=0.4, zorder=3)

        # Highlight the specific player in red
        plt.scatter(filtered_df['Shots Against per 90'], filtered_df['Goals Prevented %'], color='#e9575d', s=250, alpha=0.9, label=player_name, zorder=5)

        # Add labels for the selected player
        for idx, row in filtered_df.iterrows():
            x, y = row['Shots Against per 90'], row['Goals Prevented %']
            text = f"{row['Player']}\n{row['Team']}"
            txt = plt.text(x, y, text, fontsize=20, ha='center', va='top', color='white', zorder=10, fontproperties=custom_font)
            txt.set_path_effects([path_effects.Stroke(linewidth=3, foreground='black'), path_effects.Normal()])
            # Adjust the y position for the label to be below the dot
            txt.set_y(y - 1)  # Adjusting by 1 unit to place the label below

        # Plot mean lines for both axes
        plt.axvline(x=mean_x, color='white', linestyle='--', linewidth=2, zorder=1)
        plt.axhline(y=mean_y, color='white', linestyle='--', linewidth=2, zorder=1)

        # Add grid lines
        plt.grid(color='white', linestyle='--', linewidth=1, alpha=0.2)

        # Remove top and right spines
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('white')
        ax.spines['bottom'].set_color('white')

        # Set the axes color
        ax.set_facecolor('#1e1b21')

        # Set labels and title
        plt.xlabel('Shots Against per 90', fontproperties=custom_font, color='white', fontsize=24)
        plt.ylabel('Goals Prevented %', fontproperties=custom_font, color='white', fontsize=24)

        # Set the x and y tick colors and font family
        ax.tick_params(axis='x', colors='white', labelsize=20)
        ax.tick_params(axis='y', colors='white', labelsize=20)
        for label in (ax.get_xticklabels() + ax.get_yticklabels()):
            label.set_fontproperties(custom_font)

        # Add titles and subtitles
        fig_text(
            x=0.12, y=0.965,
            s="Goals Prevented %",
            va="bottom", ha="center",
            fontsize=40, color="#e9575d",
            fontproperties=bold_font  # Using the bold font for the title
        )

        fig_text(
            x=0.285, y=0.935,
            s="Minimum 15 Games Played | Data via Wyscout | Created by @motBischoff",
            va="bottom", ha="center",
            fontsize=24, color="white",
            fontproperties=custom_font
        )

        fig_text(
            x=0.4225, y=0.905,
            s="A goalkeeper who achieves a goals prevented percentage of 30% has outperformed the average goalkeeper by saving 30% more goals",
            va="bottom", ha="center",
            fontsize=20, color="white",
            fontproperties=custom_font
        )

        # Show plot
        st.pyplot(fig)

        # Display the player's name and team below the plot
        st.markdown(f"**Player:** {player_name}  \n**Team:** {player_team}")

    else:
        st.write("Player not found. Please check the name, team, or age.")

# Call the function to create and display the plot based on user input
if player_name and player_team and player_age:
    create_plot(player_name, player_team, player_age)
