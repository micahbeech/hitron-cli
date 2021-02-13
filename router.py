from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from webhelper import WebHelper
from webhelper import InteractionException

import logging

class Credential:
    """
    Stores credentials for login

    Attributes
    ----------
    username : str
        the username used for login
    password : str
        the password used for login
    """

    def __init__(self, username, password):
        """
        Parameters
        ----------
        username : str
            the username to be used for login
        password : str
            the password to be used for login
        """
        self.username = username
        self.password = password

class RouterController():
    """
    Used for interactions with the router/modem's GUI

    Attributes
    ----------
    ip : str
        the IP address to access the router/modem via, e.g. 192.168.0.1
    driverPath : string
        path to the installation of chromedriver with which to connect to the modem
    credentials : Credential
        the credentials used to log into the router/modem's GUI with
    headless : bool
        open the web interface in headless mode when set to True (default)

    Methods
    -------
    restart(dryRun=False)
        restarts the router/modem
    """

    def __init__(self, ip, driverPath, credentials, headless = True):
        """
        Parameters
        ----------
        ip : str
            the IP address to access the router/modem via, e.g. 192.168.0.1
        driverPath : string
            path to the installation of chromedriver with which to connect to the modem
        credentials : Credential
            the credentials used to log into the router/modem's GUI
        headless : bool
            open the web interface in headless mode when set to True (default)
        """

        logger = logging.getLogger('RouterController')

        logger.debug('Creating RouterController...')

        options = webdriver.ChromeOptions()

        if headless:
            # Generate options for operating in headless mode
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--disable-gpu")
            options.add_argument("--disable-extensions")
            options.add_experimental_option("useAutomationExtension", False)
            options.add_argument("--proxy-server='direct://'") 
            options.add_argument("--proxy-bypass-list=*")
            options.add_argument("--start-maximized")
            options.add_argument("--headless")

            logger.debug('Configured settings for headless mode')

        self.driverPath = driverPath
        self.driverCapabilities = options.to_capabilities()
        self.credentials = credentials
        self.rootUrl = 'http://' + ip

        logger.debug('Created RouterController')

        

    def __login(self, driver, logger):
        """ Login to the router/modem's GUI """

        usernameInput = WebHelper.safeFind(driver.find_element_by_id, 'user_login')
        logger.debug('Found username field')
        WebHelper.safeInteract(usernameInput.send_keys, self.credentials.username)
        logger.debug('Successfully entered username')

        passwordInput = WebHelper.safeFind(driver.find_element_by_id, 'user_password')
        logger.debug('Found password field')
        WebHelper.safeInteract(passwordInput.send_keys, self.credentials.password)
        logger.debug('Successfully entered password')
        WebHelper.safeInteract(passwordInput.send_keys, Keys.ENTER)
        logger.debug('Submitted credentials to server')

        # The login failure element is always on the page, just with display toggled
        # so we will always be able to find it, we just need to check if it is displayed
        loginFailure = WebHelper.safeFind(driver.find_element_by_id, 'Login_Failed', timeout=1)

        if loginFailure.is_displayed():
            raise InteractionException('Login failed. Please check your credentials and try again.')

    def __doRestart(self, driver, dryRun, logger):
        """ Restart the router/modem's GUI """

        admin = WebHelper.safeFind(driver.find_element_by_link_text, 'Admin')
        logger.debug('Found Admin tab')
        WebHelper.safeInteract(admin.click)
        logger.debug('Clicked Admin tab')

        deviceReset = WebHelper.safeFind(driver.find_element_by_link_text, 'Device Reset')
        logger.debug('Found Device Reset tab')
        WebHelper.safeInteract(deviceReset.click)
        logger.debug('Clicked Device Reset tab')

        reboot = WebHelper.safeFind(driver.find_element_by_id, 'reboot')
        logger.debug('Found Reboot button')
        WebHelper.safeInteract(reboot.click)
        logger.debug('Clicked Reboot button')

        confirmation = WebHelper.safeSwitch(driver)
        logger.debug('Switched to reboot confirmation alert')

        if dryRun:
            logger.info('Finished dry run. Could have successfully rebooted modem.')
        else:
            WebHelper.safeInteract(confirmation.accept)
            logger.debug('Confirmed reboot. The router/modem should be restarting now')


    def restart(self, dryRun=False):
        """
        Restarts the router/modem

        If argument `dryRun` is passed in, the operation is attempted
        but not actually executed.

        Parameters
        ----------
        dryRun : bool
            Whether or not to actually restart the router/modem (default is False)
        """

        loginLogger = logging.getLogger('RouterController.Login')
        restartLogger = logging.getLogger('RouterController.Restart')

        driver = webdriver.Chrome(self.driverPath, desired_capabilities=self.driverCapabilities)
        driver.get(self.rootUrl)
        restartLogger.debug('Opened %s', self.rootUrl)

        try:
            self.__login(driver, loginLogger)
        except InteractionException as e:
            # Sometimes the page navigates past the login page before the login failed element is found
            # so if that is the reason for failure, we still logged in, just ignore the exception
            if 'Login_Failed' not in e.message:
                loginLogger.error(e.message)
                driver.quit()
                return

        try:
            self.__doRestart(driver, dryRun, restartLogger)
        except InteractionException as e:
            restartLogger.error(e.message)
        finally:
            driver.quit()

