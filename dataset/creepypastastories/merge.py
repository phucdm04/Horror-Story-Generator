import os
import pandas as pd

def merge():
    files = os.listdir('./dataset/creepypastastories/')
    json_files = [file for file in files if file.endswith('.json')]
    merged_df = pd.DataFrame()

    for json_file in json_files:
        # Read the JSON file
        df = pd.read_json(f'./dataset/creepypastastories/{json_file}')

        merged_df = pd.concat([merged_df, df], ignore_index=True)
        print(f"File {json_file} merged successfully.")
    # Remove duplicates based on the 'titles' column
    merged_df = merged_df.drop_duplicates(subset=['titles'])
    # Save the merged DataFrame to a new JSON file
    merged_df.to_json('./dataset/creepypastastories/web_dataset.json', force_ascii=False, orient='records')


if __name__ == "__main__":
    merge()
    print("All files merged successfully.")