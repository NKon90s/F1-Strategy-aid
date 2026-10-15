import numpy as np

strat = {'recommended_strategy': {'starting_compound': 'SOFT', 'first_stint': 20, 'second_compound': 'SOFT', 'second_stint': 14, 'third_compound': 'HARD', 'third_stint': np.int64(23), 'pit1_lap': 20, 'pit2_lap': 34, 'race_time': np.float64(5661.37)}, 'alternative_strategy': {'starting_compound': 'SOFT', 'first_stint': 20, 'second_compound': 'HARD', 'second_stint': np.int64(37), 'pit_lap': 20, 'race_time': np.float64(5687.69)}}

alt_strat =  {'recommended_strategy': {'starting_compound': 'MEDIUM', 'first_stint': 22, 'second_compound': 'SOFT', 'second_stint': 14, 'third_compound': 'HARD', 'third_stint': np.int64(23), 'pit1_lap': 20, 'pit2_lap': 34, 'race_time': np.float64(5561.37)}, 'alternative_strategy': {'starting_compound': 'SOFT', 'first_stint': 20, 'second_compound': 'HARD', 'second_stint': np.int64(37), 'pit_lap': 20, 'race_time': np.float64(5677.69)}}

def top_two_strategies(strat, alt_strat):

    strat1 = strat['recommended_strategy']
    strat2 = strat['alternative_strategy']
    strat3 = alt_strat['recommended_strategy']
    strat4 = alt_strat['alternative_strategy']

    strats_idx = ['strat1', 'strat2', 'strat3', 'strat4']
    strats = [strat1, strat2, strat3, strat4]
    t_strats = [strat1['race_time'], strat2['race_time'], strat3['race_time'], strat4['race_time']]
    hash_map = {}
    strat_map = {}
 
    for i, s in enumerate(strats_idx):
        hash_map[s] = t_strats[i]

    for i, s in enumerate(strats_idx):
        strat_map[s] = strats[i]
    
    t_strats.sort()

    for _, s in enumerate(strats_idx):
        if t_strats[0] == hash_map[s]:
            main_strategy = strat_map[s]
        if t_strats[1] == hash_map[s]:
            alt_strategy = strat_map[s]

    return main_strategy, alt_strategy



if __name__ == "__main__":
    rec_strat, alt_strat = top_two_strategies(strat, alt_strat)

    print(rec_strat)
    print(alt_strat)