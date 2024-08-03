from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
import time

# Step 1: Set up Edge WebDriver
edge_options = Options()
# Optional: Configure additional options here if needed
# edge_options.add_argument('--headless')

# Update the path to your msedgedriver.exe
service = Service(executable_path='C:/Users/Alfaize/Desktop/New folder/msedgedriver.exe')

driver = webdriver.Edge(service=service, options=edge_options)

# Step 2: Open the login page
driver.get("http://the-internet.herokuapp.com/login")

# Step 3: Find the username and password fields
username_field = driver.find_element(By.ID, "username")
password_field = driver.find_element(By.ID, "password")

# Step 4: Enter login credentials
username_field.send_keys("tomsmith")
password_field.send_keys("SuperSecretPassword!")

# Step 5: Submit the login form
password_field.send_keys(Keys.RETURN)

# Step 6: Wait for the login to process
time.sleep(3)

# Step 7: Verify successful login
success_message = driver.find_element(By.CSS_SELECTOR, ".flash.success").text
assert "You logged into a secure area!" in success_message

# Step 8: Log out (if applicable)
logout_button = driver.find_element(By.CSS_SELECTOR, "a[href='/logout']")
logout_button.click()

# Step 9: Verify successful logout
logout_message = driver.find_element(By.CSS_SELECTOR, ".flash.success").text
assert "You logged out of the secure area!" in logout_message

# Step 10: Close the browser
driver.quit()
