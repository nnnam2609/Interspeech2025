"""
Interspeech 2025 ISCA Archive Scraper

This script scrapes paper metadata from the ISCA Archive for Interspeech 2025.
It extracts session information, paper titles, authors, abstracts, and other metadata.
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import re
from pathlib import Path
from typing import Dict, List, Optional
from tqdm import tqdm
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ISCAArchiveScraper:
    """Scraper for ISCA Archive papers."""
    
    BASE_URL = "https://www.isca-archive.org"
    CONFERENCE_URL = f"{BASE_URL}/interspeech_2025/"
    
    def __init__(self, output_dir: str = "data/raw"):
        """
        Initialize the scraper.
        
        Args:
            output_dir: Directory to save scraped data
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
    def fetch_page(self, url: str, retry: int = 3) -> Optional[BeautifulSoup]:
        """
        Fetch and parse a webpage.
        
        Args:
            url: URL to fetch
            retry: Number of retry attempts
            
        Returns:
            BeautifulSoup object or None if failed
        """
        for attempt in range(retry):
            try:
                response = self.session.get(url, timeout=10)
                response.raise_for_status()
                return BeautifulSoup(response.content, 'lxml')
            except requests.RequestException as e:
                logger.warning(f"Attempt {attempt + 1}/{retry} failed for {url}: {e}")
                if attempt < retry - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    logger.error(f"Failed to fetch {url} after {retry} attempts")
                    return None
    
    def extract_sessions(self, soup: BeautifulSoup) -> List[Dict]:
        """
        Extract session information from the main conference page.
        
        Args:
            soup: BeautifulSoup object of the main page
            
        Returns:
            List of session dictionaries
        """
        sessions = []
        
        # Find all h4 tags (session headers)
        session_headers = soup.find_all('h4')
        
        logger.info(f"Found {len(session_headers)} session headers")
        
        for idx, h4 in enumerate(session_headers):
            session_name = h4.get_text(strip=True)
            
            # Skip if this doesn't look like a real session
            if not session_name or len(session_name) < 3:
                continue
            
            # Get the parent div which contains all papers for this session
            parent_div = h4.parent
            
            # Find all paper links within this parent div
            # Papers have <a> tags with href ending in .html
            paper_links = []
            for a_tag in parent_div.find_all('a', href=True):
                href = a_tag.get('href')
                # Filter for actual paper links (relative paths ending in _interspeech.html)
                if href.endswith('.html') and '_interspeech.html' in href:
                    # Construct full URL
                    paper_url = f"{self.CONFERENCE_URL}{href}"
                    paper_title = a_tag.get_text(strip=True)
                    
                    # Filter out the session title itself and very short titles
                    if paper_title and len(paper_title) > 10 and paper_title != session_name:
                        paper_links.append({
                            'title': paper_title,
                            'url': paper_url
                        })
            
            if paper_links:
                sessions.append({
                    'session_id': len(sessions),  # Use actual count for ID
                    'session_name': session_name,
                    'papers': paper_links
                })
                logger.info(f"Session '{session_name}': {len(paper_links)} papers")
        
        logger.info(f"Found {len(sessions)} sessions with papers")
        return sessions
    
    def extract_paper_metadata(self, url: str, session_info: Dict) -> Optional[Dict]:
        """
        Extract metadata from a paper page.
        
        Args:
            url: URL of the paper page
            session_info: Information about the session
            
        Returns:
            Dictionary with paper metadata or None if failed
        """
        soup = self.fetch_page(url)
        if not soup:
            return None
        
        metadata = {
            'url': url,
            'session_id': session_info.get('session_id'),
            'session_name': session_info.get('session_name')
        }
        
        # Extract paper ID from URL
        match = re.search(r'/interspeech_2025/(.+?)\.html', url)
        if match:
            metadata['paper_id'] = match.group(1)
        
        # Extract title
        title_tag = soup.find(['h1', 'h2'], class_=re.compile(r'title|paper'))
        if not title_tag:
            title_tag = soup.find('h1')
        if title_tag:
            metadata['title'] = title_tag.get_text(strip=True)
        
        # Extract authors
        authors_section = soup.find(['div', 'p'], class_=re.compile(r'author'))
        if authors_section:
            # Try to extract individual author names
            author_tags = authors_section.find_all(['span', 'a'])
            if author_tags:
                metadata['authors'] = [tag.get_text(strip=True) for tag in author_tags]
            else:
                metadata['authors'] = [authors_section.get_text(strip=True)]
        
        # Extract abstract
        abstract_section = soup.find(['div', 'p'], class_=re.compile(r'abstract'))
        if not abstract_section:
            # Look for a section with id or text containing "abstract"
            abstract_section = soup.find(string=re.compile(r'Abstract', re.I))
            if abstract_section:
                abstract_section = abstract_section.find_next(['div', 'p'])
        
        if abstract_section:
            metadata['abstract'] = abstract_section.get_text(strip=True)
        
        # Extract DOI
        doi_link = soup.find('a', href=re.compile(r'doi.org'))
        if doi_link:
            metadata['doi'] = doi_link.get('href')
        
        # Extract page range
        page_info = soup.find(string=re.compile(r'pp\.|pages?', re.I))
        if page_info:
            page_match = re.search(r'(\d+)[-–](\d+)', str(page_info))
            if page_match:
                metadata['page_start'] = int(page_match.group(1))
                metadata['page_end'] = int(page_match.group(2))
        
        # Extract PDF link
        pdf_link = soup.find('a', href=re.compile(r'\.pdf$'))
        if pdf_link:
            pdf_url = pdf_link.get('href')
            if pdf_url and not pdf_url.startswith('http'):
                pdf_url = f"{self.BASE_URL}{pdf_url}"
            metadata['pdf_url'] = pdf_url
        
        return metadata
    
    def scrape_all(self) -> List[Dict]:
        """
        Scrape all papers from Interspeech 2025.
        
        Returns:
            List of paper metadata dictionaries
        """
        logger.info(f"Starting scrape of {self.CONFERENCE_URL}")
        
        # Fetch main conference page
        main_soup = self.fetch_page(self.CONFERENCE_URL)
        if not main_soup:
            logger.error("Failed to fetch main conference page")
            return []
        
        # Extract sessions
        sessions = self.extract_sessions(main_soup)
        logger.info(f"Found {len(sessions)} sessions")
        
        # Extract paper metadata
        all_papers = []
        
        for session in tqdm(sessions, desc="Processing sessions"):
            session_name = session['session_name']
            logger.info(f"Processing session: {session_name}")
            
            for paper_info in tqdm(session['papers'], desc=f"  Papers in {session_name}", leave=False):
                metadata = self.extract_paper_metadata(
                    paper_info['url'],
                    session
                )
                
                if metadata:
                    all_papers.append(metadata)
                
                # Be polite to the server
                time.sleep(0.5)
        
        logger.info(f"Successfully scraped {len(all_papers)} papers")
        return all_papers
    
    def save_to_jsonl(self, papers: List[Dict], filename: str = "interspeech2025_papers.jsonl"):
        """
        Save papers to JSONL format.
        
        Args:
            papers: List of paper dictionaries
            filename: Output filename
        """
        output_path = self.output_dir / filename
        
        with open(output_path, 'w', encoding='utf-8') as f:
            for paper in papers:
                f.write(json.dumps(paper, ensure_ascii=False) + '\n')
        
        logger.info(f"Saved {len(papers)} papers to {output_path}")
    
    def save_to_json(self, papers: List[Dict], filename: str = "interspeech2025_papers.json"):
        """
        Save papers to JSON format.
        
        Args:
            papers: List of paper dictionaries
            filename: Output filename
        """
        output_path = self.output_dir / filename
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(papers, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved {len(papers)} papers to {output_path}")


def main():
    """Main execution function."""
    scraper = ISCAArchiveScraper(output_dir="data/raw")
    
    # Scrape all papers
    papers = scraper.scrape_all()
    
    if papers:
        # Save in both formats
        scraper.save_to_jsonl(papers)
        scraper.save_to_json(papers)
        
        # Print summary statistics
        logger.info("\n=== Scraping Summary ===")
        logger.info(f"Total papers scraped: {len(papers)}")
        
        sessions = set(p.get('session_name') for p in papers if p.get('session_name'))
        logger.info(f"Total sessions: {len(sessions)}")
        
        papers_with_abstract = sum(1 for p in papers if p.get('abstract'))
        logger.info(f"Papers with abstract: {papers_with_abstract}")
        
        papers_with_authors = sum(1 for p in papers if p.get('authors'))
        logger.info(f"Papers with authors: {papers_with_authors}")
    else:
        logger.error("No papers were scraped!")


if __name__ == "__main__":
    main()
