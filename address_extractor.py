from langchain_ollama import OllamaEmbeddings
import chromadb
import pandas as pd
import warnings
warnings.filterwarnings('ignore', category=pd.errors.DtypeWarning)

# Initialize the persistent ChromaDB client
chroma_client = chromadb.PersistentClient(path="./vectorstore")
# Load the collection with the address metadata
address = chroma_client.get_collection(name="address_metadata")
# Initialize the OllamaEmbeddings model
oembed = OllamaEmbeddings(model="llama3.2:1b")

# Load the locations data
state = pd.read_csv("malaysia-postcodes-location-mukim-district-state.csv")[["state"]].drop_duplicates()['state'].str.lower().tolist()
district = pd.read_csv("malaysia-postcodes-location-mukim-district-state.csv")[["district"]].drop_duplicates()['district'].str.lower().tolist()
mukim = pd.read_csv("malaysia-postcodes-location-mukim-district-state.csv")[["mukim"]].dropna().drop_duplicates()['mukim'].str.lower().tolist()
location = pd.read_csv("malaysia-postcodes-location-mukim-district-state.csv")[["location"]].dropna().drop_duplicates()['location'].str.lower().tolist()

str = "235, pintasan mayang 1, persiaran mayang pasir, 11900, mukim 12, pulau pinang"

# find the state, district, mukim and location in the string
state_found = [s for s in state if s in str.lower()] # case len = 1 , case len = 0 , case len > 1
district_found = [d for d in district if d in str.lower()]
mukim_found = [m for m in mukim if m in str.lower()]
location_found = [l for l in location if l in str.lower()]  # Convert float to string

state_update = []
district_update = []
mukim_update = []
location_update = []

# level 1,2,3,4
state = pd.read_csv("malaysia-postcodes-location-mukim-district-state.csv")[["state"]].drop_duplicates()['state'].str.lower().tolist()
district = pd.read_csv("malaysia-postcodes-location-mukim-district-state.csv")[["district"]].drop_duplicates()['district'].str.lower().tolist()
mukim = pd.read_csv("malaysia-postcodes-location-mukim-district-state.csv")[["mukim"]].dropna().drop_duplicates()['mukim'].str.lower().tolist()
location = pd.read_csv("malaysia-postcodes-location-mukim-district-state.csv")[["location"]].dropna().drop_duplicates()['location'].str.lower().tolist()

# find the state, district, mukim and location in the string
state_found = [s for s in state if s in str.lower()] # case len = 1 , case len = 0 , case len > 1
district_found = [d for d in district if d in str.lower()]
mukim_found = [m for m in mukim if m in str.lower()]
location_found = [l for l in location if l in str.lower()]  # Convert float to string

# 1)
if len(state_found) == 1:                                                                                                                 
    state_update=state_update+(state_found)
    state = pd.read_csv("malaysia-postcodes-location-mukim-district-state.csv")
    #filter state_found
    state = state[state['state'].str.lower() == state_found[0]]
    #update district_found
    district = state[["district"]].drop_duplicates()['district'].str.lower().tolist()
    district_found = [d for d in district if d in str.lower()]

    ####################################################################################################################

    # 2)
    if district_found:                                                                                                                              
        for district in district_found:
            # district name is not the same as state name
            # 2a)
            if district != state_found[0]:                                                                                                   
                district_update=district_update+([district])
                # filter the district
                district_case1 = state[state['district'].str.lower() == district]
                # update mukim_found
                mukim = district_case1[["mukim"]].dropna().drop_duplicates()['mukim'].str.lower().tolist()
                mukim_found = [m for m in mukim if m in str.lower()]

            ##########################################################################################################

                # 4)
                if mukim_found:
                    for mukim in mukim_found:
                        # mukim name is not the same as district name
                        if mukim != district:
                            mukim_update=mukim_update+([mukim])
                            # filter the mukim
                            mukim_case1 = district_case1[district_case1['mukim'].str.lower() == mukim]
                            # update location_found
                            location = mukim_case1[["location"]].dropna().drop_duplicates()['location'].str.lower().tolist()
                            #location_found = [l for l in location if l in str.lower()]
                            location_found = [x for x in [l for l in location if l.lower() in str.lower()] if x in [x.strip() for x in str.lower().strip().split(',')]]
                            # 8) [1248]
                            if location_found:
                                for location in location_found:
                                    if location != mukim_found[0]:
                                        location_update=location_update+([location])
                        # mukim name is the same as district name
                        elif mukim == district:
                            mukim_update=mukim_update+([mukim])
                            # filter the mukim
                            mukim_case2 = district_case1[district_case1['mukim'].str.lower() == mukim]
                            # update location_found
                            # 8) [1248]
                            location = mukim_case2[["location"]].dropna().drop_duplicates()['location'].str.lower().tolist()
                            #location_found = [l for l in location if l in str.lower()]
                            location_found = [x for x in [l for l in location if l.lower() in str.lower()] if x in [x.strip() for x in str.lower().strip().split(',')]]
                            location_update=location_update+([location])

            ##########################################################################################################

                # 5)    
                elif not mukim_found:                  
                    # update location_found
                    location = district_case1[["location"]].dropna().drop_duplicates()['location'].str.lower().tolist()
                    #location_found = [l for l in location if l in str.lower()]
                    location_found = [x for x in [l for l in location if l.lower() in str.lower()] if x in [x.strip() for x in str.lower().strip().split(',')]]
                    # 10) [12510]
                    if location_found:
                        for location in location_found:
                            if location != district:
                                location_update=location_update+([location])
            
            ##########################################################################################################
            
            # district name is the same as state name
            # 2b)
            elif district == state_found[0]:
                district_update=district_update+([district])
                # filter the district
                district_case2 = state[state['district'].str.lower() == district]
                # update mukim_found
                mukim = district_case2[["mukim"]].dropna().drop_duplicates()['mukim'].str.lower().tolist()
                mukim_found = [l for l in mukim if l in str.lower()]

            ##########################################################################################################
            
                # 4)
                if mukim_found:
                    for mukim in mukim_found:
                        # mukim name is not the same as district name
                        if mukim != district:
                            mukim_update=mukim_update+([mukim])
                            # filter the mukim
                            mukim_case1 = district_case2[district_case2['mukim'].str.lower() == mukim]
                            # update location_found
                            location = mukim_case1[["location"]].dropna().drop_duplicates()['location'].str.lower().tolist()
                            #location_found = [l for l in location if l in str.lower()]
                            location_found = [x for x in [l for l in location if l.lower() in str.lower()] if x in [x.strip() for x in str.lower().strip().split(',')]]
                            # 8) [1248]
                            if location_found:
                                for location in location_found:
                                    if location != mukim_found[0]:
                                        location_update=location_update+([location])
                        # mukim name is the same as district name
                        elif mukim == district:
                            mukim_update=mukim_update+([mukim])
                            # filter the mukim
                            mukim_case2 = district_case2[district_case2['mukim'].str.lower() == mukim]
                            # update location_found
                            # 8) [1248]
                            location = mukim_case2[["location"]].dropna().drop_duplicates()['location'].str.lower().tolist()
                            #location_found = [l for l in location if l in str.lower()]
                            location_found = [x for x in [l for l in location if l.lower() in str.lower()] if x in [x.strip() for x in str.lower().strip().split(',')]]
                            location_update=location_update+([location])

            ##########################################################################################################

                # 5)    
                elif not mukim_found:                 
                    # update location_found
                    location = district_case2[["location"]].dropna().drop_duplicates()['location'].str.lower().tolist()
                    #location_found = [l for l in location if l in str.lower()]
                    location_found = [x for x in [l for l in location if l.lower() in str.lower()] if x in [x.strip() for x in str.lower().strip().split(',')]]
                    # 10) [12510]
                    if location_found:
                        for location in location_found:
                            if location != district:
                                location_update=location_update+([location])

# level 1,3,4
state = pd.read_csv("malaysia-postcodes-location-mukim-district-state.csv")[["state"]].drop_duplicates()['state'].str.lower().tolist()
district = pd.read_csv("malaysia-postcodes-location-mukim-district-state.csv")[["district"]].drop_duplicates()['district'].str.lower().tolist()
mukim = pd.read_csv("malaysia-postcodes-location-mukim-district-state.csv")[["mukim"]].dropna().drop_duplicates()['mukim'].str.lower().tolist()
location = pd.read_csv("malaysia-postcodes-location-mukim-district-state.csv")[["location"]].dropna().drop_duplicates()['location'].str.lower().tolist()

# find the state, district, mukim and location in the string
state_found = [s for s in state if s in str.lower()] # case len = 1 , case len = 0 , case len > 1
district_found = [d for d in district if d in str.lower()]
mukim_found = [m for m in mukim if m.lower() in str.lower()]
location_found = [l for l in location if l in str.lower()]  # Convert float to string

# 1)
if len(state_found) == 1:                                                                                                                 

    state_update=state_update+(state_found)

    state = pd.read_csv("malaysia-postcodes-location-mukim-district-state.csv")
    
    #filter state_found
    state = state[state['state'].str.lower() == state_found[0]]

    #update mukim_found
    mukim = state[["mukim"]].dropna().drop_duplicates()['mukim'].str.lower().tolist()
    mukim_found = [x for x in [m for m in mukim if m.lower() in str.lower()] if x in [x.strip() for x in str.lower().strip().split(',')]]

    ####################################################################################################################

    # 4)
    if mukim_found:
        for mukim in mukim_found:
            # mukim name is not the same as district name
            if mukim != state_found[0]:
                mukim_update=mukim_update+([mukim])
                # filter the mukim
                mukim_case1 = state[state['mukim'].str.lower() == mukim]
                # update location_found
                location = mukim_case1[["location"]].dropna().drop_duplicates()['location'].str.lower().tolist()
                #location_found = [l for l in location if l in str.lower()]
                location_found = [x for x in [l for l in location if l.lower() in str.lower()] if x in [x.strip() for x in str.lower().strip().split(',')]]
                # 8) [148]
                if location_found:
                    for location in location_found:
                        if location != mukim_found[0]:
                            location_update=location_update+([location])
            # mukim name is the same as district name
            elif mukim == state_found[0]:
                mukim_update=mukim_update+([mukim])
                # filter the mukim
                mukim_case2 = state[state['mukim'].str.lower() == mukim]
                # update location_found
                # 8) [148]
                location = mukim_case2[["location"]].dropna().drop_duplicates()['location'].str.lower().tolist()
                #location_found = [l for l in location if l in str.lower()]

                location_found = [x for x in [l for l in location if l.lower() in str.lower()] if x in [x.strip() for x in str.lower().strip().split(',')]]

                location_update=location_update+([location])

##########################################################################################################

    # 5)    
    elif not mukim_found:                 
        # update location_found
        location = state[["location"]].dropna().drop_duplicates()['location'].str.lower().tolist()
        #location_found = [l for l in location if l in str.lower()]
        location_found = [x for x in [l for l in location if l.lower() in str.lower()] if x in [x.strip() for x in str.lower().strip().split(',')]]
        # 10) [12510]
        if location_found:
            for location in location_found:
                if location != state_found[0]:
                    location_update=location_update+([location])

##########################################################################################################

# level 1,4
state = pd.read_csv("malaysia-postcodes-location-mukim-district-state.csv")[["state"]].drop_duplicates()['state'].str.lower().tolist()
district = pd.read_csv("malaysia-postcodes-location-mukim-district-state.csv")[["district"]].drop_duplicates()['district'].str.lower().tolist()
mukim = pd.read_csv("malaysia-postcodes-location-mukim-district-state.csv")[["mukim"]].dropna().drop_duplicates()['mukim'].str.lower().tolist()
location = pd.read_csv("malaysia-postcodes-location-mukim-district-state.csv")[["location"]].dropna().drop_duplicates()['location'].str.lower().tolist()

# find the state, district, mukim and location in the string
state_found = [s for s in state if s in str.lower()] # case len = 1 , case len = 0 , case len > 1
district_found = [d for d in district if d in str.lower()]
mukim_found = [m for m in mukim if m.lower() in str.lower()]
location_found = [l for l in location if l in str.lower()]  # Convert float to string

# 1)
if len(state_found) == 1:                                                                                                                 
    state_update=state_update+(state_found)
    state = pd.read_csv("malaysia-postcodes-location-mukim-district-state.csv")
    #filter state_found
    state = state[state['state'].str.lower() == state_found[0]]

    ####################################################################################################################

    #location_found = [l for l in location if l in str.lower()]
    location_found = [x for x in [l for l in location if l.lower() in str.lower()] if x in [x.strip() for x in str.lower().strip().split(',')]]
    # 8) [18]
    if location_found:
        for location in location_found:
            if location != state_found[0]:
                location_update=location_update+([location])

    ##########################################################################################################
            
state_update = list(set(state_update))
district_update = list(set(district_update))
mukim_update = list(set(mukim_update))
location_update = list(set(location_update))

print()
print("state_update:", state_update)
print("district_update:", district_update)
print("mukim_update:", mukim_update)
print("location_update:", location_update)