#!bin/python3
# Google Search  - 1100 Series

try:
    import requests
    import fake_useragent
    from bs4 import BeautifulSoup

except ModuleNotFoundError:
    print("Modules Not Found")
    exit(0)


class GoogleSearch:
    base_query = "https://www.google.com/search"

    def __init__(self):
        """Initializing All The Parameters for Effective Search"""
        self.query = ""
        google_abuse = """GOOGLE_ABUSE_EXEMPTION % 3
        DID % 3
        D82800e39327b1d52: TM % 3
        D1691600928: C % 3
        Dr: IP % 3
        D103
        .162
        .189
        .227 -: S % 3
        DYEOUU5FEhb6pdjn3GGungR4 % 3
        B + path % 3
        D / % 3
        B + domain % 3
        Dgoogle.com % 3
        B + expires % 3
        DWed, +09 - Aug - 2030 + 20: 0
        8: 48 + GMT"""
        self.parameters = {'q': self.query, 'hl': "en", "ie": "UTF-8", "oq": self.query}
        self.session = requests.session()

    def search(self, query):
        self.query = query
        self.parameters["q"] = self.query
        self.parameters["oq"] = self.query

        response = self.session.get(GoogleSearch.base_query, params=self.parameters)
        with open("w1.html", 'w', encoding="utf-8") as file:
            file.write(response.text)
        print(response.status_code)
        print(response.cookies, response.headers)
        print(response.history)
        print(response.url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find all anchor tags within search results
            search_results = soup.find_all('a')
            f1 = open("urls.txt", 'a', encoding="utf-8")
            urls = []
            for result in search_results:
                # Extract URLs from anchor tags
                link = result.get('href')
                if link and link.startswith('/url?q='):
                    # Extract the actual URL from the query parameter
                    actual_url = link[7:].split('&')[0]
                    actual_url = actual_url.replace("%3F", "?")
                    actual_url = actual_url.replace("%3D", "=")
                    urls.append(actual_url)
                    f1.write(actual_url + "\n")
                    # print(actual_url)
            return urls
        else:
            print("Error:", response.status_code)


q1 = GoogleSearch()
print("Ready.")
#q1.search("chat.openai.com")

