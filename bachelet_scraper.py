import requests
from bs4 import BeautifulSoup
import html5lib

article_number = 0
all_articles = []

for p in range(1,381):
  print(f"Scraping page number: {p}")
  url = f"http://archivospresidenciales.archivonacional.cl/index.php/search?page={p}&mediatypes=137&query=pobreza+y+pol%C3%ADticas+sociales&limit=20&sort=alphabetic"
  link_url_base = "http://archivospresidenciales.archivonacional.cl"

  headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}
  r = requests.get(url=url, headers=headers)
  soup = BeautifulSoup(r.content, 'html5lib')
  titles = []
  titles = soup.find_all('p', attrs = {'class':'title'})
  for t in titles:
    article_number += 1
    name = f"{str(article_number).zfill(2)}- {t.get_text()}"
    link = link_url_base + t.find("a")["href"]
    article = (name, link)
    all_articles.append(article)
	
print(f"Total articles: {len(all_articles)}")

# Just in case, I save it not to scrap again all the indexes
with open("all_links.txt", 'w') as f:
  for a in all_articles:
    f.write(f"('{a[0]}','{a[1]}')")
	

# For every single article visit the corresponding page and download the thingy
for article in all_articles:
  print(f"Generating article: {article[0]}")
  filename = article[0]
  url = article[1]
  r = requests.get(url=url, headers=headers)
  soup = BeautifulSoup(r.content, 'html5lib')
  article_link = soup.find("div", class_="digital-object-reference")
  download_link = article_link.find("a")["href"] #get the specific download link
  response = requests.get(download_link) #and download :)
  if len(filename) > 210:
    filename = filename[0:210] + "__truncated"
  filename += ".pdf"
  with open(filename, "wb") as f:
    f.write(response.content)
