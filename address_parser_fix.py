import pandas as pd
import warnings
warnings.filterwarnings('ignore', category=pd.errors.DtypeWarning)

def extract_address_metadata(address_str):
    """
    Extract state, district, mukim, and location from an address string.
    
    Args:
        address_str (str): The address string to parse
        
    Returns:
        tuple: (state_update, district_update, mukim_update, location_update)
    """
    address_lower = address_str.lower()
    
    # Initialize lists
    state_update = []
    district_update = []
    mukim_update = []
    location_update = []
    
    # Read data from CSV
    df = pd.read_csv("malaysia-postcodes-location-mukim-district-state.csv")
    
    # Extract unique values and convert to lowercase strings
    state = df[["state"]].drop_duplicates()['state'].str.lower().tolist()
    district = df[["district"]].drop_duplicates()['district'].str.lower().tolist()
    mukim = df[["mukim"]].dropna().drop_duplicates()['mukim'].str.lower().tolist()
    location = df[["location"]].dropna().drop_duplicates()['location'].str.lower().tolist()
    postcode = df[["postcode"]].drop_duplicates()['postcode'].astype(str).tolist()  # Convert to string
    
    # Find matches in the address string
    state_found = [s for s in state if s in address_lower]
    district_found = [d for d in district if d in address_lower]
    mukim_found = [m for m in mukim if m in address_lower]
    location_found = [l for l in location if l in address_lower]
    postcode_found = [p for p in postcode if p in address_lower]
    
    # Process state matches
    if len(state_found) == 1:
        state_update = state_found
        
        # Filter data for the found state
        state_data = df[df['state'].str.lower() == state_found[0]]
        
        # Update district_found based on filtered state data
        district = state_data[["district"]].drop_duplicates()['district'].str.lower().tolist()
        district_found = [d for d in district if d in address_lower]
        
        # Process district matches
        if district_found:
            for district_name in district_found:
                district_update.append(district_name)
                
                # Filter data for the found district
                district_data = state_data[state_data['district'].str.lower() == district_name]
                
                # Update mukim_found based on filtered district data
                mukim = district_data[["mukim"]].dropna().drop_duplicates()['mukim'].str.lower().tolist()
                mukim_found = [m for m in mukim if m in address_lower]
                
                # Process mukim matches
                if mukim_found:
                    for mukim_name in mukim_found:
                        mukim_update.append(mukim_name)
                        
                        # Filter data for the found mukim
                        mukim_data = district_data[district_data['mukim'].str.lower() == mukim_name]
                        
                        # Update location_found based on filtered mukim data
                        location = mukim_data[["location"]].dropna().drop_duplicates()['location'].str.lower().tolist()
                        location_found = [l for l in location if l in address_lower]
                        
                        # Process location matches
                        if location_found:
                            for location_name in location_found:
                                location_update.append(location_name)
                else:
                    # If no mukim found, look for locations directly in the district
                    location = district_data[["location"]].dropna().drop_duplicates()['location'].str.lower().tolist()
                    location_found = [l for l in location if l in address_lower]
                    
                    # Process location matches
                    if location_found:
                        for location_name in location_found:
                            location_update.append(location_name)
        else:
            # If no district found, look for mukims directly in the state
            mukim = state_data[["mukim"]].dropna().drop_duplicates()['mukim'].str.lower().tolist()
            mukim_found = [m for m in mukim if m in address_lower]
            
            # Process mukim matches
            if mukim_found:
                for mukim_name in mukim_found:
                    mukim_update.append(mukim_name)
                    
                    # Filter data for the found mukim
                    mukim_data = state_data[state_data['mukim'].str.lower() == mukim_name]
                    
                    # Update location_found based on filtered mukim data
                    location = mukim_data[["location"]].dropna().drop_duplicates()['location'].str.lower().tolist()
                    location_found = [l for l in location if l in address_lower]
                    
                    # Process location matches
                    if location_found:
                        for location_name in location_found:
                            location_update.append(location_name)
            else:
                # If no mukim found, look for locations directly in the state
                location = state_data[["location"]].dropna().drop_duplicates()['location'].str.lower().tolist()
                location_found = [l for l in location if l in address_lower]
                
                # Process location matches
                if location_found:
                    for location_name in location_found:
                        location_update.append(location_name)
    
    # Remove duplicates
    state_update = list(set(state_update))
    district_update = list(set(district_update))
    mukim_update = list(set(mukim_update))
    location_update = list(set(location_update))
    
    return (state_update, district_update, mukim_update, location_update)

# Example usage
if __name__ == "__main__":
    address = "235, pintasan mayang 1, persiaran mayang pasir, 11900, mukim 12, pulau pinang"
    result = extract_address_metadata(address)
    print("State:", result[0])
    print("District:", result[1])
    print("Mukim:", result[2])
    print("Location:", result[3])