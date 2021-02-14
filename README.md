# Hitron CLI

This tool is intended for use with the Hitron CODA-4589 Cable Modem Router. The tool interacts with the modem via its web GUI, accessed using its internal IP address.

The idea of the tool is to be able to automate tasks that you might not be able to otherwise. I use it to regularly reboot my modem every 24 hours.

On this page:
- [Prerequisites](#prerequisites)
- [Setup](#setup)
    - [Python Version](#python-version)
    - [Credentials](#credentials)
    - [Logging](#logging)
- [Usage](#usage)
    - [Positional Arguments](#positional-arguments)
    - [Optional Arguments](#optional-arguments)
- [Examples](#examples)

&nbsp;

## Prerequisites

- Hitron CODA-4589 Cable Modem Router
    - If you have a different model, you can give the code a try, but I haven't tested it. YMMV
- Python 3.7+
    - I believe this could work on as low as Python 3.4, but again, the tool has only been tested with 3.7
- Selenium
    - The tool uses Selenium for web interaction
    - If you don't have Selenium installed, install it using `pip install -U Selenium`. See [https://pythonspot.com/selenium-install/](https://pythonspot.com/selenium-install/) for more details.
- Google Chrome and Chromedriver
    - The tool uses Chromedriver as the webdriver for Selenium. To use this, you must have both Google Chrome (the browser) and a version of chromedriver installed. 
    - You can download Chromedriver from [this](https://chromedriver.chromium.org) website. Make sure to download the correct version for Chrome and your OS.
    - Place the driver in your home directory (the tool looks for the file ~/chromedriver). If you prefer, there is an option to specify a different path at runtime, discussed in [Usage](#optional-arguments).

&nbsp;

## Setup

### Python Version
The tool should be useable out of the box, although depending on what version of Python you use, you may have to edit the first line of the `hitron` wrapper script to point to a different version of Python. Currently, the tool runs Python using
```
#!/Library/Frameworks/Python.framework/Versions/3.7/bin/python3
```
For example, a common alternative might be
```
#!/usr/bin/python
```

### Credentials
To make it easier to provide the IP address and credentials for login to the modem, these details can be provided in a configuration file that is read by the tool. The file should contain three lines, in the following format:
```
<IP address>
<Username>
<Password>
```
By default, the tool looks for the file `~/.routerCredentials`, but an alternate file can be specified using the `-c` option described below.

If no credential file is provided, the tool uses the following default values:
Item | Default
--- | ---
IP address | 192.168.0.1
Username | cusadmin
Password | password

### Logging
By default, the tool logs at INFO level. If you wish to change this (e.g. to DEBUG), modify
```
logging.basicConfig(
    ...
    level=logging.INFO,
    ...
)
```
in `app.py` to
```
logging.basicConfig(
    ...
    level=logging.<NEW LEVEL>,
    ...
)
```
where `<NEW LEVEL>` is one of `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`. I may add an option to set the log level at runtime in the future.

By default, the tool logs to standard error, but can log to a file specified using the `-f` option, discussed in [Optional Arguments](#optional-arguments).

&nbsp;

## Usage

Run the tool by executing
```
./hitron [OPTIONS] <command>
```

### Positional Arguments
- command
    - The command you want to execute. Currently, the supported commands are:

    Command | Effect
    --- | ---
    login | Logs in to the modem/router's GUI. This is useful to test if you have your credentials set up correctly before executing any meaningful commands
    restart | Logs in to the modem/router's GUI and issues a reboot

### Optional Arguments

Option | Effect
--- | ---
-h, --help | Display the help message
-c CONFIG_FILE, --config-file CONFIG_FILE | Specify the path to a config file to read details for the modem from. The file should be of the format described in [Credentials](#credentials).
-d, --dry-run | If the -d option is specified, the command given will be run but not executed with any effect. This option only has an effect with commands that alter the modem's state or settings in some way.
--driver-path DRIVER_PATH | Specify the path to an installation of Chromedriver to use
-f LOG_FILE, --log-file LOG_FILE | Specify the path to a file for log output
-H, --headless | If the -h option is specified, the tool will run the command without launching the GUI itself on the user's screen. This is beneficial when using the tool in a script/alternate program
-i IP_ADDRESS, --ip-address IP_ADDRESS | Specify the IP address with which to connect to the modem. Use of the -i option overrides any IP address provided by a configuration file
-p PASSWORD, --password PASSWORD | Specify the password with which to login to the modem's GUI. Use of the -p option overrides any password provided by a configuration file
-u USERNAME, --username USERNAME | Specify the username with which to login to the modem's GUI. Use of the -u option overrides any username provided by a configuration file

&nbsp;

## Examples
```
./hitron restart
```
The tool will read credentials from `~/.routerCredentials` and use these to log in to the GUI, which will open in a Chrome window on your screen using the driver found at `~/chromedriver`. It will select the option to reboot the modem. Log output is printed to standard error.

```
./hitron restart -H -d -c creds.txt -f hitron.log -u sharon
```
The tool will use IP address and password from `creds.txt` and username `sharon` to log into the GUI, which will run without opening on the screen. It will do a dry restart, and log its results to `hitron.log`.

&nbsp;

## Scheduling
You may which to run the `restart` command on a schedule in order to keep your modem running well. I did this using a CRON job in the following format:
```
0 4 * * * /path/to/hitron restart
```
