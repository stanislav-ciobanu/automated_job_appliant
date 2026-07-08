# MITP Resident Scraper & Automated Job Application Sender

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Selenium](https://img.shields.io/badge/-selenium-%2343B02A?style=for-the-badge&logo=selenium&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)

## Overview
This project consists of two Python scripts designed to automate the process of finding and contacting potential employers. 
1. **`parser_emails_excel.py`**: A web scraper that extracts company information (name, email, and phone number) from the Moldova Innovation Technology Park (https://mitp.md/ro/profilul-rezidentilor/) resident directory and saves it to an Excel file.
2. **`mail_sender.py`**: An automated email client that reads the generated Excel file and sends a customized HTML job application, complete with PDF attachments (CV and graduation certificate), to each company. It also features progress tracking by updating the Excel file after each successful send.

---

## Technologies & Tech Stack
* **Language:** Python 3.x
* **Web Scraping / Browser Automation:** `selenium`, `webdriver`
* **Data Manipulation:** `pandas`, `openpyxl` (required for Excel read/write operations)
* **Email Protocol:** `smtplib` (SMTP protocol for sending emails)
* **Email Formatting:** `email.mime` (MIMEMultipart, MIMEText, MIMEBase)
* **Built-in Modules:** `os`, `time`

---

## File Structure & Script Details

### 1. `parser_emails_excel.py` 🕸️
This script uses Selenium to navigate the MITP residents portal, handling dynamic content loading and pop-up overlays.
* **Bypass Automation Detection:** Uses Chrome options (`--disable-blink-features=AutomationControlled`, `excludeSwitches`) to prevent the browser from blocking the automated session.
* **Dynamic Scrolling:** Uses JavaScript injection (`window.scrollBy`) to infinitely scroll until the DOM height stops changing, ensuring all dynamically loaded residents are rendered.
* **Data Extraction:** Locates `mailto:` and `tel:` anchor tags within dynamic drawers/modals to extract contact details.
* **Data Export:** Compiles the scraped data into a Pandas DataFrame and exports it to `list_emails_residents_mitp.xlsx`.

### 2. `mail_sender.py` 📧
This script acts as a bulk email sender using a Gmail SMTP server, specifically designed for job hunting.
* **SMTP Integration:** Authenticates with Gmail using TLS encryption on port 587 and an App Password.
* **MIME Composition:** Constructs a multipart email containing an HTML body and base64-encoded PDF attachments (`Ciobanu Stanislav CV.pdf` and `Certificate of Graduation.pdf`).
* **State Management:** Reads the Excel file row by row. If an email is successfully sent, the script drops that row and overwrites the Excel file. If the script crashes or is stopped, it can be restarted without sending duplicate emails.
* **Rate Limiting:** Implements a 15-second delay (`time.sleep(15.0)`) between emails to avoid triggering spam filters or rate limits.

---

## Setup & Installation ⚙️

### Prerequisites
1. **Python 3.8+** installed on your machine.
2. **Google Chrome** installed.
3. **App Password:** A Google App Password generated for your Gmail account.

### Dependencies
Install the required Python packages using pip:
```bash
pip install selenium pandas openpyxl
```

### Configuration
Before running `mail_sender.py`, ensure you configure the following variables inside the script:
* `MY_EMAIL`: Your Gmail address.
* `APP_PASS`: Your 16-character Google App Password (do not use your standard email password).
* `REPLY_TO_EMAIL`: The email address you want employers to reply to.
* Ensure both PDF files (`Ciobanu Stanislav CV.pdf` and `Certificate of Graduation.pdf`) are located in the same root directory as the script.

---

## Usage 🚀

**Step 1: Scrape the data**
Run the parser to generate the Excel file containing the companies contact information.
```bash
python parser_emails_excel.py
```
*Note: A Chrome window will open and automatically scroll through the website. Do not interact with the browser while the script is running.*

**Step 2: Send the applications**
Once `list_emails_residents_mitp.xlsx` is generated, run the email sender:
```bash
python mail_sender.py
```
*Monitor the console output for success logs or error alerts. If you got error from mail server because you reached today limit of number of sended messages, just re-run second script after 24 hours, and proccess will be start from last company from excel where you remain last time*
