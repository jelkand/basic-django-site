from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.refresh()
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def input_text_into_list_table(self, input_text):
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys(input_text)
        inputbox.send_keys(Keys.ENTER)


    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get(self.live_server_url)
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-do', header_text)

        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        #Insert 2 items into table, check if they are there.
        self.input_text_into_list_table('Buy peacock feathers')
        user1_list_url = self.browser.current_url
        #Assert REST format for url
        self.assertRegex(user1_list_url, '/lists/.+')
        self.check_for_row_in_list_table('1: Buy peacock feathers')
        self.input_text_into_list_table('Use peacock feathers to make a fly')
        self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')

        ##Test for a second user to ensure user lists are distinct.
        self.browser.refresh()
        self.browser.quit()
        self.browser = webdriver.Firefox()

        #Check that previous user's list is not on page
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)

        #Insert an item and check.
        self.input_text_into_list_table('Buy milk')
        self.check_for_row_in_list_table('1: Buy milk')

        #users should have different urls
        user2_list_url = self.browser.current_url
        self.assertRegex(user2_list_url, '/lists/.+')
        self.assertNotEqual(user2_list_url, user1_list_url)

    def test_layout_and_styling(self):
        #Check that input box is centered
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )

        #Check to see if list view is centered as well
        inputbox.send_keys('testing\n')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )
