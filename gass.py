import requests
from bs4 import BeautifulSoup

def fetch_links(query, page_number):
    url = 'https://searx.baczek.me/search'
    data = {
        'q': query,
        'category_general': '1',
        'pageno': str(page_number),
        'language': 'auto',
        'time_range': '',
        'safesearch': '0',
        'theme': 'simple'
    }

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'null',
        'priority': 'u=0, i',
        'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
    }

    response = requests.post(url, data=data, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Menyimpan link ke file
        with open('link.txt', 'a') as file:
            for a_tag in soup.find_all('a', href=True):
                href = a_tag['href']
                file.write(href + '\n')
    else:
        print(f"Request failed with status code {response.status_code}")

def main():
    # Membaca nilai q dari file key.txt
    with open('key.txt', 'r') as file:
        queries = file.readlines()
    
    queries = [query.strip() for query in queries]
    
    # Looping untuk setiap query dan setiap halaman
    for query in queries:
        for page in range(1, 11):
            print(f"Fetching links for query: '{query}' on page: {page}")
            fetch_links(query, page)

if __name__ == "__main__":
    main()
