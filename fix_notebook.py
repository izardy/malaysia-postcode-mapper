import pandas as pd
import warnings
warnings.filterwarnings('ignore', category=pd.errors.DtypeWarning)

# Read the CSV file
df = pd.read_csv("malaysia-postcodes-location-mukim-district-state.csv")

# Extract unique values and convert to lowercase strings
state = df[["state"]].drop_duplicates()['state'].str.lower().tolist()
district = df[["district"]].drop_duplicates()['district'].str.lower().tolist()
mukim = df[["mukim"]].dropna().drop_duplicates()['mukim'].str.lower().tolist()
location = df[["location"]].dropna().drop_duplicates()['location'].str.lower().tolist()
postcode = df[["postcode"]].drop_duplicates()['postcode'].astype(str).tolist()  # Convert to string

# Define the address string
address_str = "235, pintasan mayang 1, persiaran mayang pasir, 11900, mukim 12, pulau pinang"
address_lower = address_str.lower()

# Find matches in the address string
state_found = [s for s in state if s in address_lower]
district_found = [d for d in district if d in address_lower]
mukim_found = [m for m in mukim if m in address_lower]
location_found = [l for l in location if l in address_lower]
postcode_found = [p for p in postcode if p in address_lower]

print("State found:", state_found)
print("District found:", district_found)
print("Mukim found:", mukim_found)
print("Location found:", location_found)
print("Postcode found:", postcode_found)

# Try with a different address
address_str2 = "235, pintasan mayang 1, persiaran mayang pasir, 11900, bayan lepas, pulau pinang"
address_lower2 = address_str2.lower()

# Find matches in the second address string
state_found2 = [s for s in state if s in address_lower2]
district_found2 = [d for d in district if d in address_lower2]
mukim_found2 = [m for m in mukim if m in address_lower2]
location_found2 = [l for l in location if l in address_lower2]
postcode_found2 = [p for p in postcode if p in address_lower2]

print("\nFor second address:")
print("State found:", state_found2)
print("District found:", district_found2)
print("Mukim found:", mukim_found2)
print("Location found:", location_found2)
print("Postcode found:", postcode_found2)