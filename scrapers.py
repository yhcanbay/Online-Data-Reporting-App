import json
import urllib.request
import urllib.error
import time
import urllib.parse

# Kullanıcının belirttiği temel arama kalıpları
SEARCH_PATTERNS = [
    "Is there a tool for",
    "I wish there was an app that",
    "I hate doing this manually",
    "Why is there no good software for",
    "How can I automate",
    "Bunu manuel yapmaktan nefret ediyorum",
    "Neden hala düzgün çalışan bir yazılım yok"
]

def fetch_reddit_posts(subreddit: str, keywords: list = None, limit: int = 5) -> list:
    """Reddit'ten veri çeker. Anahtar kelime ve kalıplara göre arama yapar."""
    posts = []
    
    search_terms = []
    if keywords:
        for kw in keywords:
            for pattern in SEARCH_PATTERNS:
                search_terms.append(f'"{kw}" {pattern}')
    else:
        search_terms = SEARCH_PATTERNS

    # Çok fazla istek atmamak için limitliyoruz
    for term in search_terms[:5]:
        query = urllib.parse.quote(term)
        url = f"https://www.reddit.com/r/{subreddit}/search.json?q={query}&restrict_sr=1&limit={limit}&sort=relevance"
        
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) IdeaGeneratorBot/1.0'}
        )
        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode('utf-8'))
                for item in data.get('data', {}).get('children', []):
                    post_data = item['data']
                    title = post_data.get('title', '')
                    selftext = post_data.get('selftext', '')
                    content = f"{title}\n{selftext}".strip()
                    if content:
                        posts.append({
                            "kaynak": f"Reddit (r/{subreddit})",
                            "icerik": content,
                            "url": f"https://www.reddit.com{post_data.get('permalink', '')}",
                            "arama_terimi": term
                        })
            time.sleep(1) # Rate limit
        except Exception as e:
            print(f"Reddit (r/{subreddit}) '{term}' araması hatası: {e}")
            
    return posts

def fetch_hacker_news(keywords: list = None, limit: int = 15) -> list:
    """Hacker News verilerini çeker ve anahtar kelime/kalıplara göre filtreler."""
    url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    posts = []
    
    check_list = SEARCH_PATTERNS
    if keywords:
        check_list = keywords + SEARCH_PATTERNS

    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            # Daha az hikaye tarayarak hız sorununu çözelim
            max_stories = 100 if keywords else 30
            story_ids = json.loads(response.read().decode('utf-8'))[:max_stories]
            
        for story_id in story_ids:
            if len(posts) >= limit:
                break
                
            story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
            try:
                with urllib.request.urlopen(story_url, timeout=5) as story_response:
                    story = json.loads(story_response.read().decode('utf-8'))
                    if not story: continue
                    title = story.get('title', '')
                    text = story.get('text', '')
                    content = f"{title}\n{text}".strip()
                    
                    if content:
                        if any(p.lower() in content.lower() for p in check_list):
                            posts.append({
                                "kaynak": "Hacker News",
                                "icerik": content,
                                "url": f"https://news.ycombinator.com/item?id={story_id}"
                            })
            except:
                continue
            time.sleep(0.02)
    except Exception as e:
        print(f"Hacker News veri çekme hatası: {e}")
    return posts

def fetch_mock_data(keywords: list = None) -> list:
    """Mock verileri anahtar kelime ve kalıplara göre filtreler."""
    all_mock = [
        {
            "kaynak": "X (Twitter)",
            "icerik": "I wish there was an app that simply organizes my tax receipts by reading emails automatically. I hate doing this manually at the end of every month! #freelanceproblems",
            "url": "https://x.com/sample_user/status/123456"
        },
        {
            "kaynak": "G2 Reviews (QuickBooks)",
            "icerik": "Entegrasyon süreçleri tam bir kabus. Neden hala düzgün çalışan bir yazılım yok? Müşteri hizmetlerine ulaşmak imkansız.",
            "url": "https://www.g2.com/products/quickbooks/reviews"
        },
        {
            "kaynak": "Quora",
            "icerik": "What is the hardest part of being a Dentist? Honestly, managing patient appointments and last-minute cancellations. Is there a tool for this that doesn't cost a fortune?",
            "url": "https://www.quora.com/What-is-the-hardest-part-of-being-a-Dentist"
        },
        {
            "kaynak": "LinkedIn (Supply Chain Group)",
            "icerik": "We are consistently struggling with real-time inventory tracking. How can I automate this process without a $100k budget?",
            "url": "https://www.linkedin.com/groups/12345/sample"
        }
    ]
    
    check_list = SEARCH_PATTERNS
    if keywords:
        check_list = keywords + SEARCH_PATTERNS
        
    return [p for p in all_mock if any(pattern.lower() in p['icerik'].lower() for pattern in check_list)]

def get_all_data(keywords: list = None) -> list:
    """Tüm kaynaklardan verileri toplayıp birleştirir."""
    all_data = []
    
    # Reddit Aramaları
    reddit_subs = ['SaaS', 'Entrepreneur', 'SmallBusiness', 'SideProject']
    for sub in reddit_subs:
        # Bir subredditden en fazla 3 post (kalıplardan bağımsız)
        all_data.extend(fetch_reddit_posts(sub, keywords=keywords, limit=3))
    
    # Hacker News (Limit artırıldı)
    all_data.extend(fetch_hacker_news(keywords=keywords, limit=10 if keywords else 6))
    
    # Mock data
    all_data.extend(fetch_mock_data(keywords=keywords))
    
    # Mükerrer olanları temizle
    unique_data = []
    seen_urls = set()
    for item in all_data:
        if item['url'] not in seen_urls:
            unique_data.append(item)
            seen_urls.add(item['url'])
            
    return unique_data

if __name__ == "__main__":
    import sys
    kws = sys.argv[1:] if len(sys.argv) > 1 else None
    data = get_all_data(keywords=kws)
    print(f"Toplam {len(data)} veri çekildi.")
