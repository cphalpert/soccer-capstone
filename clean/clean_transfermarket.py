"""
Clean the transfermarket data

Operations:
    - Dedupe arrivals / departures by player
    - Remove any transfers with 
"""
import pandas as pd
import numpy as np

ARRIVALS_FILE = '../scraper/output/arrivals.p'
DEPARTURES_FILE = '../scraper/output/departures.p'

arrivals = pd.read_pickle(ARRIVALS_FILE)
departures = pd.read_pickle(DEPARTURES_FILE)

# Merge arrivals and departures
def merge_arrivals_departures(arrivals, departures):
    # Join on player name and year
    all = arrivals.merge(departures, left_on=['Arrivals','year'], 
                    right_on=['Departures', 'year'], how='outer', suffixes=['_a', '_d'])

    # Some players transfer multiple times per year so we need to also check for 
    # consistency in the team names
    both_transfers = all[(all['index_a'].notnull() & all['index_d'].notnull())]
    from_match = (both_transfers['Moving from'] == both_transfers['team_name_d'])
    to_match = (both_transfers['Moving to'] == both_transfers['team_name_a'])
    drop_rows = both_transfers[~(from_match & to_match)].index
    all = all.drop(drop_rows).reset_index(drop=True)
    return all

all = merge_arrivals_departures(arrivals, departures)

def check_value_consistency(df, column_1, column_2):
    """Ensure that if both column 1 and 2 exist that their values match"""
    has_both = (df[column_1].notnull() & df[column_2].notnull())
    both = df[has_both]
    try:
        assert (both[column_1] == both[column_2]).all() == True
    except:
        return both[both[column_1] != both[column_2]].head()



# integrity checks
check_value_consistency(all, 'Arrivals', 'Departures')
check_value_consistency(all, 'Market value_a', 'Market value_d')
check_value_consistency(all, 'Transfer fee_a', 'Transfer fee_d')
check_value_consistency(all, 'Pos_a', 'Pos_d')
check_value_consistency(all, 'Pos_a', 'Pos_d')

# TODO: Merge duplicate columns
def merge_columns(df, col_1, col_2, new_col):
    """Take first value that exists from col1, col2 and add it to the new column
    Deletes the old columns
    """
    df[new_col] = np.where(df[col_1].isnull(), df[col_2], df[col_1])
    df = df.drop([col_1, col_2], axis=1)
    return df

all = merge_columns(all, 'Arrivals', 'Departures', 'Name')
all = merge_columns(all, 'Market value_a', 'Market value_d', 'Market value')
all = merge_columns(all, 'Transfer fee_a', 'Transfer fee_d', 'Transfer fee')
all = merge_columns(all, 'Pos_a', 'Pos_d', 'Position')




# Drop all observations where there's no market value

# TODO: output pickle file
all.to_pickle("../data/clean_transfermarket.p")
