import os
import time
import openpyxl
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.ui import Select
import sys

class ServiceDeskAutomation:
    def __init__(self):
        self.url = "https://servicedesk.adira.co.id/HEAT/"
        self.driver = None
        self.browser_type = "firefox"  # Default to Firefox
        self.location = ""
        
    def setup_driver(self, headless=False):
        """Initialize the WebDriver"""
        try:
            print(f"Setting up {self.browser_type.capitalize()} WebDriver...")
            
            if self.browser_type == "firefox":
                return self._setup_firefox_driver(headless)
            else:
                return self._setup_chrome_driver(headless)
                
        except Exception as e:
            print(f"Error in WebDriver setup: {str(e)}")
            return False
            
    def _setup_firefox_driver(self, headless=False):
        """Initialize Firefox WebDriver"""
        try:
            options = FirefoxOptions()
            
            if headless:
                options.add_argument("--headless")
            
            # Try to use webdriver-manager
            try:
                from webdriver_manager.firefox import GeckoDriverManager
                service = FirefoxService(GeckoDriverManager().install())
                self.driver = webdriver.Firefox(service=service, options=options)
                print("✅ Firefox WebDriver initialized!")
                return True
            except Exception as e:
                print(f"Firefox setup failed: {str(e)}")
                return False
        
        except Exception as e:
            print(f"Firefox setup error: {str(e)}")
            return False
            
    def _setup_chrome_driver(self, headless=False):
        """Initialize Chrome WebDriver"""
        try:
            options = ChromeOptions()
            
            if headless:
                options.add_argument("--headless")
            
            # Try to use webdriver-manager
            try:
                from webdriver_manager.chrome import ChromeDriverManager
                service = ChromeService(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=options)
                print("✅ Chrome WebDriver initialized!")
                return True
            except Exception as e:
                print(f"Chrome setup failed: {str(e)}")
                return False
        
        except Exception as e:
            print(f"Chrome setup error: {str(e)}")
            return False
    
    def login(self, username, password):
        """Login to ServiceDesk"""
        try:
            print("Starting login process...")
            
            if not self.driver:
                print("❌ WebDriver not initialized")
                return False
            
            # Navigate to login page
            print("Navigating to login page...")
            self.driver.get(self.url)
            time.sleep(5)
            
            # Find and fill username
            try:
                username_field = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.ID, "UserName"))
                )
                username_field.clear()
                username_field.send_keys(username)
                print("✅ Username entered")
            except Exception as e:
                print(f"❌ Could not find username field: {str(e)}")
                return False
            
            # Find and fill password
            try:
                password_field = self.driver.find_element(By.ID, "Password")
                password_field.clear()
                password_field.send_keys(password)
                print("✅ Password entered")
            except Exception as e:
                print(f"❌ Could not find password field: {str(e)}")
                return False
                
            # Submit form
            try:
                submit_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
                submit_button.click()
                print("✅ Login form submitted")
            except Exception as e:
                print(f"❌ Could not submit form: {str(e)}")
                # Try alternative method
                password_field.send_keys(Keys.RETURN)
                print("✅ Login submitted via Enter key")
                
            # Wait for login to complete
            time.sleep(10)
            
            # Check if login was successful
            if "Access denied" in self.driver.page_source:
                print("❌ Login failed - Access denied")
                return False
                
            print("✅ Login completed!")
            return True
                
        except Exception as e:
            print(f"❌ Login error: {str(e)}")
            return False
    
    def select_role(self):
        """Select the Self Service User role"""
        try:
            if not self.driver:
                print("❌ WebDriver not initialized")
                return False
                
            print("Looking for role selection...")
            time.sleep(5)
            
            # Try to find and click role
            try:
                role_div = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div/form/div[3]"))
                )
                role_div.click()
                print("✅ Role selected")
                time.sleep(2)
            except Exception as e:
                print(f"⚠️ Could not click role: {str(e)}")
            
            # Submit role selection
            try:
                submit_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div/form/div[4]/div/button"))
                )
                submit_button.click()
                print("✅ Role submitted")
            except Exception as e:
                print(f"⚠️ Could not submit role: {str(e)}")
            
            # Wait for dashboard
            print("Waiting for dashboard...")
            time.sleep(15)
            print("✅ Dashboard loaded!")
            return True
                
        except Exception as e:
            print(f"❌ Role selection error: {str(e)}")
            return False
    
    def navigate_to_new_incident(self):
        """Navigate to new incident form"""
        try:
            if not self.driver:
                print("❌ WebDriver not initialized")
                return False
                
            print("Looking for 'Report an Issue' button...")
            
            # Switch back to main content first
            try:
                self.driver.switch_to.default_content()
                print("✅ Switched to main content")
            except:
                pass
            
            # Wait for the page to load
            time.sleep(5)
            
            # Look for various possible selectors
            report_button_selectors = [
                "//button[contains(text(), 'Report an Issue')]",
                "//a[contains(text(), 'Report an Issue')]",
                "//button[contains(text(), 'Report Issue')]",
                "//a[contains(text(), 'Report Issue')]",
                "//button[@id='ext-gen60']",  # From the HTML source
                "//table[@id='ext-comp-1049']//button",
                "//button[contains(@class, 'x-btn-text') and contains(text(), 'Report')]"
            ]
            
            report_button = None
            for selector in report_button_selectors:
                try:
                    report_button = self.driver.find_element(By.XPATH, selector)
                    if report_button and report_button.is_displayed():
                        print(f"✅ Found Report button with selector: {selector}")
                        break
                except:
                    continue
                    
            if report_button:
                report_button.click()
                print("✅ Clicked 'Report an Issue'")
            else:
                print("❌ Could not find 'Report an Issue' button")
                return False
    
            # Wait for form to load
            print("Waiting for incident form to load...")
            time.sleep(10)
            
            # Check for iframes and switch to the form
            try:
                iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
                print(f"Found {len(iframes)} iframes")
                
                if iframes:
                    # Switch to the largest iframe (likely the form)
                    largest_iframe = max(iframes, key=lambda x: x.size['width'] * x.size['height'])
                    self.driver.switch_to.frame(largest_iframe)
                    print("✅ Switched to incident form iframe")
                
                    # Wait longer for form elements to load completely
                    print("Waiting for form elements to load completely...")
                    time.sleep(10)
                
                    # Take a screenshot for debugging
                    try:
                        self.driver.save_screenshot("form_debug.png")
                        print("📸 Screenshot saved as 'form_debug.png'")
                    except:
                        pass
                    
                    return True
                else:
                    print("❌ No iframes found")
                    return False
                
            except Exception as e:
                print(f"❌ Error switching to iframe: {str(e)}")
                return False
    
        except Exception as e:
            print(f"❌ Navigation error: {str(e)}")
            return False

    def _wait_for_field_validation(self, field_element, expected_value, max_wait=15):
        """Wait for dropdown field to be validated and populated"""
        try:
            print(f"    ⏳ Waiting for field validation (max {max_wait}s)...")
            start_time = time.time()
            
            while time.time() - start_time < max_wait:
                current_value = field_element.get_attribute("value") or ""
                
                # Check if the field has been populated with a valid value
                if expected_value.lower() in current_value.lower() and len(current_value) > 0:
                    print(f"    ✅ Field validated: '{current_value}'")
                    return True
                
                time.sleep(1)
            
            print(f"    ⚠️ Field validation timeout after {max_wait}s")
            return False
            
        except Exception as e:
            print(f"    ❌ Error waiting for field validation: {str(e)}")
            return False

    def fill_incident_form(self, subject, description):
        """Fill the incident form with proper timing and validation"""
        try:
            start_time = time.time()
            if not self.driver:
                print("❌ WebDriver not initialized")
                return False
                
            print("Filling incident form with proper timing...")
            
            # Wait for form to be ready
            print("Waiting for form to be ready...")
            time.sleep(3)
            
            print("\n=== USING TIMING-AWARE APPROACH ===")
            
            # Fill Service field with validation wait
            print("\n🎯 Filling Service field...")
            service_element = self.driver.find_element(By.XPATH, "//input[@id='ext-comp-1116']")
            service_element.clear()
            service_element.send_keys("Perangkat Kerja")
            print("    ✅ Typed 'Perangkat Kerja'")
            
            # Wait for validation
            if not self._wait_for_field_validation(service_element, "Perangkat Kerja"):
                print("❌ Service field validation failed")
                return False
            
            # Wait between fields
            time.sleep(3)
            
            # Fill System field with validation wait
            print("\n🎯 Filling System field...")
            system_element = self.driver.find_element(By.XPATH, "//input[@id='ext-comp-1110']")
            system_element.clear()
            system_element.send_keys("Software")
            print("    ✅ Typed 'Software'")
            
            # Wait for validation
            if not self._wait_for_field_validation(system_element, "Software"):
                print("❌ System field validation failed")
                return False

            # Fill Location field by tabbing once after System, when configured from GUI
            location_filled = False
            location_value = (self.location or "").strip()
            if location_value:
                print("\n🎯 Filling Location field...")
                system_element.send_keys(Keys.TAB)
                time.sleep(1)

                location_element = self.driver.switch_to.active_element
                location_element.clear()
                location_element.send_keys(location_value)
                print(f"    ✅ Typed Location '{location_value}'")
                location_filled = True
            else:
                print("\n🎯 Location field skipped (empty setting)")
            
            # Wait between fields
            time.sleep(3)
            
            # Fill Sub System field with validation wait
            print("\n🎯 Filling Sub System field...")
            subsystem_element = self.driver.find_element(By.XPATH, "//input[@id='ext-comp-1111']")
            subsystem_element.clear()
            subsystem_element.send_keys("Setting & Configuration")
            print("    ✅ Typed 'Setting & Configuration'")
            
            # Wait for validation
            if not self._wait_for_field_validation(subsystem_element, "Setting"):
                print("❌ Sub System field validation failed")
                return False
            
            # Wait before filling text fields
            time.sleep(3)
            
            # Fill Subject field
            print("\n🎯 Filling Subject field...")
            subject_element = self.driver.find_element(By.XPATH, "//input[@id='ext-comp-1106']")
            subject_element.clear()
            subject_element.send_keys(subject)
            print(f"✅ Subject field filled")
            
            # Wait before filling description
            time.sleep(2)
            
            # Fill Description field
            print("\n🎯 Filling Description field...")
            description_element = self.driver.find_element(By.XPATH, "//textarea[@id='ext-comp-1107']")
            description_element.clear()
            description_element.send_keys(description)
            print(f"✅ Description field filled")
            
            # Final wait before submission
            print("\n⏳ Waiting for all fields to stabilize before submission...")
            time.sleep(8)
            
            # Summary
            print(f"\n📋 FORM FILLING SUMMARY:")
            print(f"  Service Category: ⏭️ (Skipped - left as is)")
            print(f"  Service: ✅ (Perangkat Kerja)")
            print(f"  System: ✅ (Software)")
            print(f"  Location: {'✅ (' + location_value + ')' if location_filled else '⏭️ (Skipped - empty setting)'}")
            print(f"  Sub System: ✅ (Setting & Configuration)")
            print(f"  Current Location: ⏭️ (Skipped - left as is)")
            print(f"  Subject: ✅")
            print(f"  Description: ✅")
            
            elapsed_time = time.time() - start_time
            print(f"✅ Form filling completed! (took {elapsed_time:.1f} seconds)")
            return True
            
        except Exception as e:
            print(f"❌ Form filling error: {str(e)}")
            return False

    def submit_incident(self):
        """Submit the incident form and handle confirmation dialog"""
        try:
            if not self.driver:
                print("❌ WebDriver not initialized")
                return None
                
            print("Submitting incident form...")
            
            # Try to find submit button
            submit_selectors = [
                "//button[contains(text(), 'Submit')]",
                "//input[@value='Submit' or @value='Submit Incident']",
                "//input[@type='submit']",
                "//button[@type='submit']"
            ]
            
            submit_button = None
            for selector in submit_selectors:
                try:
                    submit_button = self.driver.find_element(By.XPATH, selector)
                    if submit_button and submit_button.is_displayed():
                        break
                except:
                    continue
            
            if submit_button:
                submit_button.click()
                print("✅ Submit button clicked")
                
                # Wait for confirmation dialog to appear
                time.sleep(3)
                
                # Handle confirmation dialog
                try:
                    print("Looking for confirmation dialog...")
                    
                    # Try to find the "Yes" button in confirmation dialog
                    confirmation_selectors = [
                        "//button[contains(text(), 'Yes')]",
                        "//input[@value='Yes']",
                        "//button[@id and contains(text(), 'Yes')]",
                        "//div[contains(@class, 'x-window')]//button[contains(text(), 'Yes')]"
                    ]
                    
                    yes_button = None
                    for selector in confirmation_selectors:
                        try:
                            yes_button = WebDriverWait(self.driver, 5).until(
                                EC.element_to_be_clickable((By.XPATH, selector))
                            )
                            if yes_button:
                                break
                        except:
                            continue
                    
                    if yes_button:
                        yes_button.click()
                        print("✅ Confirmation 'Yes' button clicked")
                        
                        # Wait for submission to complete
                        time.sleep(10)
                        
                        # Try to get ticket number or confirmation from page
                        try:
                            page_text = self.driver.page_source
                            if 'incident' in page_text.lower() and ('submitted' in page_text.lower() or 'created' in page_text.lower()):
                                # Try to extract ticket number
                                import re
                                ticket_pattern = r'(?:incident|ticket)[\s#:]*([A-Z0-9-]+)'
                                match = re.search(ticket_pattern, page_text, re.IGNORECASE)
                                if match:
                                    return f"SUBMITTED_SUCCESS_{match.group(1)}"
                                else:
                                    return "SUBMITTED_SUCCESS"
                            else:
                                return "SUBMITTED_UNKNOWN"
                        except:
                            return "SUBMITTED_SUCCESS"
                    else:
                        print("❌ Could not find confirmation 'Yes' button")
                        return None
                        
                except Exception as e:
                    print(f"⚠️ Error handling confirmation dialog: {str(e)}")
                    # Maybe the dialog didn't appear, submission might have worked
                    time.sleep(5)
                    return "SUBMITTED_UNKNOWN"
                    
            else:
                print("❌ Could not find submit button")
                return None
            
        except Exception as e:
            print(f"❌ Submit error: {str(e)}")
            return None

    def navigate_back_to_dashboard(self):
        """Navigate back to dashboard"""
        try:
            if not self.driver:
                print("❌ WebDriver not initialized")
                return False
                
            print("Navigating back to dashboard...")
            
            # Switch back to main content
            self.driver.switch_to.default_content()
            
            # Go to dashboard URL
            dashboard_url = "https://servicedesk.adira.co.id/HEAT/Default.aspx"
            self.driver.get(dashboard_url)
            time.sleep(5)
            
            print("✅ Returned to dashboard")
            return True
            
        except Exception as e:
            print(f"❌ Navigation error: {str(e)}")
            return False
    
    def process_tickets(self):
        """Process tickets from Excel file"""
        try:
            print("Loading Excel file: tickets.xlsx")
            
            if not os.path.exists('tickets.xlsx'):
                print("❌ tickets.xlsx file not found!")
                return False
    
            # Load workbook for reading values
            print("Loading Excel file for reading values...")
            workbook_read = openpyxl.load_workbook('tickets.xlsx', data_only=True)
            worksheet_read = workbook_read.active
            
            # Load workbook for saving (preserve formulas)
            print("Loading Excel file for preserving formulas...")
            workbook_save = openpyxl.load_workbook('tickets.xlsx', data_only=False)
            worksheet_save = workbook_save.active
            
            if not worksheet_read or not worksheet_save:
                print("❌ Could not access worksheets")
                return False
            
            print(f"✅ Excel files loaded")
            print(f"Total rows: {worksheet_read.max_row}")
            
            successful_tickets = 0
            failed_tickets = 0
            results = []
            
            # Process each row (skip header)
            for row_num in range(2, worksheet_read.max_row + 1):
                try:
                    # Get data from Excel (using the read workbook for calculated values)
                    subject_cell = worksheet_read.cell(row=row_num, column=1)
                    description_cell = worksheet_read.cell(row=row_num, column=2)
                    
                    # Debug: Show raw cell values
                    print(f"🔍 Row {row_num} - Raw values:")
                    print(f"  Subject cell: '{subject_cell.value}' (type: {type(subject_cell.value)})")
                    print(f"  Description cell: '{description_cell.value}' (type: {type(description_cell.value)})")
                    
                    subject = str(subject_cell.value or "").strip()
                    description = str(description_cell.value or "").strip()
                    
                    print(f"  Processed - Subject: '{subject}', Description: '{description}'")
                    
                    if not subject or not description:
                        print(f"⚠️ Skipping row {row_num}: Empty data")
                        continue
                    
                    print(f"\n📋 Processing ticket {row_num - 1}")
                    print(f"Subject: {subject}")
                    print(f"Description: {description}")
                    
                    # Navigate to new incident form
                    if not self.navigate_to_new_incident():
                        print("❌ Failed to navigate to form")
                        failed_tickets += 1
                        results.append(f"Ticket {row_num - 1}: FAILED - Navigation failed")
                        continue
                    
                    # Fill form
                    if not self.fill_incident_form(subject, description):
                        print("❌ Failed to fill form")
                        failed_tickets += 1
                        results.append(f"Ticket {row_num - 1}: FAILED - Form filling failed")
                        continue
                    
                    # Submit form
                    ticket_number = self.submit_incident()
                    
                    if ticket_number:
                        print(f"✅ Success! Ticket: {ticket_number}")
                        successful_tickets += 1
                        results.append(f"Ticket {row_num - 1}: SUCCESS - {ticket_number}")
                        
                        # Update Excel with ticket number (using the save workbook to preserve formulas)
                        worksheet_save.cell(row=row_num, column=3, value=ticket_number)
                        
                        # Navigate back for next ticket
                        if row_num < worksheet_read.max_row:
                            self.navigate_back_to_dashboard()
                            time.sleep(3)
                    else:
                        print("❌ Submission failed")
                        failed_tickets += 1
                        results.append(f"Ticket {row_num - 1}: FAILED - Submission failed")
                    
                    # Save Excel after each ticket (using the save workbook to preserve formulas)
                    workbook_save.save('tickets.xlsx')
                    
                except Exception as e:
                    print(f"❌ Error processing ticket {row_num - 1}: {str(e)}")
                    failed_tickets += 1
                    results.append(f"Ticket {row_num - 1}: FAILED - {str(e)}")
            
            # Final save (using the save workbook to preserve formulas)
            workbook_save.save('tickets.xlsx')
            
            # Close workbooks to release file handles
            workbook_read.close()
            workbook_save.close()
            
            # Write results
            with open('ticket_results.txt', 'w', encoding='utf-8') as f:
                f.write("SERVICEDESK TICKET PROCESSING RESULTS\n")
                f.write("=" * 50 + "\n")
                f.write(f"Total processed: {successful_tickets + failed_tickets}\n")
                f.write(f"Successful: {successful_tickets}\n")
                f.write(f"Failed: {failed_tickets}\n")
                if successful_tickets + failed_tickets > 0:
                    success_rate = (successful_tickets / (successful_tickets + failed_tickets)) * 100
                    f.write(f"Success rate: {success_rate:.1f}%\n\n")
                
                f.write("DETAILED RESULTS:\n")
                for result in results:
                    f.write(result + "\n")
            
            print(f"\n🎯 FINAL SUMMARY")
            print(f"Total tickets: {successful_tickets + failed_tickets}")
            print(f"Successful: {successful_tickets}")
            print(f"Failed: {failed_tickets}")
            if successful_tickets + failed_tickets > 0:
                success_rate = (successful_tickets / (successful_tickets + failed_tickets)) * 100
                print(f"Success rate: {success_rate:.1f}%")
            
            return successful_tickets > 0
            
        except Exception as e:
            print(f"❌ Processing error: {str(e)}")
            return False
        finally:
            # Ensure workbooks are closed even if there's an error
            try:
                if 'workbook_read' in locals():
                    workbook_read.close()
                if 'workbook_save' in locals():
                    workbook_save.close()
            except:
                pass
    
    def run(self):
        """Run the complete automation"""
        try:
            print("=== ServiceDesk Automation Started ===")
            
            # Setup WebDriver
            if not self.setup_driver():
                print("❌ Failed to setup WebDriver")
                input("❌ Press Enter to continue...")  # Pause for error
                return False
            
            # Get credentials
            username = input("Enter ServiceDesk username: ")
            password = input("Enter ServiceDesk password: ")
            
            # Login
            if not self.login(username, password):
                print("❌ Login failed")
                input("❌ Press Enter to continue...")  # Pause for error
                return False
            
            # Select role
            if not self.select_role():
                print("❌ Role selection failed")
                input("❌ Press Enter to continue...")  # Pause for error
                return False
            
            # Process tickets
            if not self.process_tickets():
                print("❌ Ticket processing failed")
                input("❌ Press Enter to continue...")  # Pause for error
                return False
            
            print("✅ Automation completed successfully!")
            input("✅ Press Enter to close...")  # Pause for success
            return True
            
        except Exception as e:
            print(f"❌ Automation error: {str(e)}")
            print("❌ Full error details:")
            import traceback
            traceback.print_exc()
            input("❌ Press Enter to close after error...")  # Pause for error
            return False
        finally:
            # Close browser
            if self.driver:
                try:
                    self.driver.quit()
                    print("✅ Browser closed")
                except:
                    pass

if __name__ == "__main__":
    automation = ServiceDeskAutomation()
    automation.run()


