import sys

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = "https://codejam.withgoogle.com/2018/challenges"
ROUND_NAME = "Round 1A 2018"


class Ranking:
	def __init__(self, rank, nickname, score):
		self.rank = rank
		self.nickname = nickname
		self.score = score

	def to_csv(self):
		return ",".join([str(self.rank), self.nickname, self.score])

def find_round_scoreboard(driver):
	WAIT.until(EC.visibility_of_element_located((By.CLASS_NAME, "adventures")))

	table = driver.find_element_by_class_name("adventures")
	rows = table.find_elements_by_tag_name("tr")[1:]
	for row in rows:
		cols = row.find_elements_by_tag_name("td")
		name = cols[0].text
		if ROUND_NAME == name:
			cols[4].find_element_by_tag_name("a").click()
			return
	raise Exception("Unknown Round Name: " + str(ROUND_NAME))

def scrap_scores_page(driver):
	WAIT.until(EC.visibility_of_element_located((By.CLASS_NAME, "scoreboard")))

	table = driver.find_element_by_class_name("scoreboard")
	rows = table.find_elements_by_tag_name("tr")[2:-1]
	for row in rows:
		cols = row.find_elements_by_tag_name("td")
		rank = int(cols[0].text)
		nickname = cols[2].text.encode(sys.stdout.encoding, errors='replace').decode(sys.stdout.encoding)
		score = cols[3].text
		print(Ranking(rank, nickname, score).to_csv())

driver = webdriver.Chrome()
driver.get(URL)

WAIT = WebDriverWait(driver, 10)

find_round_scoreboard(driver)

page_num = 0
pagination_xpath = "//ul[@class='pagination center-align']"
has_more_pages = True

while has_more_pages:
	WAIT.until(EC.visibility_of_element_located((By.XPATH, pagination_xpath)))
	pages = driver.find_elements_by_xpath(pagination_xpath + "//li")
	scrap_scores_page(driver)
	page_num += 1
	if page_num < len(pages):
		pages[page_num].find_element_by_tag_name("a").click()
	else:
		has_more_pages = False