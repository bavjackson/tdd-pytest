import pytest
from selenium import webdriver
from selenium.webdriver.support.events import EventFiringWebDriver


@pytest.fixture()
def browser():
    driver = webdriver.Firefox()
    yield driver
    driver.quit()


@pytest.fixture
def driver_factory(request, driver_class, driver_kwargs):
    """
    Returns a factory function that returns a WebDriver instance when called,
    based on options and capabilities
    """
    request.node.drivers = []

    def factory():
        driver = driver_class(**driver_kwargs)
        request.node.drivers.append(driver)

        event_listener = request.config.getoption("event_listener")
        if event_listener is not None:
            # Import the specified event listener and wrap the driver instance
            mod_name, class_name = event_listener.rsplit(".", 1)
            mod = __import__(mod_name, fromlist=[class_name])
            event_listener = getattr(mod, class_name)
            if not isinstance(driver, EventFiringWebDriver):
                driver = EventFiringWebDriver(driver, event_listener())

        return driver

    yield factory

    for driver in request.node.drivers:
        driver.quit()


@pytest.fixture
def driver(driver_factory):
    return driver_factory()


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass