import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium_stealth import stealth
import time
import pandas as pd
from bs4 import BeautifulSoup
from typing import List, Dict

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def make_url(job_keyword: str, location_keyword: str, index: int) -> str:
    url = f'https://in.indeed.com/jobs?q={job_keyword}&l={location_keyword}&start={index}'
    logging.info(f"Scraping URL: {url}")
    return url

def scrape_job_data(job_keyword: str, location_keyword: str, time_limit: int) -> List[Dict[str, str]]:
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--log-level=3")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--ignore-ssl-errors")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        
        job_results = []
        start_time = time.time()
        index = 0
        
        while (time.time() - start_time) < time_limit:
            url = make_url(job_keyword, location_keyword, index)
            driver.get(url)
            
            time.sleep(5)  
            
            page_soup = BeautifulSoup(driver.page_source, 'html.parser')
            scraped_data = parse_job_data_from_soup(page_soup)
            job_results.extend(scraped_data)
            
            index += 10  
            
            time.sleep(5)  
        
        return job_results
    
    except Exception as e:
        logging.error(f"An error occurred during scraping: {str(e)}")
        return []

    finally:
        if 'driver' in locals():
            driver.quit()

def parse_job_data_from_soup(page_soup):
    jobs = page_soup.find_all("div", class_="job_seen_beacon")
    job_results = []

    for job in jobs:
        title = job.find("your tag", class_="your_class")
        job_title = title.text.strip()
        company = job.find("your tag", class_="your_class")
        company_name = company.text.strip() 
        location = job.find("your tag", class_="your_class")
        location = location.text.strip() 

        job_results.append({
            'Job Title': job_title,
            'Company Name': company_name,
            'Location': location
        })

    return job_results

job_title = input("Enter job title keyword: ")
location = input("Enter location keyword: ")
time_limit = int(input("Enter number of seconds to scrap: "))

scraped_data = scrape_job_data(job_title, location, time_limit)

dataframe = pd.DataFrame(scraped_data)

print(dataframe)










# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.common.by import By
# from selenium_stealth import stealth
# import time
# import requests
# from bs4 import BeautifulSoup

# options = webdriver.ChromeOptions()
# options.add_argument('--headless')
# options.add_argument('--disable-gpu')
# options.add_argument('--no-sandbox')
# options.add_argument('--disable-dev-shm-usage')
# options.add_argument("--log-level=3")
# options.add_argument("--ignore-certificate-errors")
# options.add_argument("--ignore-ssl-errors")
# options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# stealth(driver,
#         languages=["en-US", "en"],
#         vendor="Google Inc.",
#         platform="Win32",
#         webgl_vendor="Intel Inc.",
#         renderer="Intel Iris OpenGL Engine",
#         fix_hairline=True,
# )

# url = 'https://in.indeed.com/jobs?q=java&l=chennai&from=searchOnHP&vjk=595459980e65a97f'
# driver.get(url)

# # Allow the page to load
# time.sleep(5)

# response = requests.get(url, headers={
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
# })
# soup = BeautifulSoup(response.content, 'html.parser')


# # job_cards = driver.find_elements(By.XPATH, '//*[@id="mosaic-provider-jobcards"]/ul/li/div')

# job_cards = driver.find_elements(By.CLASS_NAME, 'mosaic-zone')

# job_results = []

# for job_card in job_cards:
#     try:
#         title_elem = job_card.find_element(By.XPATH, '//*[@id="mosaic-provider-jobcards"]/ul/li[1]/div/div/div/div/div/table/tbody/tr/td[1]/div[1]/h2')
#         title = title_elem.text.strip()
#         location_elem = job_card.find_element(By.XPATH, '//*[@id="mosaic-provider-jobcards"]/ul/li[1]/div/div/div/div/div/table/tbody/tr/td[1]/div[2]/div/div[2]')
#         job_location = location_elem.text.strip()
#         company_name = job_card.find_element(By.XPATH, '//*[@id="mosaic-provider-jobcards"]/ul/li[1]/div/div/div/div/div/table/tbody/tr/td[1]/div[2]')
#         company_name = company_name.text.strip()


#         job_results.append({
#             'Job Title': title,
#             'Job Location': job_location,
#             'Comapny Name' :company_name
#         })
#     except Exception as e:
#         print(f"Error: {e}")

#     time.sleep(3)  # wait for the job page to load

# print(job_results)

# driver.quit()













































# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.common.by import By
# from selenium_stealth import stealth
# import time

# options = webdriver.ChromeOptions()
# options.add_argument('--headless')
# options.add_argument('--disable-gpu')
# options.add_argument('--no-sandbox')
# options.add_argument('--disable-dev-shm-usage')
# options.add_argument("--log-level=3")
# options.add_argument("--ignore-certificate-errors")
# options.add_argument("--ignore-ssl-errors")
# options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# stealth(driver,
#         languages=["en-US", "en"],
#         vendor="Google Inc.",
#         platform="Win32",
#         webgl_vendor="Intel Inc.",
#         renderer="Intel Iris OpenGL Engine",
#         fix_hairline=True,
# )


# url = 'https://in.indeed.com/jobs?q=Data_Scientist&l=india&from=searchOnHP&vjk=595459980e65a97f'
# driver.get(url)


# time.sleep(5)  # wait for the page to load

# job_cards = driver.find_elements(By.XPATH, '//*[@id="mosaic-provider-jobcards"]/ul/li/div')

# job_results = []

# for job_card in job_cards:
#     try:
#         title_elem = job_card.find_element(By.XPATH, './/h2[@class="jobTitle css-198pbd eu4oa1w0"]')
#         title = title_elem.text.strip()
#         location = job_card.find_element(By.XPATH, '//*[@id="mosaic-provider-jobcards"]/ul/li[1]/div/div/div/div/div/table/tbody/tr/td[1]/div[2]/div/div[2]')
#         job_location = location.text.strip()

#         job_results.append({
#             'Job Title': title,
#             'Job Location': job_location
#         })
#     except Exception as e:
#         print(f"Error: {e}")

#     time.sleep(3)  # wait for the job page to load

# print(job_results)

# driver.quit()













# from selenium import webdriver
# import time
# from selenium.webdriver.common.by import By
# from selenium_stealth import stealth
# from webdriver_manager.chrome import ChromeDriverManager
# from bs4 import BeautifulSoup
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.chrome.service import Service


# def get_current_url(url, job_title, location):
#     options = webdriver.ChromeOptions()
#     options.add_argument('--headless')
#     options.add_argument('--disable-gpu')
#     options.add_argument('--no-sandbox')
#     options.add_argument('--disable-dev-shm-usage')
#     options.add_argument("--log-level=3")
#     options.add_argument("--ignore-certificate-errors")
#     options.add_argument("--ignore-ssl-errors")
#     options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
#     stealth(driver,
#             languages=["en-US", "en"],
#             vendor="Google Inc.",
#             platform="Win32",
#             webgl_vendor="Intel Inc.",
#             renderer="Intel Iris OpenGL Engine",
#             fix_hairline=True,
#     )
#     try:
#         driver.get(url)
#         time.sleep(3)

#         # Input job title and location
#         job_title_field = driver.find_element(By.XPATH, '//*[@id="text-input-what"]')
#         job_title_field.send_keys(job_title)
#         job_location_field = driver.find_element(By.XPATH, '//*[@id="text-input-where"]')
#         job_location_field.send_keys(location)

#         submit_button = driver.find_element(By.XPATH, '//*[@id="jobsearch"]/div/div[2]/button')
#         submit_button.click()
#         time.sleep(3)

#         # Get current URL after search
#         current_url = driver.current_url

#         return driver, current_url

#     except Exception as e:
#         print(f"Error occurred: {str(e)}")
#         return None, None

# def scrape_job_details(driver):
#     job_details = []

#     try:
#         # Wait for the job listings to load
#         WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="mosaic-provider-jobcards"]/ul/li[1]/div')))
        
        
#         # Get the page source and create a BeautifulSoup object
#         soup = BeautifulSoup(driver.page_source, 'html.parser')

#         job_cards = soup.find_all('div', class_='cardOutline tapItem dd-privacy-allow result job_cb23ae101ec34931 resultWithShelf sponTapItem desktop css-yria2i eu4oa1w0')

#         for job_card in job_cards:
#             job_role = job_card.find('h2', class_='jobTitle css-198pbd eu4oa1w0').text.strip()
#             location = job_card.find('div', class_='company_location css-17fky0v e37uo190').text.strip()
#             job_link = job_card.find('a', class_='jcs-JobTitle css-jspxzf eu4oa1w0')['href']

#             # Navigate to job details page to get company link
#             driver.get('https://in.indeed.com' + job_link)
#             time.sleep(3)
            
#             # Extract company link
#             company_link_element = driver.find_element(By.XPATH, '//*[@id="viewJobSSRRoot"]/div[2]/div[3]/div/div/div[1]/div[2]/div[2]/div[2]/div/a')
#             company_link = company_link_element.get_attribute('href')

#             job_details.append({
#                 'job_role': job_role,
#                 'location': location,
#                 'job_link': job_link,
#                 'company_link': company_link
#             })

#     except Exception as e:
#         print(f"Error occurred while scraping: {str(e)}")

#     return job_details

# driver, current_url = get_current_url('https://in.indeed.com/', 'Data Scientist', 'Bengaluru')
# if current_url:
#     print(f"Current URL: {current_url}")
#     job_details = scrape_job_details(driver)
#     if job_details:
#         for job in job_details:
#             print(f"Job Role: {job['job_role']}")
#             print(f"Location: {job['location']}")
#             print(f"Job Link: https://in.indeed.com{job['job_link']}")
#             print(f"Company Link: {job['company_link']}")
#             print("---------------------------")
#     else:
#         print("No job details found.")
# else:
#     print("Failed to retrieve current URL.")

# if driver:
#     driver.quit()

