from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options 
from webdriver_manager.chrome import ChromeDriverManager
import time

options = Options()
# options.add_argument("--headless")
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

url = "https://www.fishbase.se/search.php"
driver.get(url)

fish_name = "cichlid"  
search_input = driver.find_element("name", "CommonName")
search_input.send_keys(fish_name)
search_button = driver.find_element("xpath", "//input[@value='Search']")
search_button.click()

time.sleep(2)  

url = driver.current_url

all_links = driver.find_elements(By.TAG_NAME, "a")

fish_link = None
for link in all_links:
    if fish_name.lower() in link.text.lower():
        fish_link = link
        break

if fish_link:
    fish_link.click()
else:
    print(f"Link for fish '{fish_name}' not found.")

time.sleep(2)  

div_elements = driver.find_elements(By.CLASS_NAME, "smallSpace")

index = 1

indices_to_skip = [8, 10, 11, 14, 15, 16, 17, 18]

printed_estimates_heading = False
printed_estimates_content = False

for div_element in div_elements:
    try:
        div_content = div_element.text
        
        if index not in indices_to_skip and div_content.strip():  
            if index == 1:
                print("*Classification / Names*")
            elif index == 2:
                print("*Environment: milieu / climate zone / depth range / distribution range*")
            elif index == 3:
                print("*Distribution*")
            elif index == 4:
                print("*Length at first maturity / Size / Weight / Age*")
            elif index == 5:
                print("*Short description*")
            elif index == 6:
                print("*Biology*")
            elif index == 7:
                print("*Life cycle and mating behavior*")
            elif index == 9:
                print("*IUCN Red List Status*")
            elif index == 12:
                print("*Threat to humans*")
            elif index == 13:
                print("*Human uses*")
            elif index >= 19:
                if not printed_estimates_heading:
                    print("*Estimates based on models*")
                    printed_estimates_heading = True

            if index<19:
                print(div_content)
                print("")
            else:
                if printed_estimates_content:
                    print(div_content)
                printed_estimates_content = True

        index += 1
    except Exception as e:
        print("Error extracting content:", e)

driver.quit()
