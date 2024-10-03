import requests
from bs4 import BeautifulSoup

# Define the URLs
urls = [
    "https://slcl.overdrive.com/search",
    "https://mlcstl.overdrive.com/search",
    "https://stcharles.overdrive.com/search"
]

# Load queries from the file using UTF-8 encoding to avoid decoding errors
with open('to-read.txt', 'r', encoding='utf-8') as f:
    queries = f.readlines()

# Function to perform a GET request and check for positive result
def search_overdrive(url, query):
    try:
        # Send GET request with the query
        response = requests.get(url, params={'q': query.strip()})
        
        if response.status_code == 200:
            # Parse the HTML response
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Check if "search results" is present in the title element
            if soup.title and 'search results' in soup.title.text.lower():
                return True
        return False
    except Exception as e:
        print(f"Error searching {url} with query '{query}': {e}")
        return False

# File to store positive results
output_file = 'positive_results.txt'

with open(output_file, 'w', encoding='utf-8') as output:
    # Loop over each query and each URL
    for query in queries:
        for url in urls:
            if search_overdrive(url, query):
                # Write the positive result to the file
                output.write(f"Query: {query.strip()} | URL: {url}\n")

print("Search completed. Positive results saved.")
