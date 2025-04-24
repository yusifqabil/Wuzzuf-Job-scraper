from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd 
import time 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests 
# Initiating a web driver 
driver = webdriver.Chrome()
driver.implicitly_wait(60)
driver.get("https://wuzzuf.net/jobs/egypt")
history = [driver.current_url]
# Creating a function to check if the last page of the search query has been reached
def urlCheck(url,all):
     if url in all : 
          return True 
     else : 
          return False 
# getting the elements required to enter the search query
textField = driver.find_element(By.TAG_NAME,"input")
button = driver.find_element(By.XPATH,"""//*[@id="app"]/div/div/main/div[2]/div[1]/form/button""")
textField.send_keys("Data Analyst")
button.click()
# Creating a list to hold the results
result = []
# A While loop to loop through the pages until the function returns true
while True : 
    time.sleep(5)
    check = urlCheck(driver.current_url,history)
    if check == True :
         break 
     #     Making BeautifulSoup Handle the HTML file of the current URL
    request = requests.get(driver.current_url)
    soup = BeautifulSoup(request.text,"html.parser")
     #     getting hold of the job cards , companies , experience 
    allJCards = soup.select(".css-m604qf a")
    companies = soup.select("a.css-17s97q8")
    experience = soup.select(".css-y4udm8 div > span:nth-of-type(1)")
     #     Adding a print statement to separate pages 
    print("---------------NEW PAGE--------------")
     #     looping through the job postings and companies list simultaneously and storing the result in a tuple
    for i,card in enumerate(allJCards) :
        result.append((card.string,companies[i].string,experience[i].contents[2],card["href"]))
     #     Pressing the NEXT page button ,adding an explicit wait for the button to be clickable 
    try :
         element = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".css-1q4vxyr button")))
         nextButton = driver.find_elements(By.CSS_SELECTOR,".css-1q4vxyr button")[-1]
         history.append(driver.current_url)
         nextButton.click()
    except : 
         break 
    else:
         continue
# Ending the session
driver.quit()
# Creating a pandas dataframe to hold the results gracefully to be exported as CSV format
dataFrame = pd.DataFrame(result,columns=["JOB","HIRER","EXPERIENCE LEVEL","LINK"])
dataFrame.to_csv("output",index=False)
