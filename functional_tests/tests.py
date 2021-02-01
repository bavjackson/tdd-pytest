from selenium.webdriver.common.keys import Keys
import pytest

import time


@pytest.mark.functest
def test_can_start_a_list_and_retrieve_it_later(live_server, browser):
    # Edith has heard about a cool new online to-do app. She goes
    # to check out its homepage
    browser.get(str(live_server))

    # She notices the page title and header mention to-do lists
    assert "To-Do" in browser.title
    header_text = browser.find_element_by_tag_name("h1").text
    assert "To-Do" in header_text

    # She is invited to enter a to-do item straight away
    inputbox = browser.find_element_by_id("id_new_item")
    assert inputbox.get_attribute("placeholder") == "Enter a to-do item"

    # she types "Buy peacock feathers" into a text box (Edith's hobby
    # is tying fishing lures)
    inputbox.send_keys("Buy peacock feathers")

    # When she hits enter, the page updates, and now the page lists
    # '1: Buy peacock feathers' as an item in a to-do list
    inputbox.send_keys(Keys.ENTER)
    time.sleep(1)

    check_for_row_in_list_table(browser, "1: Buy peacock feathers")

    # There is still a text box inviting her to add another item. She
    # enters 'Use peacock feathers to make a fly' (Edith is very methodical)
    inputbox = browser.find_element_by_id("id_new_item")
    inputbox.send_keys("Use peacock feathers to make a fly")
    inputbox.send_keys(Keys.ENTER)
    time.sleep(1)

    # The page updates again, and now shows both items on her list
    check_for_row_in_list_table(browser, "1: Buy peacock feathers")
    check_for_row_in_list_table(browser, "2: Use peacock feathers to make a fly")

    # Edith wonders whether the site will remember her list. The she sees
    # that the site has generated a unique URL for her -- there is some
    # explanatory text to that effect.
    assert 0, "Finish the test!"

    # she visits that URL - her to-do list is still there.

    # Satisfied, she goes back to sleep


# Helpers
def check_for_row_in_list_table(browser, row_text):
    table = browser.find_element_by_id("id_list_table")
    rows = table.find_elements_by_tag_name("tr")
    assert row_text in [row.text for row in rows]