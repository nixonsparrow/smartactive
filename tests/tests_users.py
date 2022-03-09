from time import sleep

from django.contrib.staticfiles.testing import LiveServerTestCase
from django.urls.base import reverse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as cond
from selenium.webdriver.support.ui import WebDriverWait

from users.models import User

# class UserCreationTestCase(LiveServerTestCase):
#     def setUp(self):
#         options = Options()
#         # options.headless = True
#         self.browser = webdriver.Firefox(options=options)
#
#     def tearDown(self):
#         self.browser.quit()
#
#     def test_browser_user_form_creates_user(self):
#         self.browser.get(self.live_server_url + reverse('user-create-form'))
#         WebDriverWait(self.browser, 5).until(cond.title_contains(''))
#
#         inputbox = self.browser.find_element(By.ID, 'id_username')
#         inputbox.send_keys('Tester')
#         inputbox = self.browser.find_element(By.ID, 'id_first_name')
#         inputbox.send_keys('Mahatma')
#         inputbox = self.browser.find_element(By.ID, 'id_last_name')
#         inputbox.send_keys('Gandhi')
#         inputbox = self.browser.find_element(By.ID, 'id_email')
#         inputbox.send_keys('test@wp.pl')
#         inputbox = self.browser.find_element(By.ID, 'id_password1')
#         inputbox.send_keys('G^*DFj#%(fgk)')
#         inputbox = self.browser.find_element(By.ID, 'id_password2')
#         inputbox.send_keys('G^*DFj#%(fgk)', Keys.ENTER)
#
#         sleep(5)
