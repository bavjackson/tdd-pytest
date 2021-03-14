from selenium.webdriver.common.keys import Keys
import pytest

from .base import wait_for_row_in_list_table


@pytest.mark.functest
def test_layout_and_stying(live_server, selenium):
    # Edith goes to the home page
    selenium.get(str(live_server))
    selenium.set_window_size(1024, 768)

    # She notices the input box is nicely centered
    inputbox = selenium.find_element_by_id("id_new_item")
    assert inputbox.location["x"] + inputbox.size["width"] / 2 == pytest.approx(
        512, abs=10
    )

    # She starts a new list and sees the input is nicely
    # centered there too
    inputbox.send_keys("testing")
    inputbox.send_keys(Keys.ENTER)
    wait_for_row_in_list_table(selenium, "1: testing")
    inputbox = selenium.find_element_by_id("id_new_item")
    assert inputbox.location["x"] + inputbox.size["width"] / 2 == pytest.approx(
        512, abs=10
    )