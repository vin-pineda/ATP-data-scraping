from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time

driver = webdriver.Chrome()
driver.get("https://www.tennisabstract.com/cgi-bin/leaders.cgi")

time.sleep(5)

soup = BeautifulSoup(driver.page_source, "html.parser")
driver.quit()


table = soup.find("table", id="matches")

headers = [th.text.strip() for th in table.find_all("th")]

data = []
for row in table.find_all("tr")[1:]:
    cells = row.find_all(["td", "th"])
    data.append([cell.text.strip() for cell in cells])

data = data[:-1]

df = pd.DataFrame(data, columns=headers)

df.to_csv("tennis_stats.csv", index=False)

print(df)