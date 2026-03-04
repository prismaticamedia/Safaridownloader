import requests
import json

with open("cookies.json") as f:
    cookies = json.load(f)

# The target url was identified as SAFARI_BASE_URL + "/api/v2/epub-chapters/?epub_identifier=urn:orm:book:{0}"
url = "https://learning.oreilly.com/api/v2/epub-chapters/?epub_identifier=urn:orm:book:9781835880401"
res = requests.get(url, cookies=cookies)
data = res.json()

if "results" in data and len(data["results"]) > 0:
    first_chapter = data["results"][0]
    print("Chapter URL:", first_chapter.get("url"))
    print("Images keys present:", "images" in first_chapter)
    if "images" in first_chapter:
        print("Images array length:", len(first_chapter["images"]))
        if len(first_chapter["images"]) > 0:
            print("First image:", first_chapter["images"][0])
    
    print("\nAll keys in chapter data:", list(first_chapter.keys()))
else:
    print("No results found.")
