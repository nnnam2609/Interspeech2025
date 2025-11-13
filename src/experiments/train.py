import os
import sys
from src.data_processing.preprocess import load_data, clean_data, extract_features
from src.models.model import Model
from src.utils.helpers import log_experiment, save_model

def main():
    # Load and preprocess data
    raw_data = load_data('path/to/dataset')
    cleaned_data = clean_data(raw_data)
    features = extract_features(cleaned_data)

    # Initialize model
    model = Model()

    # Train the model
    model.train(features)

    # Log the experiment
    log_experiment(model)

    # Save the trained model
    save_model(model, 'path/to/save/model')

if __name__ == "__main__":
    main()