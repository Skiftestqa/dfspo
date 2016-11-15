"""In pytest conftest.py file is central file that is automatically
found by pytest and used during test execution. It's used for
global setup and teardown. And also for enabling command line
arguments using helper method pytest_addoption(parser).

"""



import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from tests import config
import os
import platform


def pytest_addoption(parser):
    """Helper method available in pytest.

    It enables to specify a custom runtime flag and set a sensible default.
    This value gets passed into the 'request' variable that is available in our test fixture.
    So we can easily pluck the value out of it and store it in 'config.baseurl'.
    """
    parser.addoption("--baseurl",
                     action="store",
                     default="https://www.fanduel.com",
                     help="base usrl for application under test")
    parser.addoption("--browser",
                     action="store",
                     default="firefox",
                     help="the name of the browser you want to test with")


@pytest.fixture
def driver(request):
    """Return Webdriver instance

    request is a parameter made available to fixtures.
    It enables access to many things during a test run.
    """

    config.baseurl = request.config.getoption("--baseurl")
    config.browser = request.config.getoption("--browser").lower()
    if config.browser == "firefox":
        driver_ = webdriver.Firefox()
        driver_.maximize_window()
    elif config.browser == "chrome":
        if platform.system() == "Darwin":  # find out that OS that we run test on to select proper chromedriver
            chromedriver = os.getcwd() + "/../vendor/chromedriver"
        elif platform.system() == "Windows":
            chromedriver = os.getcwd() + "/../vendor/chromedriver.exe"
        options = Options()
        options.add_argument("--start-maximized")
        driver_ = webdriver.Chrome(chromedriver, chrome_options=options)
    elif config.browser == "ie":
        driver_ = webdriver.Ie()
        driver_.maximize_window()
    else:
        raise Exception("This browser is not supported at the moment")

    def quit():
        driver_.quit()

    request.addfinalizer(quit)
    return driver_
