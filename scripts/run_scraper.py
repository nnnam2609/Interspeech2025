#!/usr/bin/env python3
"""
Quick script to run the ISCA Archive scraper.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.data_processing.scraper import ISCAArchiveScraper

if __name__ == "__main__":
    print("=" * 60)
    print("Interspeech 2025 Paper Scraper")
    print("=" * 60)
    print()
    
    scraper = ISCAArchiveScraper(output_dir="data/raw")
    
    print("Starting scrape...")
    papers = scraper.scrape_all()
    
    if papers:
        print(f"\n✓ Successfully scraped {len(papers)} papers!")
        scraper.save_to_jsonl(papers)
        scraper.save_to_json(papers)
        print("\n✓ Data saved to data/raw/")
    else:
        print("\n✗ Failed to scrape papers. Check the logs above.")
        sys.exit(1)
