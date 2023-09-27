import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Main:
  def __init__(self) -> None:
    self.chromeOptions = chromeOptions = uc.ChromeOptions() 
    #chromeOptions = webdriver.ChromeOptions() 
    chromeOptions.binary_location = '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary'
    #chromeOptions.executable_path = driver_path
    #chromeOptions.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 1}) 
    chromeOptions.add_argument("user-data-dir=/Users/kirthi/Library/Application Support/Google/Chrome Canary")
    chromeOptions.add_argument("--no-sandbox") 
    chromeOptions.add_argument("--disable-setuid-sandbox") 
    chromeOptions.add_argument("--disable-extensions") 
    chromeOptions.add_argument("--disable-gpu") 
    chromeOptions.add_argument("disable-infobars")

    self.url    = 'https://accounts.google.com/ServiceLogin'
    self.driver = driver = uc.Chrome(use_subprocess=True)
    self.time   = 10
    
  def login(self, email, password):
    self.driver.get(self.url)
    WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.NAME, 'identifier'))).send_keys(f'{email}\n')
    WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.NAME, 'Passwd'))).send_keys(f'{password}\n')
            
                                                                                  
if __name__ == "__main__":
  #  ---------- EDIT ----------
  email = 'kirthi.balakrishnan@gmail.com' # replace email
  password = '' # replace password
  #  ---------- EDIT ----------                                                                                                                                                         
 
  driver = Main()
  driver.login(email, password)                                                                                
