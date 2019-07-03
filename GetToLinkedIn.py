from Browsing.Browsing import login, setUp, wait_for

browser = ""


def main():
    global browser
    print('Starting the program\nSetting up Browser')
    browser = setUp()
    browser.get('https://www.linkedin.com/login')
    login('//*[@id="username"]', '//*[@id="password"]', '//*[@id="app__container"]/main/div/form/div[3]/button')
    print("Logged in")


main()
browser.quit()