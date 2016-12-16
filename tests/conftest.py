"""In pytest conftest.py file is central file that is automatically
found by pytest and used during test execution. It's used for
global setup and teardown. And also for enabling command line
arguments using helper method pytest_addoption(parser).

"""

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from dfspo.tests import config
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
                     default="chrome",
                     help="the name of the browser you want to test with")
    parser.addoption("--host",
                     action="store",
                     default="saucelabs",
                     help="where to run tests localhost ot saucelabs")
    parser.addoption("--browserversion",
                     action="store",
                     default="54",
                     help="the browser version you want to test with")
    parser.addoption("--platform",
                     action="store",
                     default="Darwin",
                     help="the operating system to run your tests on(saucelabs only)")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Helper method.

    Used to grab the outcome of a test as it's running
    and append the result to a node in the request object
    that we're using in our fixture.
    """
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    result = outcome.get_result()
    # pass result of test to saucelab
    setattr(item, "result_" + result.when, result)
    # for pytest-html report extras
    extra = getattr(result, 'extra', [])
    if result.when == 'call':
        # always add url to report
        extra.append(pytest_html.extras.url('http://www.example.com/'))
        xfail = hasattr(result, 'wasxfail')
        if (result.skipped and xfail) or (result.failed and not xfail):
            # only add additional html on failure
            extra.append(pytest_html.extras.html('<div>Additional HTML</div>'))
        result.extra = extra


@pytest.fixture()
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
        _desired_caps = {}  # Desired Capabilities object which is passed to Sauce Labs
        _desired_caps["browserName"] = config.browser
        _desired_caps["version"] = config.browserversion
        _desired_caps["platform"] = config.platform
        _desired_caps["name"] = request.cls.__name__ + "." + request.function.__name__  # pass test name to SauceLabs
        _credentials = os.environ["SAUCE_USERNAME"] + ":" + os.environ["SAUCE_ACCESS_KEY"]
        _url = "http://" + _credentials + "@ondemand.saucelabs.com:80/wd/hub"
        driver_ = webdriver.Remote(_url, _desired_caps)  # connect to Sauce Labs using Selenium Remote

    # if command-line value set to localhost check browser value to determine which browser to launch locally
    if config.host == "localhost":
        if config.browser == "firefox":  # create webdriver instance of Firefox
            driver_ = webdriver.Firefox()
            driver_.maximize_window()
        elif config.browser == "chrome":  # create webdriver instance of Chrome
            if platform.system() == "Darwin":  # locate chromedriver if test run on OS X
                chromedriver = os.getcwd() + "/../vendor/chromedriver"
            elif platform.system() == "Windows":  # locate chromedriver if test run on Windows
                chromedriver = os.getcwd() + "/../vendor/chromedriver.exe"
            options = Options()
            options.add_argument("--start-maximized")  # start chrome window maximized
            driver_ = webdriver.Chrome(chromedriver, chrome_options=options)
        elif config.browser == "ie32":  # create webdriver instance of Internet Explorer
            iedriver = os.getcwd() + "/../vendor/IEDriverServer32.exe"
            driver_ = webdriver.Ie(iedriver)
            driver_.maximize_window()
        elif config.browser == "ie64":
            iedriver = os.getcwd() + "/../vendor/IEDriverServer64.exe"
            driver_ = webdriver.Ie(iedriver)
            driver_.maximize_window()
        elif config.browser == "safari":
            driver_ = webdriver.Safari(quiet=True)
            driver_.maximize_window()
        else:
            raise Exception("This browser is not supported at the moment")

        def quit():
            try:
                if config.host == "saucelabs":
                    if request.node.result_call.failed:
                        driver_.execute_script("sauce:job-result=failed")  # communicate to Sauce what outcome was
                        # output URL of the job to the console
                        print "http://saucelabs.com/beta/tests/" + driver_.session_id
                    elif request.node.result_call.passed:
                        driver_.execute_script("sauce:job_result=passed")
            finally:
                driver_.quit()

        request.addfinalizer(quit)
        return driver_
