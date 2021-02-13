import time

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import NoAlertPresentException

class InteractionException(Exception):
    """
    An exception to be raised when an interaction with a web page fails

    Attributes
    ----------
    message : str
        The message detailing why the exception was raised
    """
    
    def __init__(self, message):
        """
        Parameters
        ----------
        message : str
            The message detailing why the exception was raised
        """
        self.message = message

class WebHelper():
    """
    Used to safely interact with a web interface

    Methods
    -------
    @staticmethod
    safeFind(selector, identifier, delay=0.1, timeout=10)
        Attempt to find an element within a web page

    @staticmethod
    safeInteract(action, *args, delay=0.1, timeout=10)
        Attempt to perform an action on a web page

    @staticmethod
    safeSwitch(driver, delay=0.1, timeout=10)
        Attempt to switch to a presented alert on a web page
    """

    @staticmethod
    def safeFind(selector, identifier, delay=0.1, timeout=10):
        """
        Attempt to find an element within a web page

        Parameters
        ----------
        selector : method
            The method used to find the element on the screen
        identifier : str
            The identifier with which `selector` will attempt to find the element
        delay : float
            How many seconds to wait between attempts (default 0.1)
        timeout : float
            How many seconds to attempt to find the element before giving up (default 10)

        Returns
        -------
        selenium.webdriver.remote.webelement.WebElement
            The element found on the screen

        Raises
        ------
        InteractionException
            If the element cannot be found
        """

        message = f'Could not find element \'{identifier}\' within {timeout} seconds.'
        return WebHelper.__doSafe(selector, [identifier], NoSuchElementException, message, delay, timeout)

    @staticmethod
    def safeInteract(action, *args, delay=0.1, timeout=10):
        """
        Attempt to perform an action on a web page

        Parameters
        ----------
        action : method
            The action to perform
        args : *args
            The arguments to perform `action` with
        delay : float
            How many seconds to wait between attempts (default 0.1)
        timeout : float
            How many seconds to attempt to perform the action before giving up (default 10)

        Raises
        ------
        InteractionException
            If the action cannot be performed
        """

        message = f'Could not perform {action} within {timeout} seconds.'
        WebHelper.__doSafe(action, args, ElementNotInteractableException, message, delay, timeout)

    @staticmethod
    def safeSwitch(driver, delay=0.1, timeout=10):
        """
        Attempt to switch to a presented alert on a web page

        Parameters
        ----------
        driver : selenium.webdriver.chrome.webdriver.WebDriver
            The webdriver on which the alert is being displayed
        delay : float
            How many seconds to wait between attempts (default 0.1)
        timeout : float
            How many seconds to attempt to switch to the alert before giving up (default 10)

        Returns
        -------
        selenium.webdriver.common.alert.Alert
            The alert that was switched to

        Raises
        ------
        InteractionException
            If the alert cannot be switched to
        """

        message = f'Could not switch to alert within {timeout} seconds.'
        return WebHelper.__doSafe(driver.switch_to.alert, None, NoAlertPresentException, message, delay, timeout)

    @staticmethod
    def __doSafe(action, args, exception, message, delay, timeout):
        """
        Attempt to safely interact with a web page

        Parameters
        ----------
        action : method
            The action to perform within the web page
        args : *args
            The arguments to be passed to the action
        exception : selenium.common.exceptions.<Exception Type>
            The type of exception to catch while interacting with the web page
        message : str
            The message to propogate upon failure
        delay : float
            How many seconds to wait between attempts (default 0.1)
        timeout : float
            How many seconds to attempt to switch to the alert before giving up (default 10)

        Returns
        -------
        any
            The element that was interacted with

        Raises
        ------
        InteractionException
            If the interaction failed
        """

        # The web page seems to freeze if we don't take breaks
        # so start with an initial pause to avoid this issue
        time.sleep(1)

        start = time.time()
        now = time.time()

        while now < start + timeout:
            try:
                # No arguments indicate that action is the element we want
                if args is None:
                    return action

                return action(*args)

            except exception:
                time.sleep(delay)
            
            now = time.time()

        raise InteractionException(message)

