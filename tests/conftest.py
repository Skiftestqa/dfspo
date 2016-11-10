import pytest
from selenium import webdriver
from constants import dfs_constants


@pytest.fixture
def driver(request):
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
