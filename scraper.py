#Made and worked during the 2021 Black Friday sales. Websites may have changed since hand in.
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys 
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, ElementClickInterceptedException 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup 
import time
import warnings

#allow webdriver options
options = webdriver.ChromeOptions()
# options.add_argument("--headless")
# options.add_argument("--incognito")

#turn off terminal warnings to only show printed results
options.add_argument("--log-level=3")
warnings.filterwarnings("ignore")

#paths to webdriver placed in same folder as script and allows for custom options
driver = webdriver.Chrome(r"./chromedriver.exe", options=options)

#urls
ho_url = "https://www.hyperoptic.com"
bt_url = "https://www.bt.com/broadband"

#my postcode
postcode = "CT11 0PB" 

#function for scraping hyperoptic site to avoid repeating code
def hyperoptic(contract_length):

    #captures page source
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    #finds the available broadband packages
    deals = soup.find("div", {"class": "packages-wr"})
    package_elements = deals.find_all("div", class_="package")

    #for each deal
    for package_element in package_elements:
        #extracts title of broadband deal from img src and capitalises
        title_element = package_element.find("img")["src"][70:][:-9].capitalize()
        
        #finds and concatenates two spans with information relating to price neatly
        price_element = package_element.find("span", class_="price").text + " " + package_element.find("span", class_="font-f-museo-700").text
        
        #combines two spans in order to provide speed information
        speed_element = package_element.find("span", class_="size").text + package_element.find("span", class_="unit").text

        #split span into list of strings and extract the last in the list
        setup_element = package_element.find("span", class_="font-f-museo-500").text.split('\n')[-1]

        #prints information in an organised way
        print('\n')
        print(title_element)
        print(price_element)
        print(speed_element)
        print(setup_element)
        print(contract_length) # We know where we navigated to with Selenium and passed that into the function


def BT():

    #captures page source
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    #finds the available broadband packages
    deals = soup.find("div", {"id": "product-list"})
    package_elements = deals.find_all("div", class_="jss316")

    #for each deal
    for package_element in package_elements:
        #extracts the name of deal from div
        title_element = package_element.find("div", id="product-name").text
        
        #extracts relevant pricing information and combines them neatly (the first part coming from nested divs), removing the triangle which has lost its context cues from the website.
        price_element = package_element.find("div", class_="jss1798").findAll("div")[1].text + " " + package_element.find("span", class_="jss1802").text.replace("Δ", "")
        
        #collects speed information out of a parent div of nested divs/spans that had no class/id/name information to narrow down the extraction. 
        # replaces "D" with " D" in order to clean up resulting text, as speed and Download were mushed together originally ( e.g. 500MbDownload speed)
        speed_element = package_element.find("div", class_="jss1746").text.replace("D", " D")
 
        #extracts setup pricing information
        setup_element = package_element.find("span", class_="jss1818").text

        #extracts information on length of contract and removes superfluous whitespeace before 'month'
        contract_length = package_element.find("div", id="contract-length").text.replace(" m", "m")

        #prints information in an organised way
        print('\n')
        print(title_element)
        print(price_element)
        print(speed_element)
        print(setup_element)
        print(contract_length)


################## Hyperoptic ##################

#navigate to hyperoptic url
driver.get(ho_url);

#print Hyperoptic as reference to which providers deals these are
print("\n" + "Hyperoptic")

#accept cookies
driver.find_element_by_css_selector(".modal-button.accept").click()

#click on 24 month deals
driver.find_element_by_css_selector("label[for='contractButton0']").click()

#run hyperoptic function and pass in the length of contract we have told selenium to click on
hyperoptic("24 Month Contract")

#click on 12 month deals
driver.find_element_by_css_selector("label[for='contractButton1']").click()

#run hyperoptic function and pass in the length of contract we have told selenium to click on
hyperoptic("12 Month Contract")

#click on rolling contract deals
driver.find_element_by_css_selector("label[for='contractButton2']").click()

#run hyperoptic function and pass in the length of contract we have told selenium to click on
hyperoptic("Monthly Rolling Contract")

################### BT Broadband #################

#navigate to bt url
driver.get(bt_url);

#switch to frame containing accept cookies button
driver.switch_to.frame(driver.find_element_by_xpath("//iframe[@class='truste_popframe']"))

#accept cookies
WebDriverWait(driver, 10).until(EC.element_to_be_clickable(driver.find_element_by_link_text('Accept all cookies'))).click()

#switch back to default page content frame
driver.switch_to.default_content()

#find and select box to input postcode
postcode_box = driver.find_element_by_xpath("//input[@id='sc-postcode']")
postcode_box.click()

#type and enter my postcode
postcode_box.send_keys(postcode)
postcode_box.submit()

#wait for it to load
time.sleep(1)

#search the options for the correct address and choose it
elem = driver.find_element_by_id("tvsc-address")
for option in elem.find_elements_by_tag_name("option"):
    if option.text == "47 Eskdale Avenue, Ramsgate, CT11 0PB":
        option.click()
        break

#click button to confirm the address
driver.find_element_by_id("btnCustomConfirmAddress").click()

#allow page to load
time.sleep(5)

#print BT for clarity as to who provides the following deals
print("\n" + "BT")

#runs function to scrape BT deals
BT()

#closes web driver
driver.quit()

