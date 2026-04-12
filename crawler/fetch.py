import requests  # tool that lets Python talk to the internet

WIKIPEDIA_API = "https://en.wikipedia.org/w/api.php"  # Wikipedia's official API door

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"  # pretend to be a real browser so Wikipedia doesn't block us
}

def fetch_page(title):  # function that fetches one Wikipedia page by its title
    params = {
        "action": "query",       # tell API we want to look something up
        "format": "json",        # get the response as JSON (structured data)
        "titles": title,         # the page name we want to fetch
        "prop": "extracts",      # we want the text content of the page
        "explaintext": "1",      # give plain text, not messy HTML
    }

    response = requests.get(WIKIPEDIA_API, params=params, headers=HEADERS)  # send the request to Wikipedia
    data = response.json()  # convert the response into a Python dictionary

    pages = data["query"]["pages"]  # unwrap the outer envelope of the response
    page = next(iter(pages.values()))  # unwrap the inner envelope to get the actual page data

    return {
        "title": page.get("title", "Unknown"),  # extract the page title (use "Unknown" if missing)
        "text": page.get("extract", "")         # extract the full page text (use empty string if missing)
    }

def get_wikipedia_titles(category, limit=100):  # fetches a list of page titles from a Wikipedia category
    params = {
        "action": "query",
        "format": "json",
        "list": "categorymembers",      # get pages from a category
        "cmtitle": f"Category:{category}",  # the category to fetch from
        "cmlimit": str(limit),          # how many pages to fetch
        "cmtype": "page"                # only get pages, not subcategories
    }

    response = requests.get(WIKIPEDIA_API, params=params, headers=HEADERS)  # send request
    data = response.json()  # parse the response

    titles = [page["title"] for page in data["query"]["categorymembers"]]  # extract just the titles
    return titles  # return the list of titles