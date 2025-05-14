# %%
import pickle
from torch.utils.data import TensorDataset, DataLoader

from transformers import GPT2Tokenizer
import torch



def merge_datasets(path1: str = './dataset/creepypastastories/web_text.pkl', 
                   path2: str = './dataset/reddit/reddit_dataset.pkl') -> list:
    """
    Merges two datasets by concatenating their contents.
    """
    with open(path1, 'rb') as f:
        dataset1 = pickle.load(f)
    with open(path2, 'rb') as f:
        dataset2 = pickle.load(f)

    merged_dataset = dataset1 + dataset2

    return merged_dataset

# %%
def split_dataset(dataset: list, train_ratio: float = 0.8, test_ratio:float = 0.1) -> tuple:
    """
    Splits the dataset into training, validation, and test sets.
    """
    import random
    if train_ratio + test_ratio >= 1.0:
        raise ValueError("train_ratio and test_ratio must sum to less than 1.0")

    random.shuffle(dataset)
    
    train_index = int(len(dataset) * train_ratio)
    test_index = int(len(dataset) * (train_ratio + test_ratio))

    train_set = dataset[:train_index]
    test_set = dataset[train_index:test_index]
    val_set = dataset[test_index:]

    return train_set, val_set, test_set

# %%
def chunk_dataset(dataset: list, tokenizer, chunk_size: int = 512) -> list:
    """
    Chunks the dataset into smaller pieces of specified size.
    """
    tokenized_dataset = []
    for text in dataset:
        tokens = tokenizer.encode(text)
        for i in range(0, len(tokens), chunk_size):
            tokenized_dataset.append(tokens[i:i + chunk_size])

    # Padding 
    for i, data in enumerate(tokenized_dataset):
        if len(data) < chunk_size:
            tokenized_dataset[i] = data + [tokenizer.pad_token_id] * (chunk_size - len(data))
        else:
            tokenized_dataset[i] = data[:chunk_size]
    return tokenized_dataset


# %%
def create_loader(dataset: list, batch_size = 2, saving_path = None) -> DataLoader:
    tensor = torch.tensor(dataset)
    tensor_dataset = TensorDataset(tensor)

    if saving_path is not None:
        with open(saving_path, 'wb') as f:
            pickle.dump(tensor_dataset, f)
            
    return DataLoader(tensor_dataset, batch_size=batch_size, shuffle=True)


def main():
    tokenizer = GPT2Tokenizer.from_pretrained("EleutherAI/gpt-neo-1.3B")
    tokenizer.pad_token = tokenizer.eos_token

    print("Loading datasets...")
    dataset = merge_datasets()
    print("Splitting datasets...")
    train_set, val_set, test_set = split_dataset(dataset)

    print("Tokenizing datasets...")
    tokenized_train_set = chunk_dataset(train_set, tokenizer, chunk_size=2048)
    tokenized_val_set = chunk_dataset(val_set, tokenizer, chunk_size=2048)
    tokenized_test_set = chunk_dataset(test_set, tokenizer, chunk_size=2048)

    print("Creating loaders...")
    create_loader(tokenized_train_set, batch_size=2, saving_path='./dataset/input/train_loader.pkl')
    create_loader(tokenized_val_set, batch_size=2, saving_path='./dataset/input/val_loader.pkl')
    create_loader(tokenized_test_set, batch_size=2, saving_path='./dataset/input/test_loader.pkl')


if __name__ == "__main__":
    main()



