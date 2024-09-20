# mlb_bet_scraper.py

import requests
from bs4 import BeautifulSoup
import re
import json
import pandas as pd
from datetime import datetime, timedelta
from pybaseball import  playerid_lookup, statcast_pitcher, get_splits, pitching_stats_bref, pitching_stats_range
from dateutil.relativedelta import relativedelta
from sklearn.preprocessing import LabelEncoder


def extract_player_data(url, date):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    scripts = soup.find_all('script')

    script_with_data = None
    for script in scripts:
        if 'offers' in script.text:
            script_with_data = script.text
            break

    if script_with_data:
        json_text_match = re.search(r'(\{.*\})', script_with_data)
        if json_text_match:
            json_text = json_text_match.group(1)
            data = json.loads(json_text)

            player_data = []
            for offer in data['offers']:
                for participant in offer['participants']:
                    first_name = participant['player']['first_name']
                    last_name = participant['player']['last_name']
                    player_short_name = participant['player']['short_name']
                    full_name = f"{first_name} {last_name}"
                    for selection in offer['selections']:
                        if selection['selection'] == 'over':
                            strikeout_value = selection['opening_line']['line']
                            player_data.append({
                                'full_name': full_name,
                                'short_name': player_short_name,
                                'strikeout_value': strikeout_value,
                                'date': date
                            })

            return player_data
    return None



def generate_urls(start_date, end_date):
    urls = []
    current_date = start_date
    while current_date <= end_date:
        date_str = current_date.strftime('%Y-%m-%d')
        url = f"https://www.bettingpros.com/mlb/odds/player-props/strikeouts/?date={date_str}"
        urls.append((url, date_str))
        current_date += timedelta(days=1)
    return urls


def get_player_ids(df):
    player_ids = []
    for i in range(len(df)):
        name_parts = df.iloc[i, 0].split()
        if len(name_parts) == 2:
            firstname, lastname = name_parts
        else:
            firstname = ' '.join(name_parts[:-1])
            lastname = name_parts[-1]

        lookup_result = playerid_lookup(lastname, firstname)
        if not lookup_result.empty:
            # filter to get the most recent player
            recent_player = lookup_result.loc[lookup_result['mlb_played_last'].idxmax()]
            player_id = recent_player['key_mlbam']
            player_ids.append(player_id)
        else:
            print(f"No match found for {firstname} {lastname}")
            player_ids.append(None)
    return player_ids


def get_prior_date(input_date):
    date_obj = datetime.strptime(input_date, '%Y-%m-%d')
    new_date_obj = date_obj - relativedelta(months=2)
    new_date_str = new_date_obj.strftime('%Y-%m-%d')

    return new_date_str
