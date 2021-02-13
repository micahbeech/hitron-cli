import argparse
import logging
from pathlib import Path
from router import RouterController
from router import Credential

DEFAULT_IP = '192.168.0.1'
DEFAULT_USERNAME = 'cusadmin'
DEFAULT_PASSWORD = 'password'

class UnknownCommandException(Exception):
    pass

def main():
    """
    The entrance point for interacting with the Hitron CODA-4589's GUI

    The purpose of this method is to handle command line arguments and
    execute the requested commands appropriately
    """

    parser = argparse.ArgumentParser(description='Manage Hitron CODA-4589 via web interface.')
    parser.add_argument('command', help='The command to execute. See ReadMe for list of supported commands')
    parser.add_argument('-c', '--config-file', default=f'{Path.home()}/routerCredentials.txt', help='Config file to read credentials from. Defaults to ~/routerCredentials.txt')
    parser.add_argument('-d', '--dry-run', action='store_true', help='Run the command without effect')
    parser.add_argument('--driver-path', default=f'{Path.home()}/chromedriver', help='Path to the chromedriver to use. Defaults to ~/chromedriver')
    parser.add_argument('-f', '--log-file', help='File to log output to. Defaults to standard error')
    parser.add_argument('-H', '--headless', action='store_true', help='Run in headless mode')
    parser.add_argument('-i', '--ip-address', help='IP address associated with the modem')
    parser.add_argument('-p', '--password', help='Password for login')
    parser.add_argument('-u', '--username', help='Username for login')

    args = parser.parse_args()

    ip = None
    username = None
    password = None

    try:
        # Initially attempt to read info from config file
        with open(args.config_file, 'r') as configFile:
            credentials = configFile.readlines()
            ip = credentials[0].strip()
            username = credentials[1].strip()
            password = credentials[2].strip()

    except:
        # If the config file couldn't be read or was poorly formatted,
        # Set the values to the defaults
        if ip is None:
            ip = DEFAULT_IP
        if username is None:
            username = DEFAULT_USERNAME
        if password is None:
            password = DEFAULT_PASSWORD
    
    # Override any config file or defaults with values given via command line
    if args.ip_address is not None:
        ip = args.ip_address
    if args.username is not None:
        username = args.username
    if args.password is not None:
        password = args.password

    # Extracting the rest of the values here if we want to do some modification later
    driverPath = args.driver_path
    headless = args.headless
    dryRun = args.dry_run
    logFile = args.log_file
    command = args.command

    creds = Credential(username, password)

    # Change the default logging level here if you want
    # May add a command line option to do so in the future
    logging.basicConfig(
        level=logging.INFO,
        format=('%(asctime)s: %(levelname)-4s [%(name)s] %(message)s'),
        filename=logFile
    )

    controller = RouterController(ip, driverPath, creds, headless)

    try:
        dispatchCommand(command, controller, dryRun)
    except UnknownCommandException:
        print(f'Unknown command {command}\n')
        parser.print_help()

def dispatchCommand(command, controller, dryRun):
    """
    Dispatcher for commands that can be entered

    Parameters
    ----------
    command : str
        The name of the command to be executed
    controller : RouterControler
        The controller object with which to execute the command
    dryRun : bool
        True if the command should be attempted but not executed
    
    Raises
    ------
    UnknownCommandException
        If the command is not recognized by the dispatcher
    """

    if command.lower() == 'restart':
        controller.restart(dryRun)
    else:
        raise UnknownCommandException()
