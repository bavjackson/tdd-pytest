import pytest
from selenium import webdriver


@pytest.fixture()
def browser():
    driver = webdriver.Firefox()
    yield driver
    driver.quit()


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass