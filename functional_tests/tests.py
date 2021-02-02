import re
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
import pytest

import time

MAX_WAIT = 10


@pytest.mark.functest
def test_can_start_a_list_for_one_user(live_server, selenium):
    # Edith has heard about a cool new online to-do app. She goes
    # to check out its homepage
    selenium.get(str(live_server))

    # She notices the page title and header mention to-do lists
    assert "To-Do" in selenium.title
    header_text = selenium.find_element_by_tag_name("h1").text
    assert "To-Do" in header_text

    # She is invited to enter a to-do item straight away
    inputbox = selenium.find_element_by_id("id_new_item")
    assert inputbox.get_attribute("placeholder") == "Enter a to-do item"

    # she types "Buy peacock feathers" into a text box (Edith's hobby
    # is tying fishing lures)
    inputbox.send_keys("Buy peacock feathers")

    # When she hits enter, the page updates, and now the page lists
    # '1: Buy peacock feathers' as an item in a to-do list
    inputbox.send_keys(Keys.ENTER)
    time.sleep(1)

    wait_for_row_in_list_table(selenium, "1: Buy peacock feathers")

    # There is still a text box inviting her to add another item. She
    # enters 'Use peacock feathers to make a fly' (Edith is very methodical)
    inputbox = selenium.find_element_by_id("id_new_item")
    inputbox.send_keys("Use peacock feathers to make a fly")
    inputbox.send_keys(Keys.ENTER)

    # The page updates again, and now shows both items on her list
    wait_for_row_in_list_table(selenium, "1: Buy peacock feathers")
    wait_for_row_in_list_table(selenium, "2: Use peacock feathers to make a fly")

    # Satisfied, she goes back to sleep


@pytest.mark.functest
def test_multiple_users_can_start_lists_at_different_urls(live_server, driver_factory):
    browser = driver_factory()

    # Edith starts a new to-do list
    browser.get(str(live_server))
    inputbox = browser.find_element_by_id("id_new_item")
    inputbox.send_keys("Buy peacock feathers")
    inputbox.send_keys(Keys.ENTER)
    wait_for_row_in_list_table(browser, "1: Buy peacock feathers")

    # she notices that her list has a unique URL
    edith_list_url = browser.current_url
    assert re.search(r"/lists/.+", edith_list_url)

    # Now a new user, Francis, comes along to the site.

    ## Use a new browser session to make sure no information
    ## of Edith's is coming through from cookies etc...
    browser.quit()
    browser = driver_factory()

    # Francis visits the home page. There is no sign of Edith's
    # list
    browser.get(str(live_server))
    page_text = browser.find_element_by_tag_name("body").text
    assert "Buy peacock feathers" not in page_text
    assert "make a fly" not in page_text

    # Francis starts a new list by entering a new item. He
    # is less interesting than Edith...
    inputbox = browser.find_element_by_id("id_new_item")
    inputbox.send_keys("Buy milk")
    inputbox.send_keys(Keys.ENTER)
    wait_for_row_in_list_table(browser, "1: Buy milk")

    # Francis gets his own unique URL
    francis_list_url = browser.current_url
    assert re.search(r"/lists/.+", francis_list_url)

    # Again, there is no trace of Edith's list
    page_text = browser.find_element_by_tag_name("body").text
    assert "Buy peacock feathers" not in page_text
    assert "make a fly" not in page_text

    # Satisfied, they both go back to sleep


# Helpers
def wait_for_row_in_list_table(browser, row_text):
    start_time = time.time()
    while True:
        try:
            table = browser.find_element_by_id("id_list_table")
            rows = table.find_elements_by_tag_name("tr")
            assert row_text in [row.text for row in rows]
            return
        except (AssertionError, WebDriverException) as e:
            if time.time() - start_time > MAX_WAIT:
                raise e
            time.sleep(0.5)