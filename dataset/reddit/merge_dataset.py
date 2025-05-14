import pandas as pd
import os

def clean_subreddit(path, subreddit):
    """
    Read dataset from path, filter by flair, drop duplicates, and return a cleaned DataFrame.
    Args:
        path (str): Path to the dataset file.
        subreddit (str): Subreddit name to filter by.
    """
    df = pd.read_json(path)
    if df.shape[0] < df.shape[1]: # transpose if more columns than rows
        df = df.T
    
    remained_flair = "all"
    dropped_flair = "none"
    if subreddit == "creepypasta":
        remained_flair = ['Creepypasta', 'Text Story', 'Very Short Story']
    elif subreddit == "nosleep":
        dropped_flair = ["Series"]
    elif subreddit == "Creepypastastories":
        remained_flair = ['Story']
    elif subreddit == "Horror_stories":
        return df
    elif subreddit == "RedditHorrorStories":
        remained_flair = ['True Horror Story', 'Story (True)', 'Story (Fiction)', 'Fictional Horror Story']

    if remained_flair != "all":
        df = df[df['flair'].isin(remained_flair)]
    if dropped_flair != "none":
        df = df[~df['flair'].isin(dropped_flair)]

    df = df.dropna(subset=['flair'], how='all')
    df = df.drop_duplicates(subset=['title', 'selftext'], keep='first')
    return df

def merge_datasets(input_path, output_path):
    """
    Merge all datasets in the input_path and save to output_path.
    """
    # List of subreddits to merge
    subreddits = ["creepypasta", "nosleep", "Creepypastastories", "Horror_stories", "RedditHorrorStories"]
    
    # Initialize an empty DataFrame to hold the merged data
    merged_df = pd.DataFrame()

    # Loop through each subreddit and filter the dataset
    for subreddit in subreddits:
        files = os.listdir(input_path)
        files = [f for f in files if f.startswith(subreddit) and f.endswith('.json')]
        for file in files:
            try:
                file_path = os.path.join(input_path, file)                    
                df = clean_subreddit(file_path, subreddit)
                df['subreddit'] = subreddit

                # Append the filtered DataFrame to the merged DataFrame
                merged_df = pd.concat([merged_df, df], ignore_index=True)
                print(f"Completed merging {file}.")
            except Exception as e:
                print(f"Error processing file {file}: {e}")
    # Reset the index of the merged DataFrame
    merged_df.reset_index(drop=True, inplace=True)
    # Drop duplicates based on 'title' and 'selftext'
    merged_df = merged_df.drop_duplicates(subset=['title', 'selftext'], keep='first')
    print(merged_df.shape)
    # Save the merged DataFrame to a CSV file
    merged_df.T.to_parquet(output_path, index=False, engine='pyarrow')

if __name__ == "__main__":
    input_path = "./dataset/reddit/data_from_subreddit/"
    output_path = "./dataset/reddit/reddit_dataset.parquet"
    merge_datasets(input_path, output_path)
    print(f"Merged dataset saved to {output_path}")