from selenium import webdriver
from selenium.webdriver import DesiredCapabilities

conf = {
    # use chrome service in docker-compose
    'selemium_endpoint': 'http://chrome:4444/wd/hub',
    'sample_URL': 'http://example.com'
}

driver = webdriver.Remote(
    command_executor=conf['selemium_endpoint'],
    desired_capabilities=DesiredCapabilities.CHROME.copy())
try:
    driver.get(conf['sample_URL'])
    print('title:', driver.title)
finally:
    driver.quit()
