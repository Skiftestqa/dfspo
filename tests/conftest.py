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
    So we can easily pluck the value out of it and store it in 'config.[NAME]'.
    """

    # In the beginning of our fixture we grab the command-line
    # values and store them in an instance of config.py, which we'll use throughout the fixture.
    parser.addoption("--baseurl",
                     action="store",
                     default="https://www.fanduel.com",
                     help="base usrl for application under test")
    parser.addoption("--browser",
                     action="store",
                     default="firefox",
                     help="the name of the browser you want to test with")
    parser.addoption("--host",
                     action="store",
                     default="saucelabs",
                     help="where to run tests localhost ot saucelabs")
    parser.addoption("--browserversion",
                     action="store",
                     default="10.0",
                     help="the browser version you want to test with")
    parser.addoption("--platform",
                     action="store",
                     default="Windows 7",
                     help="the operating system to run your tests on(saucelabs only)")


@pytest.fixture
def driver(request):
    """Return Webdriver instance

    request is a parameter made available to fixtures.
    It enables access to many things during a test run.
    """

    config.baseurl = request.config.getoption("--baseurl")
    config.browser = request.config.getoption("--browser").lower()
    config.host = request.config.getoption("--host").lower()
    config.browserversion = request.config.getoption("--browserversion").lower()
    config.platform = request.config.getoption("--platform").lower()

    # saucelab test run setup
    if config.host == "saucelabs":
        _desired_caps = {}
        _desired_caps["browserName"] = config.browser
        _desired_caps["version"] = config.browserversion
        _desired_caps["platform"] = config.platform
        _credentials = os.environ["SAUCE_USERNAME"] + ":" + os.environ["SAUCE_ACCESS_KEY"]
        _url = "http://" + _credentials + "@ondemand.saucelabs.com:80/wd/hub"
        driver_ = webdriver.Remote(_url, _desired_caps)

    # if command-line value set to localhost check browser value to determine which browser to launch locally
    if config.host == "localhost":
        if config.browser == "firefox": # create webdriver instance of Firefox
            driver_ = webdriver.Firefox()
            driver_.maximize_window()
        elif config.browser == "chrome": # create webdriver instance of Chrome
            if platform.system() == "Darwin":  # select proper path to chromedriver based on OS
                chromedriver = os.getcwd() + "/../vendor/chromedriver"
            elif platform.system() == "Windows":
                chromedriver = os.getcwd() + "/../vendor/chromedriver.exe"
            options = Options()
            options.add_argument("--start-maximized") # start chrome window maximized
            driver_ = webdriver.Chrome(chromedriver, chrome_options=options)
        elif config.browser == "ie": # create webdriver instance of Internet Explorer
            driver_ = webdriver.Ie()
            driver_.maximize_window()
        else:
            raise Exception("This browser is not supported at the moment")

        def quit():
            driver_.quit()

        request.addfinalizer(quit)
        return driver_
