#!/usr/bin/env python3

import os
import sys
import requests
import json
import csv
import html
import re
import time

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait 

def get_page(url):
    filename = url.replace('https://', '').replace('/', '-') + '.html'

    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        return content

    response = requests.get(
        url=url,
    )
    with open(filename, 'w', encoding="utf-8") as f:
        f.write(response.text)
    return response.text

def save_csv(books):
    with open('books.csv', 'w', newline='') as file:
        fieldnames = ['id', 'title', 'description', 'url', 'price', 'pages', 'newTime', 'isNew', 'categoryid', 'categoryname', 'bLink', 'label']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for book in books:
            writer.writerow(book)

def extract_book_data(html):
    soup = BeautifulSoup(html, features='lxml')
    script_tag = soup.find('script', type='text/javascript', text=re.compile('bookData'))

    json_str = re.search(r'bookData: (\[.*\])', script_tag.string).group(1)
    books = json.loads(json_str)

    save_csv(books)

    return books

def download_book(book_url):
    print('Trying to download a book ' + book_url)
    current_directory = os.getcwd()
    parent_directory = os.path.abspath(os.path.join(current_directory, os.pardir))
    download_directory = os.path.join(parent_directory, 'downloads')

    options = webdriver.ChromeOptions()
    options.add_experimental_option('prefs', {
        "download.default_directory": download_directory,
        "download.prompt_for_download": False, 
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True
    })

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    driver.get(book_url)

    element = WebDriverWait(driver, 20).until(lambda x: x.find_element(by=By.CLASS_NAME, value='buttonBar'))

    time.sleep(1) 

    try:
        button_bars = driver.find_elements(by=By.CLASS_NAME, value='buttonBar')
        if button_bars: 
            right_button_bar = button_bars[1] 
            buttons = right_button_bar.find_elements(by=By.CLASS_NAME, value='button')
            if len(buttons) >= 3:
                download_button = buttons[1] # 2'nd button (from right to left) is the download button
                download_button.click()
                print('Clicked Download')
            else:
                print('Not enough buttons found.')
        else:
            print('No button bars found.')
    except Exception as e:
        print(f"Error clicking the download button: {e}")

    time.sleep(10)

    print('Book download finished: ' + book['title'])

    driver.quit()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Wrong number of arguments provided. Supply a FlipHTML5 URL as an argument.")
        sys.exit(1)
    url = sys.argv[1]
    if not url.startswith("https://fliphtml5.com/bookcase/"):
        print("Wrong URL provided. Use a fully qualified URL: 'https://fliphtml5.com/bookcase/<BOOKCASE_ID>'")

    print("Processing URL: " + url)

    page_html = get_page(url)
    print(page_html)
    books = extract_book_data(page_html)

    for book in books:
        print(book['title'], book['url'])

    for book in books:
        download_book(book['url'])
        time.sleep(2)
