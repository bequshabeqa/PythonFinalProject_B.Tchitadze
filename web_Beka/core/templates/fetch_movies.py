try:
    import requests  # type: ignore
except Exception:
    # Fallback to urllib if requests is not available (helps linters/tools that can't resolve requests)
    import urllib.request as _urllib

    class _Response:
        def __init__(self, text, status_code):
            self.text = text
            self.status_code = status_code

    def _get(url, headers=None):
        req = _urllib.Request(url, headers=headers or {})
        with _urllib.urlopen(req) as resp:
            body = resp.read().decode('utf-8')
            code = resp.getcode()
        return _Response(body, code)

    requests = type('requests', (), {'get': staticmethod(_get)})()
from bs4 import BeautifulSoup  # type: ignore
from ..models import Movie

def fetch_and_save_movies():
    url = "https://www.imdb.com/chart/top/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        items = soup.select('li.ipc-metadata-list-summary-item')[:50]
        
        for item in items:
            title = item.select_one('h3.ipc-title__text').text.split('. ', 1)[-1]
            rate = item.select_one('span.ipc-rating-star--rating').text
            
            # თუ ფილმი ბაზაში არ არის, ვქმნით მას
            Movie.objects.get_or_create(title=title, defaults={'rate': float(rate)})
        print("50 ფილმი წარმატებით დაემატა!")
    else:
        print("შეცდომა IMDb-სთან დაკავშირებისას.")


# ფაილის ბოლოს დაამატე ეს:
if __name__ == "__main__":
    fetch_and_save_movies()