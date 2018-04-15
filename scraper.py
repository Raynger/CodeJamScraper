from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = "https://codejam.withgoogle.com/2018/challenges"
ROUND_NAME = "Round 1A 2018"

def find_round_scoreboard(driver):
	wait = WebDriverWait(driver, 10)
	wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "adventures")))
	table = driver.find_element_by_class_name("adventures")
	rows = table.find_elements_by_tag_name("tr")[1:]
	for row in rows:
		cols = row.find_elements_by_tag_name("td")
		name = cols[0].text
		if ROUND_NAME == name:
			print("Round Found")
			cols[4].find_element_by_tag_name("a").click()
			return
	raise Exception("Unknown Round Name: " + str(ROUND_NAME))
	
driver = webdriver.Chrome()
driver.get(URL)
find_round_scoreboard(driver)
scrap_scores_page(driver)