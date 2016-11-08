"""Base module.

Defines functions wrapping frequently used selenium calls in
own design class methods.

"""
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from abc import abstractmethod
from dfspo.constants import LocatorMode


class BasePage(object):
    """Page class that all page models can inherit from."""

    def __init__(self, driver):
        """Constructor.

        Creates instance of page passing it Selenium driver object
        and runs _verify_page() function to make sure that correct
        page gets loaded.

        """

        self.driver = driver
        self._verify_page()

    @abstractmethod
    def _verify_page(self):
        """This method verifies that we are on correct page."""

        return

    @property
    def footer(self):
        """Regions define functionality available through all page objects."""

        from .footer import Footer
        return Footer(self.driver)

    @property
    def nav_menu(self):
        """Navigation Menu region available to all page objects"""

        from nav_menu import NavMenu
        return NavMenu(self.driver)

    def wait_for_element_visibility(self, wait_time, locator_mode, locator):
        """Returns element after it becomes visible"""

        element = None
        if locator_mode == LocatorMode.ID:
            element = WebDriverWait(self.driver, wait_time). \
                until(EC.visibility_of_element_located((By.ID, locator)))
        elif locator_mode == LocatorMode.NAME:
            element = WebDriverWait(self.driver, wait_time). \
                until(EC.visibility_of_element_located((By.NAME, locator)))
        elif locator_mode == LocatorMode.XPATH:
            element = WebDriverWait(self.driver, wait_time). \
                until(EC.visibility_of_element_located((By.XPATH, locator)))
        elif locator_mode == LocatorMode.CSS_SELECTOR:
            element = WebDriverWait(self.driver, wait_time). \
                until(EC.visibility_of_element_located((By.CSS_SELECTOR, locator)))
        else:
            raise Exception("Unsupported locator strategy")
        return element

    def wait_until_element_clickable(self, wait_time, locator_mode, locator):
        """Returns element after it becomes clickable"""

        element = None
        if locator_mode == LocatorMode.ID:
            element = WebDriverWait(self.driver, wait_time). \
                until(EC.element_to_be_clickable((By.ID, locator)))
        elif locator_mode == LocatorMode.NAME:
            element = WebDriverWait(self.driver, wait_time). \
                until(EC.element_to_be_clickable((By.NAME, locator)))
        elif locator_mode == LocatorMode.XPATH:
            element = WebDriverWait(self.driver, wait_time). \
                until(EC.element_to_be_clickable((By.XPATH, locator)))
        elif locator_mode == LocatorMode.CSS_SELECTOR:
            element = WebDriverWait(self.driver, wait_time). \
                until(EC.element_to_be_clickable((By.CSS_SELECTOR, locator)))
        else:
            raise Exception("Unsupported location strategy")
        return element

    def find_element(self, locator_mode, locator):
        """Returns element based on choosen locator mode and locator"""

        element = None
        if locator_mode == LocatorMode.ID:
            element = self.driver.find_element_by_id(locator)
        elif locator_mode == LocatorMode.NAME:
            element = self.driver.find_element_by_name(locator)
        elif locator_mode == LocatorMode.XPATH:
            element = self.driver.find_element_by_xpath(locator)
        elif locator_mode == LocatorMode.CSS_SELECTOR:
            element = self.driver.find_element_by_css_selector(locator)
        else:
            raise Exception("Unsupported location strategy")
        return element

    def fill_out_field(self, locator_mode, locator, text):
        """Clears and fills out a field"""

        self.find_element(locator_mode, locator).clear()
        self.find_element(locator_mode, locator).send_keys(text)

    def click(self, wait_time, locator_mode, locator):
        """Clicks element once it gets loaded"""

        #pylint: disable=maybe-no-member
        self.wait_until_element_clickable(wait_time, locator_mode, locator).click()

    def switch_to_window(self, w_handle):
        """Switches to window with provided window handle"""

        self.driver.switch_to.window(w_handle)


class IncorrectPageException(Exception):
    """This exception is raised when we trying to instantiate the wrong page."""

    pass
