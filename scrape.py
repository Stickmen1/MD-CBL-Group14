from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time
import requests
import zipfile
import os
import re
from datetime import datetime

# options = webdriver.ChromeOptions()
# options.add_argument('--headless')
# driver = webdriver.Chrome(options=options)
options = webdriver.EdgeOptions()
options.add_argument('--headless')
driver = webdriver.Edge(options=options)

def get_crimes(month):
    download_url = ''
    try:
        # Open the website
        driver.get('https://data.police.uk/data/')

        # Wait for the checkboxes to load
        wait = WebDriverWait(driver, 10)

        period_from = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#id_date_from')))
        # Check if the month value is present in the dropdown options
        select = Select(period_from)
        values = [option.get_attribute('value') for option in select.options]
        if month not in values:
            return ''
        select.select_by_value(month)  # Change this value to the desired option value

        period_to = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#id_date_to')))
        # Select a specific value from the start_period dropdown
        select = Select(period_to)
        select.select_by_value(month)  # Change this value to the desired option value


        checkbox = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#id_forces_5')))
        checkbox.click()

        checkbox = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#id_forces_25')))
        checkbox.click()

        checkbox = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#id_include_outcomes')))
        checkbox.click()

        checkbox = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#id_include_stop_and_search')))
        checkbox.click()

        # Find and click the submit button
        submit_button = driver.find_element(By.CSS_SELECTOR, '#downloads > form > button')
        submit_button.click()

        # Wait for a while to see the result
        time.sleep(5)
        download_link = driver.find_element(By.CSS_SELECTOR, '#content > div > a')
        download_url = download_link.get_attribute('href')        
    finally:        
        return download_url

def download_zip(url, dest_path):
    """
    Downloads a large zip file from the given URL and saves it to dest_path.
    Downloads in streaming mode to handle large files efficiently.
    """
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(dest_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
    print(f"Downloaded zip file to {dest_path}")

def unzip_and_delete(zip_path, extract_to):
    """
    Unzips the specified zip file to the given directory and deletes the original zip file.
    """
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    os.remove(zip_path)
    print(f"Unzipped to {extract_to} and deleted {zip_path}")

def get_missing_year_months(base_dir, min_ym='2023-11'):
    """
    Returns a list of year-month strings (YYYY-MM) greater than min_ym for which subdirectories do not exist in base_dir.
    """
    # Find all year-months in the format YYYY-MM in the base_dir
    pattern = re.compile(r'^(\d{4})-(\d{2})$')
    min_dt = datetime.strptime(min_ym, '%Y-%m')
    # List all items in the base directory
    existing = set()
    for name in os.listdir(base_dir):
        if os.path.isdir(os.path.join(base_dir, name)) and pattern.match(name):
            existing.add(name)
    # Generate all year-months from min_ym to current month
    now = datetime.now()
    ym_list = []
    y, m = min_dt.year, min_dt.month
    while (y < now.year) or (y == now.year and m <= now.month):
        ym = f"{y:04d}-{m:02d}"
        if ym not in existing:
            ym_list.append(ym)
        # Increment month
        m += 1
        if m > 12:
            m = 1
            y += 1
    return ym_list

def main(start):
    # place of py script + \\UK_Police_Data
    data_dir = os.path.dirname(os.path.abspath(__file__)) + '\\UK_police_data'

    months = get_missing_year_months(data_dir, start)
    for month in months:
        print(f"Processing month: {month}")
        url = get_crimes(month)
        if url:
            file_name = data_dir + 'crimes' + month + '.zip'
            download_zip(url, file_name)
            unzip_and_delete(file_name, data_dir)
    driver.quit()

main('2024-11')