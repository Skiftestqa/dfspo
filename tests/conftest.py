import pytest
from selenium import webdriver
from dfspo.constants import dfs_constants
from dfspo.tests import config


def pytest_addoption(parser):
    parser.addoption("--baseurl",
                     action="store",
                     default="https://www.fanduel.com/",
                     help="base usrl for application under test")


@pytest.fixture
def driver(request):
    """Return Webdriver instance"""

    config.baseurl = request.config.getoption("--baseurl")
    if dfs_constants['Browser'].lower() == "firefox":
        driver_ = webdriver.Firefox()
        driver_.maximize_window()
    elif dfs_constants['Browser'].lower() == "chrome":
        driver_ = webdriver.Chrome()
        driver_.maximize_window()
    elif dfs_constants['Browser'].lower() == "ie":
        driver_ = webdriver.Ie()
        driver_.maximize_window()
    else:
        raise Exception("This browser is not supported at the moment")

    def quit():
        driver_.quit()

    request.addfinalizer(quit)
    return driver_
