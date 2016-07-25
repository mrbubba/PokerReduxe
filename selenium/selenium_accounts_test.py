import selenium.webdriver as webdriver
import unittest
import time


class RegisterFuncTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()  # Optional argument, if not specified will search path.

    def test_register_page(self):
        """can we register a new user, and does it redirect to the login page"""

        driver = self.driver
        driver.get('http://127.0.0.1:8080/accounts/register')
        time.sleep(2)
        driver.find_element_by_id('id_user_name').clear()
        driver.find_element_by_id('id_user_name').send_keys('BobaFet')
        driver.find_element_by_id('id_password').clear()
        driver.find_element_by_id('id_password').send_keys('Kermitt')
        driver.find_element_by_id('register_button').click()
        time.sleep(2)
        title = driver.title
        self.assertIn('Login', title)
        time.sleep(2)
        driver.find_element_by_id('id_user_name').clear()
        driver.find_element_by_id('id_user_name').send_keys('BobaFet')
        driver.find_element_by_id('id_password').clear()
        driver.find_element_by_id('id_password').send_keys('Kermitt')
        driver.find_element_by_id('login_button').click()
        time.sleep(2)
        title = driver.title
        self.assertIn('Page not found at', title)
        driver.get('http://127.0.0.1:8080/admin')
        time.sleep(2)
        driver.find_element_by_id('id_username').clear()
        driver.find_element_by_id('id_username').send_keys('admin')
        time.sleep(2)
        driver.find_element_by_id('id_password').clear()
        driver.find_element_by_id('id_password').send_keys('pokerreduxe')
        driver.find_element_by_id('register_button').click()
        time.sleep(2)

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()