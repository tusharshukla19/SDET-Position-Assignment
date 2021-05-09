from selenium import webdriver
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import datetime

# Get URLs for the towns
def get_url(town):
    global driver
    driver = webdriver.Chrome(ChromeDriverManager().install())
    url = "https://sso.eservices.jud.ct.gov/foreclosures/Public/PendPostbyTownDetails.aspx?town=" + town
    return url

# Create a beautiful soup object for data manipulation (Using scraping)
def create_soup(url):
    driver.get(url)
    content = driver.page_source
    soup = BeautifulSoup(content, "html.parser")   
    return soup 

# Verify date is within 7 days or not
def sale_date_difference(row):
    sale_date = get_sale_date(row)
    today_date = datetime.datetime.today()
    difference = today_date - sale_date
    days = int(difference.days)
    return days

# Get url & open it on another tab
def view_notice(row):
    anchor = row.contents[5]
    for i in anchor:
        anchor_href = i.attrs["href"]
        href_url = "https://sso.eservices.jud.ct.gov/foreclosures/Public/" + anchor_href
        script = "window.open('{}', '_blank')".format(href_url)
        driver.execute_script(script)

# Get sale date from beautiful soup object & date manipulation
def get_sale_date(row):
    row_text = row.getText()

    strip_row = row_text.strip('\n')
    split_row = strip_row.split('\n')

    raw_date = split_row[1].split('/')
    
    yyyy = raw_date[2][0:4]
    mm = raw_date[0]
    dd = raw_date[1]    
    
    filter_date = yyyy + "-" + mm + "-" + dd
    sale_date = datetime.datetime.strptime(filter_date, '%Y-%m-%d')
    return sale_date
