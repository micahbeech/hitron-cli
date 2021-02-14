# Hitron CLI

This tool is intended for use with the Hitron CODA-4589 Cable Modem Router. The tool interacts with the modem via its web GUI, accessed using its internal IP address.

The idea of the tool is to be able to automate tasks that you might not be able to otherwise. I use it to regularly reboot my modem every 24 hours.

On this page:
- [Prerequisites](#prerequisites)
- [Setup](#setup)
    - [Python Version](#python-version)
    - [Credentials](#credentials)
- [Usage](#usage)
    - [Positional Arguments](#positional-arguments)
    - [Optional Arguments](#optional-arguments)
- [Examples](#examples)

## Prerequisites

- Python 3.7+
    - I believe this could work on as low as Python 3.4, but I haven't tested it
- Selenium
    - The tool uses Selenium for web interaction
    - If you don't have it installed, install it using `pip install -U Selenium`
- Google Chrome and Chromedriver
    - The tool uses Chromedriver as the webdriver for Selenium. To use this, you must have both Google Chrome (the browser) and a version of webdriver installed. 
    - You can download Chromedriver from [this](https://chromedriver.chromium.org) website. Make sure to download the correct version for Chrome and your OS.
    - Place the driver in your home directory (the tool looks for the file ~/chromedriver). There is an option to specify a different path, discussed in [Usage](#optional-arguments).

## Setup

### Python Version
The tool should be useable out of the box, although depending on what version of Python you use, you may have to edit the first line of the `hitron` convenience script to point to a different location. Currently, the tool runs Python using
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

## Usage

### Positional Arguments
- command
    - The command you want to execute. Currently, the supported commands are:

    Command | Effect
    --- | ---
    restart | Restarts the modem/router.

### Optional Arguments

Option | Effect
--- | ---
-h, --help | Display the help message
-c CONFIG_FILE, --config-file CONFIG_FILE | Specify the path to a config file to read details for the modem from. The file should be of the format described in [Credentials](#credentials).
-d, --dry-run | If the -d option is specified, the command given will be run but not executed with any effect
--driver-path DRIVER_PATH | Path to an installation of Chromedriver to use
-f LOG_FILE, --log-file LOG_FILE | Specify the path to a file for log output. By default, the tool logs to standard error
-H, --headless | If the -h option is specified, the tool will run the command without launching the GUI itself on the user's screen. This is beneficial when using the tool in a script/alternate program.
-i IP_ADDRESS, --ip-address IP_ADDRESS | Specify the IP address with which to connect to the modem. Use of the -i option overrides any IP address provided by a configuration file.
-p PASSWORD, --password PASSWORD | Specify the password with which to login to the modem's GUI. Use of the -p option overrides any password provided by a configuration file.
-u USERNAME, --username USERNAME | Specify the username with which to login to the modem's GUI. Use of the -u option overrides any username provided by a configuration file.

## Examples
```
./hitron restart
```
The tool will read credentials from `~/.routerCredentials` and use these to log in to the GUI, which will open in a Chrome window on your screen using the driver found at `~/chromedriver`. It will select the option to reboot the modem. Log output is printed to standard error.

```
./hitron restart -H -d -c creds.txt -f hitron.log -u sharon
```
The tool will use IP address and password from `creds.txt` and username sharon to log into the GUI, which will run without opening on the screen. It will do a dry restart, and log its results to `hitron.log`.

## Scheduling
You may which to run the `restart` command on a schedule in order to keep your modem running well. I did this using a CRON job in the following format:
```
0 4 * * * /path/to/hitron restart
```
