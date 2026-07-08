import os
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import pandas as pd

MY_EMAIL = "sciobanu.work@gmail.com"
APP_PASS = "zwjx wmls ypsl mwxm"
REPLY_TO_EMAIL = "stanislav.ciobanu@outlook.com"

EXCEL_FILE = "list_emails_residents_mitp.xlsx"
POSITION_NAME = "Junior Software Engineer"

PATH_RESUME = os.path.abspath("Ciobanu Stanislav CV.pdf")
PATH_CERTIFICATE = os.path.abspath("Certificate of Graduation.pdf")

SUBJECT_EMAIL = f"{POSITION_NAME}"
TEXT_HTML_TEMPLATE = """
<html>
  <body>
    <p>Hello,</p>
    <p> </p>
    <p>I am applying for the <strong>{post}</strong> position in your company, please find my CV attached.</p>
    <p> </p>
    <p>I am a part-time student at the Technical University of Moldova and a CEITI graduate, with basic knowledge of Java/PHP, Spring (Boot, Security, Data, AI), Vue,js, HTML, CSS, JavaScript (Node.js environment), MySQL/PostgreSQL, Hibernate/JPA, REST APIs, Postman, Docker, Git, etc. I am eager to learn and grow in your team.</p>
    <p> </p>
    <p>As previous experience I have 2 Java Full-Stack Internship at the companies Inther Sofware Development (ISD) and Unifun International, plus a portfolio of practical university projects.</p>
    <p> </p>
    <p>Thank you for your consideration.</p>
    <p> </p>
    <p>Kind regards,<br>
    Ciobanu Stanislav<br>
    Phone: +373 76 76 21 97<br>
    Email: stanislav.ciobanu@outlook.com</p>
  </body>
</html>
"""

def add_attach(msg, file_path):
    if os.path.exists(file_path):
        file_name = os.path.basename(file_path)
        with open(file_path, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename= {file_name}")
        msg.attach(part)
        return True
    return False

def send_emails_smtp():
    if not os.path.exists(PATH_RESUME) or not os.path.exists(PATH_CERTIFICATE):
        print("Error: Cannot find needed PDFs files for email attach in current folder!")
        return

    if not os.path.exists(EXCEL_FILE):
        print(f"Error: File Excel '{EXCEL_FILE}' cannot find.")
        return

    try:
        df = pd.read_excel(EXCEL_FILE)
    except Exception as e:
        print(f"Error at opening Excel file: {e}")
        return

    if df.empty:
        print("Excel file is empty. Dont have more emails to send!")
        return

    print(f"Total rows in Excel: {len(df)}")
    succes_sended = 0

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(MY_EMAIL, APP_PASS)
    except Exception as e:
        print(f"SMTP Connection Error: {e}")
        return

    while not df.empty:
        index_curent = 0
        rand = df.iloc[index_curent]
        
        destination_email = str(rand.get("Email", "N/A")).strip()
        
        if destination_email == "Nespecificat" or "@" not in destination_email:
            print(f"Skipped. Invalid or empty mail: '{destination_email}' !")
            df = df.drop(df.index[index_curent]).reset_index(drop=True)
            df.to_excel(EXCEL_FILE, index=False)
            continue

        print(f"Try send to: {destination_email} ...")

        try:
            msg = MIMEMultipart()
            msg['From'] = MY_EMAIL
            msg['To'] = destination_email
            msg['Reply-To'] = REPLY_TO_EMAIL
            msg['Subject'] = SUBJECT_EMAIL
            
            html_body = TEXT_HTML_TEMPLATE.format(post=POSITION_NAME)
            msg.attach(MIMEText(html_body, 'html'))
            
            add_attach(msg, PATH_RESUME)
            add_attach(msg, PATH_CERTIFICATE)
            
            server.sendmail(MY_EMAIL, destination_email, msg.as_string())
            
            succes_sended += 1
            print(f" -> [SUCCES] Email sended to {destination_email} !")
            
            df = df.drop(df.index[index_curent]).reset_index(drop=True)
            df.to_excel(EXCEL_FILE, index=False)
            
            time.sleep(15.0)

        except Exception as e_sended:
            print(f"\n[ALERT ERROR] Aborted send to {destination_email} !")
            print(f"Error motivation: {e_sended}")
            print("Script started automatically. Data remain safed intacted in Excel.")
            break

    server.quit()
    print(f"\nSession finished. Has been sended {succes_sended} emails in this rulation.")

if __name__ == "__main__":
    send_emails_smtp()
