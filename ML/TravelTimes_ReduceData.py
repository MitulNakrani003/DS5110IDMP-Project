import pandas as pd
import glob

# https://mbta-massdot.opendata.arcgis.com/datasets/e48c8cd8cf154d27b23d31777a8f39e9/about

def create_df_for_lines():
    # Step 1: Load all CSV files from the folder
    file_paths = glob.glob('../DATA/TravelTimes2022/*.csv')  # Replace with the correct folder path

    global combined_df, orange_df, red_df, blue_df, green_df
    # Combine all CSV files into one DataFrame
    combined_df = pd.concat([pd.read_csv(file) for file in file_paths], ignore_index=True)

    # Step 2: Create different DataFrames for different lines based on 'route_id'
    # Assuming route_id values are like 'Orange', 'Red', etc.

    # For example, to filter Orange line
    orange_df = combined_df[combined_df['route_id'] == 'Orange']

    # Similarly, create DataFrames for other lines
    red_df = combined_df[combined_df['route_id'] == 'Red']
    blue_df = combined_df[combined_df['route_id'] == 'Blue']
    green_df = combined_df[combined_df['route_id'].str.startswith('Green')]
    

def print_og_df_details():
    print("=== DataFrame Details ===")
    print(f"Combined DataFrame shape: {combined_df.shape}")
    print(f"Combined DataFrame columns: {list(combined_df.columns)}")
    print()

    print(f"Orange DataFrame shape: {orange_df.shape}")
    print(f"Orange DataFrame info:")
    print(orange_df.info())
    print()

    print(f"Red DataFrame shape: {red_df.shape}")
    print(f"Red DataFrame info:")
    print(red_df.info())
    print()

    print(f"Blue DataFrame shape: {blue_df.shape}")
    print(f"Blue DataFrame info:")
    print(blue_df.info())
    print()

    print(f"Green DataFrame shape: {green_df.shape}")
    print(f"Green DataFrame info:")
    print(green_df.info())
    print()


def reduce_df_rows():
    global orange_df_reduced, red_df_reduced, blue_df_reduced, green_df_reduced
    # Step 3: Reduce the rows to make it easier to process by randomly sampling a subset
    # For example, reduce each DataFrame to 10% of the original rows
    orange_df_reduced = orange_df.sample(frac=0.01, random_state=42)
    red_df_reduced = red_df.sample(frac=0.01, random_state=42)
    blue_df_reduced = blue_df.sample(frac=0.01, random_state=42)
    green_df_reduced = green_df.sample(frac=0.01, random_state=42)


def save_reduced_dfs():
    # Step 4: Optionally save the reduced DataFrames to CSV files
    orange_df_reduced.to_csv('../DATA/TravelTimesReduced/orange_reduced.csv', index=False)
    red_df_reduced.to_csv('../DATA/TravelTimesReduced/red_reduced.csv', index=False)
    blue_df_reduced.to_csv('../DATA/TravelTimesReduced/blue_reduced.csv', index=False)
    green_df_reduced.to_csv('../DATA/TravelTimesReduced/green_reduced.csv', index=False)


# create_df_for_lines()  # Load and combine all CSV files
# print_og_df_details()  # Print details of the original DataFrames
# reduce_df_rows()  # Reduce the rows of each DataFrame
# save_reduced_dfs()  # Save the reduced DataFrames to CSV files

