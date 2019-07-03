import selenium
from selenium import webdriver
from getpass import getpass  # For getting the User's password
from selenium import webdriver  # Gives access to the browser
from selenium.webdriver.support.ui import WebDriverWait  # Allows the browser to pause
from selenium.webdriver.support import expected_conditions as ec  # Make browser get conditions
from selenium.webdriver.common.by import By  # Get methods of identifying elements
import selenium.common.exceptions as exceptions  # The exceptions module of Selenium
import json  # For reading credentials file

browser = ""
credentials_file_name = 'credentials.json'


def wait_for(text, delay=10, by=By.XPATH, check_again_limit=3, one_as_list=True):
    check = 0
    try:
        elements = WebDriverWait(browser, delay).until(ec.presence_of_all_elements_located((by, text)))
    except exceptions.TimeoutException:
        if check < check_again_limit:
            elements = WebDriverWait(browser, delay).until(ec.presence_of_all_elements_located((by, text)))
        else:
            return None
        check += 1
    if len(elements) == 0:
        return None
    elif len(elements) == 1:
        if one_as_list:
            return browser.find_elements(by, text)
        else:
            return elements[0]
    return elements


def login_info():
    try:
        # Try to open the file in read mode
        # if it doesn't exist it throws an exception
        with open(credentials_file_name) as credentials_file:
            credentials = json.load(credentials_file)
            user_name = credentials['user']
            user_pass = credentials['password']
    except FileNotFoundError:
        with open(credentials_file_name, 'w+') as credentials_file:
            # For sure the file had nothing, therefore
            user_name = str(input("Username: "))
            user_pass = getpass()
            json.dump(
                {'user': user_name,
                 'password': user_pass
                 },
                credentials_file
            )

    return user_name, user_pass


def login(email_elem_xpath, password_elem_xpath, submit_elem_xpath):
    email_elem = wait_for(email_elem_xpath, one_as_list=False)
    password_elem = wait_for(password_elem_xpath, one_as_list=False)
    print('At the login page')
    username, password = login_info()
    email_elem.send_keys(username)
    print('Username entered')
    password_elem.send_keys(password)
    print('Password entered')
    wait_for(submit_elem_xpath, one_as_list=False).click()
    print('Logging in')


def main():
    global browser
    print('Starting the program\nSetting up Browser')
    browser = webdriver.Safari()
    browser.get('https://www.linkedin.com/login')
    login('//*[@id="username"]', '//*[@id="password"]', '//*[@id="app__container"]/main/div/form/div[3]/button')
    print("Logged in")


main()