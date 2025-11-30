import os
import requests
from bs4 import BeautifulSoup
from ddgs import DDGS
from logger import logger

def search_web(query: str, num_results: int = 10) -> str:
    logger.info(f"[SEARCH] {query}")
    results = []
    try:
        with DDGS() as ddgs:
            search_results = list(ddgs.text(query, max_results=num_results))
            
            for i, r in enumerate(search_results, 1):
                results.append(f"{i}. {r.get('title')}\n   URL: {r.get('href')}\n   {r.get('body')}\n")
                 
    except Exception as e:
        logger.error(f"Search error: {e}")
        return f"Error: {e}"
    
    if not results:
        logger.warning("No results.")
        return "No results found."
    
    return "\n".join(results)

def browse_website(url: str) -> str:
    logger.info(f"[BROWSE] {url}")
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        for script in soup(["script", "style", "nav", "footer"]):
            script.decompose()
            
        text = soup.get_text()
        
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        if len(text) > 8000:
            text = text[:8000] + "\n\n[Truncated...]"
            
        return text
        
    except Exception as e:
        logger.error(f"Browse error: {e}")
        return f"Error: {e}"

def save_results(filename: str, content: str) -> str:
    logger.info(f"[SAVE] {filename}")
    try:
        data_dir = os.path.join(os.path.dirname(__file__), "data")
        os.makedirs(data_dir, exist_ok=True)
        
        filepath = os.path.join(data_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
            
        return f"Saved to {filepath}"
    except Exception as e:
        logger.error(f"Save error: {e}")
        return f"Error: {e}"

def draft_application(opportunity_url: str, opportunity_name: str, dancer_name: str, dancer_background: str) -> str:
    logger.info(f"[APP] Drafting for {dancer_name} -> {opportunity_name}")
    
    return f"""
APPLICATION DRAFT
-----------------
To: {opportunity_name}
URL: {opportunity_url}
From: {dancer_name}

Dear Selection Committee,

I am writing to express my strong interest in performing at {opportunity_name}. 

About the Artist:
{dancer_background}

I believe this would be an excellent opportunity to showcase classical Indian dance and would be honored to be considered for this performance.

I look forward to your positive response.

Sincerely,
{dancer_name}

"""
