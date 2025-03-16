"""Naukri Daily update - Using Chrome"""

import io
import logging
import os
import sys
import time
from datetime import datetime
from random import choice, randint
from string import ascii_uppercase, digits

from pypdf import PdfReader, PdfWriter
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager as CM

# Paths for your resume
originalResumePath = "/Users/ishashukla/Desktop/Testing/IshaShukla_DataAnalyst.pdf"
modifiedResumePath = "/Users/ishashukla/Desktop/Testing/modified_resume.pdf"

# Naukri credentials and mobile number
username = "isha03@gmail.com"
password = "abcd123F"
mob = "1234567890"  # Mobile number (not used in profile update anymore)

# Set to False if you don't want to modify your resume; it will be uploaded as is
updatePDF = False

# If headless = True, Chrome will run without a visible GUI
headless = False

# Set login URL
NaukriURL = "https://www.naukri.com/nlogin/login"

# Configure logging
logging.basicConfig(
    level=logging.INFO, filename="naukri.log", format="%(asctime)s    : %(message)s"
)
os.environ["WDM_LOCAL"] = "1"
os.environ["WDM_LOG_LEVEL"] = "0"


def log_msg(message):
    """Print to console and log the message."""
    print(message)
    logging.info(message)


def catch(error):
    """Log error details with exception information."""
    _, _, exc_tb = sys.exc_info()
    lineNo = str(exc_tb.tb_lineno) if exc_tb else "N/A"
    msg = f"{type(error)} : {error} at Line {lineNo}."
    print(msg)
    logging.error(msg)


def getObj(locatorType):
    """Map locator types to Selenium By objects."""
    mapping = {
        "ID": By.ID,
        "NAME": By.NAME,
        "XPATH": By.XPATH,
        "TAG": By.TAG_NAME,
        "CLASS": By.CLASS_NAME,
        "CSS": By.CSS_SELECTOR,
        "LINKTEXT": By.LINK_TEXT,
    }
    return mapping[locatorType.upper()]


def GetElement(driver, elementTag, locator="ID"):
    """Wait max 15 secs for an element and return it when available."""
    try:
        _by = getObj(locator)
        element = WebDriverWait(driver, 15).until(
            lambda d: d.find_element(_by, elementTag)
        )
        return element
    except Exception as e:
        log_msg(f"Element not found with {locator} : {elementTag}")
        catch(e)
        return None


def is_element_present(driver, how, what):
    """Returns True if element is present."""
    try:
        driver.find_element(by=how, value=what)
    except NoSuchElementException:
        return False
    return True


def WaitTillElementPresent(driver, elementTag, locator="ID", timeout=30):
    """Wait until an element is present (default timeout: 30 seconds)."""
    result = False
    driver.implicitly_wait(0)
    locator = locator.upper()
    _by = getObj(locator)
    for _ in range(timeout):
        time.sleep(0.99)
        try:
            if is_element_present(driver, _by, elementTag):
                result = True
                break
        except Exception as e:
            log_msg(f"Exception in WaitTillElementPresent: {e}")
    if not result:
        log_msg(f"Element not found with {locator} : {elementTag}")
    driver.implicitly_wait(3)
    return result


def tearDown(driver):
    """Close and quit the WebDriver."""
    try:
        driver.close()
        log_msg("Driver Closed Successfully")
    except Exception as e:
        catch(e)
    try:
        driver.quit()
        log_msg("Driver Quit Successfully")
    except Exception as e:
        catch(e)


def randomText():
    return "".join(choice(ascii_uppercase + digits) for _ in range(randint(1, 5)))


def LoadNaukri(headless):
    """Open Chrome and load Naukri.com."""
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-notifications")
    options.add_argument("--start-maximized")  # Use "--kiosk" for Mac if needed
    options.add_argument("--disable-popups")
    options.add_argument("--disable-gpu")
    if headless:
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("headless")

    try:
        driver = webdriver.Chrome(options=options, service=ChromeService(CM().install()))
    except Exception as e:
        log_msg("Error initializing ChromeDriver, trying fallback.")
        catch(e)
        driver = webdriver.Chrome(options=options)
    log_msg("Google Chrome Launched!")
    driver.implicitly_wait(3)
    driver.get(NaukriURL)
    return driver


def naukriLogin(headless=False):
    """Open Chrome browser and Login to Naukri.com."""
    status = False
    driver = None
    username_locator = "usernameField"
    password_locator = "passwordField"
    login_btn_locator = "//*[@type='submit' and normalize-space()='Login']"
    # Removed skip_locator usage

    try:
        driver = LoadNaukri(headless)

        if "naukri" in driver.title.lower():
            log_msg("Website Loaded Successfully.")

        if is_element_present(driver, By.ID, username_locator):
            emailFieldElement = GetElement(driver, username_locator, locator="ID")
            time.sleep(1)
            passFieldElement = GetElement(driver, password_locator, locator="ID")
            time.sleep(1)
            loginButton = GetElement(driver, login_btn_locator, locator="XPATH")
        else:
            log_msg("None of the login elements found.")
            return (False, driver)

        if emailFieldElement and passFieldElement and loginButton:
            emailFieldElement.clear()
            emailFieldElement.send_keys(username)
            time.sleep(1)
            passFieldElement.clear()
            passFieldElement.send_keys(password)
            time.sleep(1)
            loginButton.send_keys(Keys.ENTER)
            time.sleep(1)

            # Check login success by waiting for a checkpoint element
            if WaitTillElementPresent(driver, "ff-inventory", locator="ID", timeout=40):
                CheckPoint = GetElement(driver, "ff-inventory", locator="ID")
                if CheckPoint:
                    log_msg("Naukri Login Successful")
                    status = True
                    return (status, driver)
                else:
                    log_msg("Unknown Login Error")
            else:
                log_msg("Unknown Login Error")
    except Exception as e:
        catch(e)
    return (status, driver)


def UpdateProfile(driver):
    """Update profile without updating mobile number (mobile update code removed)."""
    try:
        view_profile_locator = "//*[contains(@class, 'view-profile')]//a"
        edit_locator = "(//*[contains(@class, 'icon edit')])[1]"
        # Retain save button locator since it is needed
        saveXpath = "//button[@type='submit'][@value='Save Changes'] | //*[@id='saveBasicDetailsBtn']"
        save_confirm = "//*[text()='today' or text()='Today']"

        if WaitTillElementPresent(driver, view_profile_locator, "XPATH", 20):
            profElement = GetElement(driver, view_profile_locator, locator="XPATH")
            if profElement:
                profElement.click()
                time.sleep(2)
        else:
            log_msg("View profile element not found.")

        if WaitTillElementPresent(driver, edit_locator, "XPATH", 20):
            editElement = GetElement(driver, edit_locator, locator="XPATH")
            if editElement:
                editElement.click()
                time.sleep(2)
                # Skipping mobile number update
                if WaitTillElementPresent(driver, saveXpath, "XPATH", 20):
                    saveFieldElement = GetElement(driver, saveXpath, locator="XPATH")
                    if saveFieldElement:
                        saveFieldElement.click()
                        time.sleep(3)
                    else:
                        log_msg("Save button not found.")
                else:
                    log_msg("Save button did not appear.")
            else:
                log_msg("Edit button not found.")
        else:
            log_msg("Edit locator not found.")

        if WaitTillElementPresent(driver, save_confirm, "XPATH", 10):
            if is_element_present(driver, By.XPATH, save_confirm):
                log_msg("Profile Update Successful")
            else:
                log_msg("Profile Update Failed")
        time.sleep(5)
    except Exception as e:
        catch(e)


def UpdateResume():
    """Update resume by merging random hidden text into the last page of the PDF."""
    try:
        # Generate random text with random properties
        txt = randomText()
        xloc = randint(700, 1000)  # Position adjustment
        fsize = randint(1, 10)

        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)
        can.setFont("Helvetica", fsize)
        can.drawString(xloc, 100, txt)
        can.save()

        packet.seek(0)
        new_pdf = PdfReader(packet)
        try:
            with open(originalResumePath, "rb") as f:
                existing_pdf = PdfReader(f)
        except Exception as e:
            catch(e)
            log_msg("Error accessing the original resume file.")
            return os.path.abspath(originalResumePath)

        pagecount = len(existing_pdf.pages)
        log_msg(f"Found {pagecount} pages in PDF")

        output = PdfWriter()
        # Merge new PDF with last page of existing PDF
        for pageNum in range(pagecount - 1):
            output.add_page(existing_pdf.pages[pageNum])

        last_page = existing_pdf.pages[pagecount - 1]
        last_page.merge_page(new_pdf.pages[0])
        output.add_page(last_page)
        try:
            with open(modifiedResumePath, "wb") as outputStream:
                output.write(outputStream)
            log_msg(f"Saved modified PDF: {modifiedResumePath}")
            return os.path.abspath(modifiedResumePath)
        except Exception as e:
            catch(e)
            log_msg("Error writing the modified resume file.")
    except Exception as e:
        catch(e)
    return os.path.abspath(originalResumePath)


def UploadResume(driver, resumePath):
    """Upload resume on Naukri profile without using a save button or closing popups."""
    try:
        attachCVID = "attachCV"
        CheckPointXpath = "//*[contains(@class, 'updateOn')]"

        driver.get("https://www.naukri.com/mnjuser/profile")
        time.sleep(2)

        if WaitTillElementPresent(driver, attachCVID, locator="ID", timeout=10):
            AttachElement = GetElement(driver, attachCVID, locator="ID")
            if AttachElement:
                AttachElement.send_keys(resumePath)
            else:
                log_msg("Attachment element not found.")

        if WaitTillElementPresent(driver, CheckPointXpath, locator="XPATH", timeout=30):
            CheckPoint = GetElement(driver, CheckPointXpath, locator="XPATH")
            if CheckPoint:
                LastUpdatedDate = CheckPoint.text
                todaysDate1 = datetime.today().strftime("%b %d, %Y")
                todaysDate2 = datetime.today().strftime("%b %#d, %Y")
                if todaysDate1 in LastUpdatedDate or todaysDate2 in LastUpdatedDate:
                    log_msg("Resume Document Upload Successful. Last Updated date = %s" % LastUpdatedDate)
                else:
                    log_msg("Resume Document Upload failed. Last Updated date = %s" % LastUpdatedDate)
            else:
                log_msg("Resume Document Upload failed. Last Updated date not found.")
    except Exception as e:
        catch(e)
    time.sleep(2)


def main():
    log_msg("-----Naukri.py Script Run Begin-----")
    driver = None
    try:
        status, driver = naukriLogin(headless)
        if status and driver:
            UpdateProfile(driver)
            if os.path.exists(originalResumePath):
                if updatePDF:
                    resumePath = UpdateResume()
                    UploadResume(driver, resumePath)
                else:
                    UploadResume(driver, originalResumePath)
            else:
                log_msg("Resume not found at %s" % originalResumePath)
        else:
            log_msg("Login failed. Exiting script.")
    except Exception as e:
        catch(e)
    finally:
        tearDown(driver)
    log_msg("-----Naukri.py Script Run Ended-----\n")


if __name__ == "__main__":
    main()
