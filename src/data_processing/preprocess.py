def load_dataset(file_path):
    """Load dataset from a given file path."""
    import pandas as pd
    return pd.read_csv(file_path)

def clean_data(data):
    """Clean the dataset by handling missing values and duplicates."""
    data = data.dropna()
    data = data.drop_duplicates()
    return data

def extract_features(data):
    """Extract features from the dataset for model training."""
    features = data.drop('target', axis=1)
    target = data['target']
    return features, target

def preprocess_data(file_path):
    """Main function to preprocess the data."""
    data = load_dataset(file_path)
    cleaned_data = clean_data(data)
    features, target = extract_features(cleaned_data)
    return features, target