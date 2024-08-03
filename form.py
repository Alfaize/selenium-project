import csv
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from datetime import datetime

# Setup Edge options if needed
edge_options = Options()
# Example: edge_options.add_argument('--headless')  # Run in headless mode

# Initialize WebDriver
driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()), options=edge_options)

# Define the URL of the form and form data
form_url = 'https://forms.gle/C7g1XZux2K9ExRcDA'
form_data = {
    'name': 'mithilesh',
    'email': 'mithilesh@example.com',
    'feedback': 'lorem ipsum helllo how are you doing today i am good',
}

# Define the expected confirmation message
expected_confirmation_message = 'Your response has been recorded.'

def submit_form(data):
    driver.get(form_url)
    
    try:
        # Wait for the name field to be present and fill it
        name_field = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//*[@aria-labelledby="i1"]'))
        )
        name_field.send_keys(data['name'])
        print("Name field filled.")
        
        # Find the email field
        email_field = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//*[@aria-labelledby="i5"]'))
        )
        email_field.send_keys(data['email'])
        print("Email field filled.")
        
        # Find the feedback textarea
        feedback_field = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//*[@aria-labelledby="i9"]'))
        )
        feedback_field.send_keys(data['feedback'])
        print("Feedback field filled.")
        
        # Attempt to click the submit button
        submit_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//div[@role="button" and contains(text(), "Submit")]'))
        )
        submit_button.click()
        print("Submit button clicked.")
        
        # Additional wait for confirmation
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), '{expected_confirmation_message}')]"))
        )
        print("Confirmation message found.")
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        # Attempt form submission with JavaScript if clicking does not work
        try:
            driver.execute_script('document.querySelector("form").submit();')
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), '{expected_confirmation_message}')]"))
            )
            print("JavaScript submission succeeded.")
            return True
        except Exception as js_exception:
            print(f"JavaScript submission also failed: {js_exception}")
            return False

def main():
    # Perform the form submission
    submission_success = submit_form(form_data)
    
    # Log the result
    result = {
        'Form Submitted': 'Yes' if submission_success else 'No',
        'Submission Date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    print(result)

    # Save the result to a CSV file
    with open('form_submission_result.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['Form Submitted', 'Submission Date'])
        writer.writeheader()
        writer.writerow(result)

# Ensure proper closing of resources
if __name__ == "__main__":
    try:
        main()
    finally:
        if driver:
            driver.quit()
