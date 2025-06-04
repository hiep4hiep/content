from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)
#from selenium.webdriver.chrome.service import Service

#service = Service('/home/hiepn/content/Packs/AITools/chromedriver-linux64/chromedriver')
#driver = webdriver.Chrome(service=service)

driver.get("https://docs-cortex.paloaltonetworks.com/r/Cortex-XSIAM/Cortex-XSIAM-Documentation/Ingest-network-flow-logs-from-Amazon-S3")
html = driver.page_source

with open("amazon_s3.html", "w") as f:
    f.write(html)