from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import time

def google_search_urls(keyword, num_results):
    driver_path = 'C:\\p\\geckodriver.exe' #ubah sini
    service = FirefoxService(executable_path=driver_path)
    options = FirefoxOptions()
    options.binary_location = "C:\\Program Files\\Mozilla Firefox\\firefox.exe" #ubah sini
    options.headless = False
    driver = webdriver.Firefox(executable_path=driver_path, options=options)

    driver.get("https://www.google.com")
    search_box = driver.find_element('xpath', '//*[@id="APjFqb"]')
    search_box.send_keys(keyword)
    search_box.send_keys(Keys.RETURN)

    time.sleep(2)

    links = []
    while len(links) < num_results:
        results = driver.find_elements('xpath', '//*[@id="rso"]/div[3]/div/div/div[1]/div/div/a')
        for result in results:
            link = result.get_attribute("href")
            links.append(link)
            if len(links) == num_results:
                break
        next_page_button = driver.find_elements('xpath', '//a[@id="pnnext"]')
        if next_page_button:
            next_page_button[0].click() 
            time.sleep(2) 
        else:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            next_page_button = driver.find_elements('xpath', '//a[@id="pnnext"]')
            if not next_page_button:
                break

    driver.quit()
    return links[:num_results]

def save_to_file(filename, search_results):
    with open(filename, "w") as file:
        for url in search_results:
            file.write(url + "\n")

if __name__ == "__main__":
    filename = input("Masukkan nama file yang berisi keywords (contoh: keywords.txt): ")
    num_results = int(input("Masukkan jumlah hasil yang diinginkan (default 10): ") or 10)

    with open(filename, "r") as file:
        keywords = file.read().splitlines()

    all_search_results = []  # List to store all search results for each keyword
    for keyword in keywords:
        search_results = google_search_urls(keyword, num_results)
        all_search_results.extend(search_results)

    print("\nHasil pencarian:")
    for idx, url in enumerate(all_search_results, 1):
        print(f"{idx}. {url}")

    save_to_file("results_drog.txt", all_search_results)

    print("Hasil pencarian telah disimpan dalam file results_drog.txt")