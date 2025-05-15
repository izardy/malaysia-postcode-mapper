import pandas as pd
import numpy as np

# Create the sample DataFrame from the input data
data = {
    'postcode': ['57227', '57228', '57229', '57231', '57232', '57233', '57234', '57235', 
                '57236', '57237', '57238', '57239', '57240', '57241'],
    'location': [np.nan] * 14,
    'district': ['LIPIS'] * 14,
    'state': ['PAHANG'] * 14,
    'mukim': ['KUALA LIPIS', 'PENJOM', 'TANJUNG BESAR', 'BANDAR KUALA LIPIS', 'BENTA', 
             'PADANG TENGKU', 'PEKAN PADANG TENGKU', 'PEKAN TAMAN JELAI', 'PEKAN PENJOM', 
             'PEKAN MELA', 'PEKAN KERAMBIT', 'PEKAN RPSB KG. PAGAR', 'PEKAN MERAPUH', 'PEKAN KECHAU TUI']
}

mukim_district_state = pd.DataFrame(data)

# Display the original DataFrame
print("Original DataFrame:")
print(mukim_district_state)
print("\n")

# Update the postcode column using the pattern
# For each mukim in LIPIS district of PAHANG, set the corresponding postcode
# Following the pattern you provided:
mukim_district_state['postcode'] = np.where(
    (mukim_district_state['district'] == 'LIPIS') & 
    (mukim_district_state['state'] == 'PAHANG') & 
    (mukim_district_state['mukim'] == 'KUALA LIPIS'), 
    '27200', 
    mukim_district_state['postcode']
)

mukim_district_state['postcode'] = np.where(
    (mukim_district_state['district'] == 'LIPIS') & 
    (mukim_district_state['state'] == 'PAHANG') & 
    (mukim_district_state['mukim'] == 'PENJOM'), 
    '27210', 
    mukim_district_state['postcode']
)

mukim_district_state['postcode'] = np.where(
    (mukim_district_state['district'] == 'LIPIS') & 
    (mukim_district_state['state'] == 'PAHANG') & 
    (mukim_district_state['mukim'] == 'TANJUNG BESAR'), 
    '27220', 
    mukim_district_state['postcode']
)

mukim_district_state['postcode'] = np.where(
    (mukim_district_state['district'] == 'LIPIS') & 
    (mukim_district_state['state'] == 'PAHANG') & 
    (mukim_district_state['mukim'] == 'BANDAR KUALA LIPIS'), 
    '27200', 
    mukim_district_state['postcode']
)

mukim_district_state['postcode'] = np.where(
    (mukim_district_state['district'] == 'LIPIS') & 
    (mukim_district_state['state'] == 'PAHANG') & 
    (mukim_district_state['mukim'] == 'BENTA'), 
    '27300', 
    mukim_district_state['postcode']
)

mukim_district_state['postcode'] = np.where(
    (mukim_district_state['district'] == 'LIPIS') & 
    (mukim_district_state['state'] == 'PAHANG') & 
    (mukim_district_state['mukim'] == 'PADANG TENGKU'), 
    '27100', 
    mukim_district_state['postcode']
)

# Display the updated DataFrame
print("Updated DataFrame:")
print(mukim_district_state)