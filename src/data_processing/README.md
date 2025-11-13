# Data Processing

This directory contains scripts for collecting and processing Interspeech 2025 paper data.

## Scraper

The `scraper.py` module crawls the ISCA Archive to extract paper metadata.

### Features

- Scrapes all Interspeech 2025 papers from https://www.isca-archive.org/interspeech_2025/
- Extracts:
  - Paper ID
  - Title
  - Authors
  - Abstract
  - Session information
  - DOI
  - Page range
  - PDF URL
- Saves data in both JSON and JSONL formats
- Includes retry logic and rate limiting to be respectful to the server

### Usage

```bash
# From project root
python scripts/run_scraper.py
```

Or use the module directly:

```python
from src.data_processing.scraper import ISCAArchiveScraper

scraper = ISCAArchiveScraper(output_dir="data/raw")
papers = scraper.scrape_all()
scraper.save_to_jsonl(papers)
```

### Output

Data is saved to `data/raw/`:
- `interspeech2025_papers.jsonl` - One paper per line (recommended for large datasets)
- `interspeech2025_papers.json` - All papers in a single JSON array

### Data Schema

Each paper object contains:

```json
{
  "paper_id": "nguyen25_interspeech",
  "url": "https://www.isca-archive.org/interspeech_2025/nguyen25_interspeech.html",
  "title": "Example Paper Title",
  "authors": ["Author One", "Author Two"],
  "abstract": "Paper abstract text...",
  "session_id": 0,
  "session_name": "Spoken Machine Translation 1",
  "doi": "https://doi.org/10.21437/...",
  "page_start": 1234,
  "page_end": 1238,
  "pdf_url": "https://www.isca-archive.org/interspeech_2025/nguyen25_interspeech.pdf"
}
```

## Preprocess

The `preprocess.py` module will handle data cleaning and preparation for embedding generation (to be implemented).
