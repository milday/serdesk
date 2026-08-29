Project-local browser drivers
=============================

This folder stores WebDriver binaries so the app does not need to download
geckodriver/chromedriver from GitHub every time.

Included:
- windows/geckodriver.exe  (Windows 64-bit)
- linux/geckodriver        (Linux 64-bit)

Runtime caches (created automatically, not required in git):
- selenium-cache/   Selenium Manager downloads
- .wdm/             webdriver-manager downloads
- windows/chromedriver.exe or linux/chromedriver after the first Chrome run

You can also drop your own files here:
- geckodriver.exe / geckodriver
- chromedriver.exe / chromedriver

The app uses an already-installed Firefox or Chrome. If Firefox is missing,
it falls back to Chrome.
