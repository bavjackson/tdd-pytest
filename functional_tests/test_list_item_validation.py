from selenium.webdriver.common.keys import Keys
import pytest

from .base import wait_for, wait_for_row_in_list_table


@pytest.mark.functest
def test_cannot_add_empty_list_items(live_server, selenium):
    # Edith goes to the home page and accidentally tries to submit
    # an empty list item. She hits Enter on the empty input box
    selenium.get(str(live_server))
    selenium.find_element_by_id("id_new_item").send_keys(Keys.ENTER)

    # The home page refreshes, and there is an error message syaing
    # that list items cannot be blank

    error_text = wait_for(selenium.find_element_by_css_selector(".has-error").text)
    assert error_text == "You can't have an empty list item"

    # She tries again with some text for the item, which now works
    selenium.find_element_by_id("id_new_item").send_keys("Buy milk")
    selenium.find_element_by_id("id_new_item").send_keys(Keys.ENTER)
    wait_for_row_in_list_table(selenium, "1: Buy milk")

    # Perversely, she now decides to submit a second blank list item
    selenium.find_element_by_id("id_new_item").send_keys(Keys.ENTER)

    # She recieves a similar warning on the list page
    error_text = wait_for(selenium.find_element_by_css_selector(".has-error").text)
    assert error_text == "You can't have an empty list item"

    # And she can correct it by filling some text in
    selenium.find_element_by_id("id_new_item").send_keys("Make tea")
    selenium.find_element_by_id("id_new_item").send_keys(Keys.ENTER)
    wait_for_row_in_list_table(selenium, "1: Buy milk")
    wait_for_row_in_list_table(selenium, "2: Make tea")
