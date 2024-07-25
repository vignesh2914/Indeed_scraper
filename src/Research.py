import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
from bs4 import BeautifulSoup
from typing import List, Dict
from exception import CustomException

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
        job_link = job.find("your tag", class_="your_class")
        job_link = job_link.text.strip() 

        if job_link != 'N/A':
            job_link = "https://www.indeed.com" + job_link


        job_results.append({
            'Job Title': job_title,
            'Company Name': company_name,
            'Location': location,
            'job_link': job_link
        })

    return job_results

def create_dataframe_of_job_data(job_data: List[Dict[str, str]]) -> pd.DataFrame:
    try:
        if job_data:
            column_names = ["Job Title", "Company Name", "Location", "Job Link"]
            df = pd.DataFrame(job_data, columns=column_names)
            logging.info("Data converted into dataframe")
            return df
        else:
            logging.info("No job data found to create dataframe.")
            return pd.DataFrame(columns=["Job Title", "Company Name", "Location", "Job Link"])
    except Exception as e:
        error_msg = f"An error occurred while creating the dataframe: {e}"
        logging.error(error_msg)
        raise CustomException(error_msg) from e

def get_unique_companies_df(df: pd.DataFrame, column_name: str) -> pd.DataFrame:
    try:
        filtered_df = df.drop_duplicates(subset=[column_name]).reset_index(drop=True)
        logging.info("Unique company name dataframe created")
        return filtered_df
    except Exception as e:
        error_msg = f"An error occurred while creating the unique companies dataframe: {e}"
        logging.error(error_msg)
        raise CustomException(error_msg) from e







job_title = input("Enter job title keyword: ")
location = input("Enter location keyword: ")
time_limit = int(input("Enter number of seconds to scrap: "))

scraped_data = scrape_job_data(job_title, location, time_limit)

dataframe = pd.DataFrame(scraped_data)

print(dataframe)






