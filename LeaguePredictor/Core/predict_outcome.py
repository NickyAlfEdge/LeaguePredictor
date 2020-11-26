import cassiopeia as cass
import numpy as np
from cassiopeia import Summoner, Champion
from s3fs.core import S3FileSystem
import requests
import joblib

# Constants
API_KEY = "RGAPI-b08e4291-74cf-465a-9a24-064e1d5cd12f"
URL = {
    'SummonerID':       'https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner}?api_key={key}',
    'Match':            'https://euw1.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/{id}?api_key={key}',
    'ChampionMastery':  'https://euw1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/'
                        '{id}/by-champion/{champid}?api_key={key}'

}
# Cassiopeia riot API wrapper configuration
cass.set_riot_api_key(API_KEY)
cass.set_default_region("EUW")
# instantiate s3 access method, for later ml model loading
s3_file = S3FileSystem()


# Get queried users encrypted summoner ID from the riot API
# for later checks, to ensure the summoner exists and is in-game
def get_sum_id(name):
    response = requests.get(
        URL['SummonerID'].format(
            summoner=name,
            key=API_KEY),
        params=""
    )
    if response.status_code != 200:
        error_code = str(response.status_code)
        error_message = response.reason
        return error_code + " " + error_message
    else:
        return response.json()['id']


# Get queried users match data by calling the corresponding riot API
# with the prior gathered encrypted summoner ID. To check if the user exists and is in-game
def get_match_data(summoner_id):
    if summoner_id == "Error":
        return "Error"
    else:
        response = requests.get(
            URL['Match'].format(
                id=summoner_id,
                key=API_KEY),
            params=""
        )
        if response.status_code != 200:
            error_code = str(response.status_code)
            error_message = response.reason
            return error_code + " " + error_message
        else:
            return response.status_code


# Get the current match data for the queried user via the cassiopeia riot api wrapper
# for easier manipulation of the returned data
def get_match(name):
    match = Summoner(name=name).current_match
    return match


# Load the match data via the riot API and format it for the machine learning prediction model
# to predict the outcome of the game
def load_match_data(name):
    match = get_match(name)
    if match.mode != match.mode.classic:
        return "Error"
    else:
        participants = match.participants
        blue_bans = match.blue_team.bans
        red_bans = match.red_team.bans
        blue_team_data = []
        red_team_data = []
        for index, participant in enumerate(participants):
            if participant.side == participant.side.blue:
                blue_team_data.append(participant.champion.id)
                blue_participant_mastery = cass.get_champion_mastery(Summoner(name=participant.summoner.name),
                                                                     Champion(name=participant.champion.name,
                                                                              id=participant.champion.id)).points
                blue_team_data.append(blue_participant_mastery)
                blue_participant_ban = str(blue_bans[index + 1]).split(",")[1].strip(" id=")
                blue_team_data.append(int(blue_participant_ban))
            else:
                red_team_data.append(participant.champion.id)
                red_participant_mastery = cass.get_champion_mastery(Summoner(name=participant.summoner.name),
                                                                    Champion(name=participant.champion.name,
                                                                             id=participant.champion.id)).points
                red_team_data.append(red_participant_mastery)
                red_participant_ban = str(red_bans[index + 1]).split(",")[1].strip(" id=")
                red_team_data.append(int(red_participant_ban))
        return np.asarray(blue_team_data + red_team_data)


# call riot api methods to validate the match status of a queried account
# ensuring they are in-game prior to passing to the prediction model
def get_match_status(name):
    sum_id = get_sum_id(name)
    if " " in sum_id:
        return sum_id
    else:
        match_status = get_match_data(sum_id)
        if match_status != 200:
            return match_status


# call the game data function and collate the game data, ensuring it is
# in the correct format to then be applied to the prediction model
def get_game_data(name):
    game_data = load_match_data(name)
    # flags warning for comparison of numpy value and string comparison
    if "Error" not in game_data:
        return game_data
    else:
        return "Error, game mode isn't classic"


# Call the appropriate methods and return the corresponding value, be it an error code
# or the predicted outcome of the game, if successful
def prediction(game_data):
    # load gradient boosting trained model from s3 bucket
    model = joblib.load(s3_file.open('{}/{}'.format("ml-model-leaguepredictor", "model.pkl")))
    result = model.predict([game_data])
    if result == 1:
        return "Based on team picks, bans and mastery levels. The Blue Team is predicted to win. Have fun!"
    elif result == 2:
        return "Based on team picks, bans and mastery levels. The Red Team is predicted to win. Have fun!"
    else:
        return "There was an error with the prediction model"
