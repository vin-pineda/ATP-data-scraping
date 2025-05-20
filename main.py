from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time
import re

driver = webdriver.Chrome()
driver.get("https://www.tennisabstract.com/cgi-bin/leaders.cgi")
time.sleep(5)

soup = BeautifulSoup(driver.page_source, "html.parser")
driver.quit()

table = soup.find("table", id="matches")

rows = table.find_all("tr")[1:]

data = []
for row in rows:
    cells = [cell.text.strip() for cell in row.find_all(["td", "th"])]

    if not cells:
        continue

    cells = cells[1:]

    full_name = cells[0]
    match = re.match(r"^(.*?)(\s*\[[A-Z]{3}\])?$", full_name)
    player = match.group(1).strip()
    country = match.group(2).strip() if match.group(2) else ""

    new_row = [player, country] + cells[1:]
    data.append(new_row)

data = data[:-1]

headers = [th.text.strip() for th in table.find_all("th")]
headers = headers[1:]
headers[0] = "Player"
headers.insert(1, "Country")

df = pd.DataFrame(data, columns=headers)
df.to_csv("tennis_stats.csv", index=False)

print(df)
