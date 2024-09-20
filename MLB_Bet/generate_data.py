# generate_data.py

from mlb_bet_scraper import *


start_date = datetime(2024, 7, 25) # specify dates
end_date = datetime(2024, 9, 25)

urls_with_dates = generate_urls(start_date, end_date)

all_player_data = []

for url, date in urls_with_dates:
    player_data = extract_player_data(url, date)
    if player_data:
        all_player_data.extend(player_data)

df = pd.DataFrame(all_player_data)

df_pitchers = pitching_stats_range("2024-08-01", "2024-08-05")

empty_row_template = pd.DataFrame(columns=df_pitchers.columns)

playerids = get_player_ids(df)
player_rows_list = []

last_start_date = None
last_end_date = None
df_pitchers_find = None

for i in range(len(df)):
    end_date = df['date'][i]
    start_date = get_prior_date(end_date)

    if start_date != last_start_date or end_date != last_end_date:
        df_pitchers_find = pitching_stats_range(start_date, end_date)
        last_start_date = start_date
        last_end_date = end_date

    player_id = str(playerids[i])

    if player_id == 'None':
        empty_row = empty_row_template.copy()
        empty_row.loc[0, 'date'] = start_date
        player_rows_list.append(empty_row)
    else:
        player_row = df_pitchers_find.loc[df_pitchers_find['mlbID'] == player_id]
        player_rows_list.append(player_row)


new_df = pd.concat(player_rows_list, ignore_index=True)
features_df = full_df.drop(columns=['full_name', 'short_name', 'SV', 'Name', '#days', 'Lev'])
targets_lookup_df = full_df[['strikeout_value', 'date', 'mlbID']]
targets_lookup_df = targets_lookup_df.dropna(subset=['mlbID'])

# today's data
last_date = None
lookup = None
over_under = []

for i in range(len(targets_lookup_df)):
    id = targets_lookup_df.iloc[i,2]
    date = targets_lookup_df.iloc[i,1]
    
    if date != last_date:
        lookup = pitching_stats_range(date, date)
        last_date = date
    row = lookup.loc[lookup['mlbID'] == id]

    if not row.empty:
        true_strikeouts = row['SO'].values[0]
        pred_strikeouts = targets_lookup_df.iloc[i,0]

        if true_strikeouts > pred_strikeouts:
            over_under.append(1)
        else:
            over_under.append(0)
    else:
        over_under.append(None)

targets_df = pd.DataFrame(over_under, columns=['Over_Under'])
