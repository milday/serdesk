# ServiceDesk Ticket Automation

This tool automates the process of creating tickets on the ServiceDesk portal (https://servicedesk.adira.co.id/HEAT/).

## Features

- Create and manage tickets in an Excel file
- Automatically submit tickets to the ServiceDesk portal
- Track ticket numbers and results
- User-friendly GUI interface

## Requirements

- Python 3.7 or higher
- Chrome browser installed
- Internet access to the ServiceDesk portal

## Quick Start

The easiest way to get started is to run the included batch files:

1. Run `run_servicedesk.bat` to start the application
2. If you encounter any issues, run `run_diagnostic.bat` to diagnose problems

## Manual Installation

1. Install the required Python packages:

```
pip install -r requirements.txt
```

2. Create a `.env` file with your ServiceDesk credentials:

```
SERVICEDESK_USERNAME=your_username
SERVICEDESK_PASSWORD=your_password
```

## Usage

### GUI Application

The recommended way to use this tool is through the GUI application:

```
python servicedesk_gui.py
```

The GUI application has three tabs:

1. **Setup**: Configure your ServiceDesk credentials and Excel file settings
2. **Tickets**: Manage your tickets (add, edit, delete)
3. **Results**: View the results of the automation

### Step-by-Step Guide

1. Launch the GUI application
2. In the Setup tab, enter your ServiceDesk credentials
3. Create or edit tickets in the Tickets tab
4. Click "Run Automation" in the Setup tab to start the process
5. View the results in the Results tab

### Manual Usage

You can also run the automation script directly:

```
python servicedesk_automation.py
```

This will prompt you for your credentials and process all tickets in the Excel file.

## Excel File Format

The Excel file should have the following columns:

- **Subject**: The subject of the ticket
- **Description**: The description of the ticket ("Mohon dilakukan" will be automatically added if not present)
- **Ticket Number**: This column will be filled automatically after the ticket is created

## Troubleshooting

If you encounter issues, follow these steps:

1. Run `run_diagnostic.bat` and select the appropriate diagnostic option
2. Check your network connection to the ServiceDesk server
3. Verify your Chrome installation is working correctly
4. Ensure your credentials are correct in the `.env` file or enter them in the GUI

### Common Issues

- **Login Failed**: This is usually due to incorrect credentials or network connectivity issues. Check your username and password are correct.
- **Browser Initialization Failed**: Make sure Chrome is installed and up to date.
- **Network Connection Error**: Verify you can access the ServiceDesk portal in your regular browser.

### Advanced Troubleshooting

If the basic troubleshooting doesn't resolve your issue:

1. Check for screenshots created during login attempts (`login_page.png`, `login_error.png`, or `login_timeout.png`)
2. Look for any error messages in the console output
3. Try running the script with visible browser mode (default in the GUI)
4. If your network requires a proxy, set it in the `.env` file or GUI

## License

This project is for personal use only.

## Support

If you continue to experience issues, please check the logs and screenshots to help identify the root cause.

# XPath Recorder for ServiceDesk Automation

This tool helps troubleshoot ServiceDesk automation by recording user interactions, including what you type and which XPath elements you select. It creates a detailed log that can be used to update the main automation script.

## Features

- Records clicks on elements and captures their XPath
- Records input text in forms
- Captures screenshots of each interaction
- Saves HTML page source for debugging
- Provides an element explorer to help find elements on the page
- Generates automatic XPaths for clicked elements
- Logs all interactions with timestamps

## Requirements

The same dependencies as the main ServiceDesk automation script:
- Python 3.6+
- Selenium
- Firefox browser
- webdriver-manager

## How to Use

1. Run the recorder script:
   ```
   python xpath_recorder.py
   ```

2. Enter the ServiceDesk URL when prompted (typically `http://servicedesk.adira.co.id/HEAT/`)

3. The script will open a Firefox browser and navigate to the URL

4. Use the interactive menu to record different types of interactions:
   - `click` - Record clicking on elements
   - `input` - Record input into form fields
   - `explore` - Find and inspect elements on the page
   - `navigate` - Navigate to a different URL
   - `screenshot` - Take a manual screenshot
   - `exit` - Close the recorder

5. After recording interactions, review the generated JSON file and screenshots in the `screenshots` directory

## Example Workflow for Troubleshooting

1. Run the recorder and navigate to the ServiceDesk login page
2. Use `input` to record entering your username and password
3. Use `click` to record clicking the login button
4. When the role selection page appears, use `explore` to find the correct role element
5. Use `click` to record clicking the role element
6. Check the generated logs to find the correct XPath for the role element
7. Update the main automation script with the correct XPath

## Output Files

- `interaction_log_YYYYMMDD_HHMMSS.json` - Detailed log of all interactions
- `screenshots/` directory - Contains screenshots and HTML source files for each interaction

## Using the Results

The recorder generates detailed logs with XPaths and other element information. Use these to update the main ServiceDesk automation script with correct element selectors.

Example:
1. Find the XPath for the role selection element in the log
2. Update the `select_role()` method in `servicedesk_automation.py` with the correct XPath
