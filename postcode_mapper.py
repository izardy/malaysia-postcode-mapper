import pandas as pd
import numpy as np

def process_postcode_data(input_data):
    """
    Process raw postcode data and convert it to a structured DataFrame
    
    Args:
        input_data (str): Raw postcode data in string format
        
    Returns:
        pd.DataFrame: Processed DataFrame with postcode, location, district, state, mukim
    """
    # Parse the input data
    rows = []
    lines = input_data.strip().split('\n')
    
    # Skip header line
    for line in lines[1:]:
        parts = line.split('\t')
        if len(parts) >= 5:
            postcode = parts[0]
            location = parts[1] if parts[1] != 'NaN' else None
            district = parts[2] if parts[2] != 'NaN' else None
            state = parts[3] if parts[3] != 'NaN' else None
            mukim = parts[4] if parts[4] != 'NaN' else None
            
            rows.append({
                'postcode': postcode,
                'location': location,
                'district': district,
                'state': state,
                'mukim': mukim
            })
    
    # Create DataFrame
    df = pd.DataFrame(rows)
    return df

def main():
    # Example usage with the data provided
    raw_data = """postcode	location	district	state	mukim
57863	NaN	NaN	MERSING	JOHOR	JEMALUANG
57864	NaN	NaN	MERSING	JOHOR	LENGGOR
57865	NaN	NaN	MERSING	JOHOR	MERSING
57866	NaN	NaN	MERSING	JOHOR	PADANG ENDAU
57867	NaN	NaN	MERSING	JOHOR	PENYABONG
57868	NaN	NaN	MERSING	JOHOR	PULAU AUR
57869	NaN	NaN	MERSING	JOHOR	PULAU BABI
57870	NaN	NaN	MERSING	JOHOR	PULAU PEMANGGIL
57871	NaN	NaN	MERSING	JOHOR	PULAU SIBU
57872	NaN	NaN	MERSING	JOHOR	PULAU TINGGI
57873	NaN	NaN	MERSING	JOHOR	SEMBRONG
57874	NaN	NaN	MERSING	JOHOR	TENGGAROH
57875	NaN	NaN	MERSING	JOHOR	TENGLU
57876	NaN	NaN	MERSING	JOHOR	TRIANG
57877	NaN	NaN	MERSING	JOHOR	BANDAR JEMALUANG
57878	NaN	NaN	MERSING	JOHOR	BANDAR MERSING
57879	NaN	NaN	MERSING	JOHOR	BANDAR MERSING KANAN
57880	NaN	NaN	MERSING	JOHOR	BANDAR PADANG ENDAU"""
    
    # Process the data
    df = process_postcode_data(raw_data)
    
    # Display the processed data
    print(df)
    
    # Save to CSV
    df.to_csv('processed_postcodes.csv', index=False)
    print("Data saved to processed_postcodes.csv")

if __name__ == "__main__":
    main()