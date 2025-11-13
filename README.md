# Illustrated Interspeech 2025

An interactive, visual exploration tool for navigating all papers presented at Interspeech 2025.

## Overview

**Illustrated Interspeech 2025** provides an intuitive, map-based interface to explore the latest research in speech and language processing. Browse through hundreds of papers organized by topic, with AI-generated summaries to help you quickly understand key contributions.

## Features

### 🗺️ Interactive 2D Map
- **Visual clustering**: Papers are spatially organized by topic and theme
- **Zoom & pan**: Navigate smoothly through the research landscape
- **Hover interactions**: Quick preview of paper details
- **Click for details**: Deep dive into individual papers

### 📄 Rich Paper Information
Each paper displays:
- Title, authors, and abstract
- **LLM-generated insights**:
  - Short summary
  - ELI5 (Explain Like I'm 5) explanation
  - Problem statement
  - Method overview
  - "Why it matters" context

### 🌳 Topic Tree Browser
Navigate papers through a hierarchical topic structure mirroring Interspeech sessions:
- **Core Areas**: ASR, TTS, Speaker Recognition, etc.
- **Specialized Topics**: Low-resource ASR, Articulatory & Vocal Tract Modelling
- **Challenges**: URGENT, ML-SUPERB, and other shared tasks
- Based on the official [ISCA Archive](https://www.isca-archive.org/) structure

## Inspiration & Acknowledgments

This project is built upon and inspired by Jay Alammar's excellent work:
- [The Illustrated NeurIPS 2025 Map](https://jalammar.github.io/assets/neurips_2025.html)
- [Newsletter: The Illustrated NeurIPS 2025](https://newsletter.languagemodels.co/p/the-illustrated-neurips-2025-a-visual)

We've adapted this approach specifically for the speech and audio processing community, with a focus on the unique taxonomy and challenges in speech research.

## Project Structure

```
Interspeech2025/
├── src/                      # Source code
│   ├── data_processing/      # Scripts for paper data extraction & processing
│   ├── models/               # Embedding models for paper clustering
│   ├── experiments/          # LLM prompt engineering & summary generation
│   └── utils/                # Helper functions
├── data/                     # Raw and processed paper data
├── results/                  # Generated embeddings, clusters, summaries
├── notebooks/                # Exploratory analysis and visualization
└── requirements.txt          # Python dependencies
```

## Getting Started

### Prerequisites
- Python 3.8+
- Node.js (for frontend, if applicable)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Interspeech2025.git
cd Interspeech2025
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run data processing:
```bash
python src/data_processing/preprocess.py
```

## Roadmap

- [ ] Scrape all Interspeech 2025 papers from ISCA Archive
- [ ] Generate paper embeddings for 2D visualization
- [ ] Cluster papers by topic
- [ ] Generate LLM summaries for each paper
- [ ] Build interactive web interface
- [ ] Implement topic tree navigation
- [ ] Deploy public demo

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see LICENSE file for details

## Contact

For questions or feedback, please open an issue on GitHub.

---

*Made with ❤️ for the speech research community* Project

## Overview
Interspeech2025 is a project aimed at developing and evaluating machine learning models for speech processing tasks. The project includes data preprocessing, model training, and exploratory data analysis.

## Project Structure
```
Interspeech2025
├── src
│   ├── data_processing
│   │   └── preprocess.py
│   ├── models
│   │   └── model.py
│   ├── experiments
│   │   └── train.py
│   └── utils
│       └── helpers.py
├── data
│   └── .gitkeep
├── results
│   └── .gitkeep
├── notebooks
│   └── exploratory.ipynb
├── requirements.txt
└── README.md
```

## Installation
To set up the project, clone the repository and install the required dependencies:

```bash
git clone <repository-url>
cd Interspeech2025
pip install -r requirements.txt
```

## Usage
1. **Data Preprocessing**: Use the `preprocess.py` script to load and preprocess your datasets.
2. **Model Training**: Run the `train.py` script to train your models using the preprocessed data.
3. **Exploratory Analysis**: Open the `exploratory.ipynb` notebook for data exploration and visualization.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or features.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.