import pandas as pd
import re
import os

#===============================
# DATA CLEANER & MERGER
# ==============================

RAW_PATH = "data/raw"
OUTPUT_PATH = "data/processed"
os.makedirs(OUTPUT_PATH, exist_ok=True)

# ------------------------------
# Helper functions
# ------------------------------

def clean_country_names(text):
    """Keeps only letters and numbers and makes it lowercase. Turning 'United States[a]' into 'unitedstates' to match country names."""
    if pd.isna(text): return ""
    return re.sub(r'[^a-zA-Z0-9]', '', str(text)).lower()

def clean_numeric(value):
    if pd.isna(value) or str(value).strip() in ['—', '', 'NaN', 'None', '...', 'n/a']:
        return None
    clean_val = re.sub(r'[^\d.]', '', str(value))
    try:
        return float(clean_val)
    except ValueError:
        return None

# ------------------------------
# Finding correct colums
# ------------------------------

def get_best_columns(df):
    """Automatically finds which column is 'Country' and which is 'Data'."""
    country_col = None
    data_col = None
    
    for col in df.columns:
        # Country column
        if df[col].astype(str).str.contains('[a-zA-Z]').mean() > 0.8:
            if country_col is None: country_col = col
        # Data column
        elif df[col].astype(str).str.contains('\d').mean() > 0.3:
            if data_col is None: data_col = col
            
    # Fallback if detection fails
    if country_col is None: country_col = df.columns[0]
    if data_col is None: data_col = df.columns[1]
    return country_col, data_col

def clean_data():
    print("-" * 35)
    print("Running Universal Matcher Engine...")
    print("-" * 35)

    # ------------------------------
    # Load raw datasets
    # ------------------------------

    raw_files = {
        'gdp': 'data/raw/data_raw_gdp.csv',
        'life': 'data/raw/data_raw_life_expectancy.csv',
        'lit': 'data/raw/data_raw_literacy.csv'
    }
    
    processed_dfs = []

    for key, path in raw_files.items():
        df = pd.read_csv(path)
        c_col, d_col = get_best_columns(df)
        
        # Creates clean version of the dataframe
        new_df = pd.DataFrame()
        new_df['Original_Country'] = df[c_col]
        new_df['Match_Key'] = df[c_col].apply(clean_country_names) #Match key for merging
        new_df[key.upper()] = df[d_col].apply(clean_numeric)
        
        # Drop empty rows & 'World' row
        new_df = new_df[new_df['Match_Key'] != 'world']
        new_df = new_df.dropna(subset=[key.upper()])
        processed_dfs.append(new_df)
        print(f"{key.upper()} list processed: {len(new_df)} entries.")

    # ------------------------------
    # Merge datasets
    # ------------------------------

    # Merge using the Match_Key
    print("-" * 30)
    print("Syncing all datasets...")
    master = processed_dfs[0]
    for next_df in processed_dfs[1:]:
        master = pd.merge(master, next_df, on='Match_Key', how='inner')

    # ------------------------------
    # Clean country names
    # ------------------------------
    
    # Keep the original country name, drop the keys and duplicates
    # We'll take the 'Original_Country' from the first file (GDP)
    cols_to_keep = ['Original_Country_x', 'GDP', 'LIFE', 'LIT']
    master = master[cols_to_keep]
    master.columns = ['Country', 'GDP_Per_Capita', 'Life_Expectancy', 'Literacy_Rate']

    # ------------------------------
    # Save Master CSV
    # ------------------------------

    output_path = 'data/processed/master_data.csv' 
    master.to_csv(output_path, index=False)

    # ------------------------------
    # Test if merge is successful
    # ------------------------------

    print("-" * 30)
    print(f"==Successfully Created Master_data.csv==")
    print(f"Total Synchronized Countries: {len(master)}")
    if len(master) > 0:
        print("---Master_data.csv, first 10 entries:---")
        print(master.head(10))
    else:
        print("!!!! No Synchronized Countries Found !!!!" \
              "Literacy table 'Match_Keys' may not overlap with GDP.")

if __name__ == "__main__":
    clean_data()


