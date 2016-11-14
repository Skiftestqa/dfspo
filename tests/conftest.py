import pytest
from selenium import webdriver
from tests import config
import os
import platform


def pytest_addoption(parser):
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
    """Return Webdriver instance"""

    config.baseurl = request.config.getoption("--baseurl")
    config.browser = request.config.getoption("--browser").lower()
    if config.browser == "firefox":
        driver_ = webdriver.Firefox()
        driver_.maximize_window()
    elif config.browser == "chrome":
        if platform.system() == "Darwin":
            chromedriver = os.getcwd() + "/vendor/chromedriver"
        elif platform.system() == "Windows":
            chromedriver = os.getcwd() + "/vendor/chromedriver.exe"
        driver_ = webdriver.Chrome(chromedriver)
        driver_.maximize_window()
    elif config.browser == "ie":
        driver_ = webdriver.Ie()
        driver_.maximize_window()
    else:
        raise Exception("This browser is not supported at the moment")

    def quit():
        driver_.quit()

    request.addfinalizer(quit)
    return driver_
