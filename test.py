import random

# Generator function for list of matchups from a team_list
def games_from_list(team_list):
    for i in range(4):
        yield team_list[i], team_list[i+4]

# Function to apply rotation to list of teams as described in article
def rotate_list(team_list):
    team_list = [team_list[4]] + team_list[0:3] + team_list[5:8] + [team_list[3]]
    team_list[0], team_list[1] = team_list[1], team_list[0]
    return team_list

# Function to check if a list of games is valid
def checkValid(game_list):
    if len(set(game_list)) != len(game_list):
        return False
    for week in range(14):
        teams = set()
        this_week_games = game_list[week*4:week*4 + 4]
        for game in this_week_games:
            teams.add(game[0])
            teams.add(game[1])
        if len(teams) < 8:
            return False
    else:
        return True


# Generate list of teams & empty list of games played
teams = list(range(8))
games_played = []

# Optionally shuffle teams before generating schedule
random.shuffle(teams)

# For each week -
for week in range(14):
    print(f"Week {week + 1}")

    # Get all the pairs of games from the list of teams.
    for pair in games_from_list(teams):
        # If the matchup has already been played:
        if pair in games_played:
            # Play the opposite match
            pair = pair[::-1]

        # Print the matchup and append to list of games.
        print(f"{pair[0]} vs {pair[1]}")
        games_played.append(pair)

    # Rotate the list of teams
    teams = rotate_list(teams)

# Checks that the list of games is valid 
print(checkValid(games_played))