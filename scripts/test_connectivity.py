"""
Test script to verify ISCA Archive connectivity and HTML structure.
"""

import requests
from bs4 import BeautifulSoup

def test_connectivity():
    """Test if we can connect to ISCA Archive."""
    url = "https://www.isca-archive.org/interspeech_2025/"
    
    print("Testing connectivity to ISCA Archive...")
    print(f"URL: {url}\n")
    
    try:
        response = requests.get(url, timeout=10)
        print(f"✓ Status Code: {response.status_code}")
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'lxml')
            
            # Print page title
            title = soup.find('title')
            if title:
                print(f"✓ Page Title: {title.get_text(strip=True)}")
            
            # Look for common elements
            print("\n--- Exploring page structure ---")
            
            # Check for headers
            headers = soup.find_all(['h1', 'h2', 'h3'])[:5]
            print(f"✓ Found {len(soup.find_all(['h1', 'h2', 'h3']))} headers")
            if headers:
                print("  First few headers:")
                for h in headers:
                    print(f"    - {h.name}: {h.get_text(strip=True)[:80]}")
            
            # Check for links
            links = soup.find_all('a', href=True)
            print(f"\n✓ Found {len(links)} links")
            
            # Find paper links
            paper_links = [l for l in links if '/interspeech_2025/' in l.get('href', '')]
            print(f"✓ Found {len(paper_links)} potential paper links")
            
            if paper_links:
                print("  Sample paper links:")
                for link in paper_links[:3]:
                    print(f"    - {link.get_text(strip=True)[:60]}")
                    print(f"      URL: {link.get('href')}")
            
            print("\n✓ Connection test passed!")
            print("The scraper should be able to access the data.")
            
        else:
            print(f"✗ Unexpected status code: {response.status_code}")
            
    except requests.RequestException as e:
        print(f"✗ Connection failed: {e}")
        print("\nPossible issues:")
        print("  - Network connectivity problem")
        print("  - ISCA Archive may be down")
        print("  - URL may have changed")

if __name__ == "__main__":
    test_connectivity()
