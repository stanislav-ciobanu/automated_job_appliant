import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_mitp_dinamic():
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    
    url = "https://mitp.md/ro/profilul-rezidentilor/"
    driver.get(url)
    
    wait = WebDriverWait(driver, 15)
    
    try:
        button_cookie = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#faz-consent .faz-btn-accept")))
        button_cookie.click()
        time.sleep(1.5)
    except Exception:
        pass

    saved_companies = {}
    print("Start mixed process (Scroll + Extract)...")
    
    last_height = driver.execute_script("return document.body.scrollHeight")
    no_change_count = 0
    
    while True:
        visible_rows = driver.find_elements(By.CSS_SELECTOR, "tbody tr.mitp-resident-table-row")
        
        for row in visible_rows:
            try:
                id_unique = row.get_attribute("data-resident-id")
                if not id_unique:
                    id_unique = row.get_attribute("id")
                
                if id_unique in saved_companies:
                    continue
                
                cells = row.find_elements(By.TAG_NAME, "td")
                if len(cells) > 1 and cells[0].text.strip().isdigit():
                    company_name = cells[1].text.strip()
                else:
                    company_name = cells[0].text.strip() if cells else "Company"

                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", row)
                time.sleep(0.3)
                row.click()
                
                panel_class = ".mitp-resident-drawer, [class*='drawer'], .mitp-resident-drawer-backdrop-visible"
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, panel_class)))
                time.sleep(1.2)
                
                email = "Not specified"
                phone = "Not specified"
                
                email_elements = driver.find_elements(By.CSS_SELECTOR, "a[href^='mailto:']")
                for el in email_elements:
                    if el.is_displayed():
                        email = el.get_attribute("href").replace("mailto:", "").strip()
                        break
                        
                phone_elements = driver.find_elements(By.CSS_SELECTOR, "a[href^='tel:']")
                for el in phone_elements:
                    if el.is_displayed():
                        phone = el.get_attribute("href").replace("tel:", "").strip()
                        break

                saved_companies[id_unique] = {
                    "Company": company_name,
                    "Email": email,
                    "Phone": phone
                }
                print(f"[{len(saved_companies)}] {company_name} -> {email} | {phone}")
                
                try:
                    backdrop = driver.find_element(By.CSS_SELECTOR, ".mitp-resident-drawer-backdrop")
                    driver.execute_script("arguments[0].click();", backdrop)
                    time.sleep(0.4)
                except:
                    pass
                    
            except Exception as e_row:
                try:
                    backdrop = driver.find_element(By.CSS_SELECTOR, ".mitp-resident-drawer-backdrop")
                    driver.execute_script("arguments[0].click();", backdrop)
                    time.sleep(0.4)
                except:
                    pass
                continue
        
        driver.execute_script("window.scrollBy(0, 3000);")
        time.sleep(2.5)
        
        new_height = driver.execute_script("return document.body.scrollHeight")
        
        if new_height == last_height:
            no_change_count += 1
            
            driver.execute_script("window.scrollBy(0, -300);")
            time.sleep(0.5)
            driver.execute_script("window.scrollBy(0, 600);")
            time.sleep(1.5)
            
            if no_change_count > 15:  
                print(f"\nWe reached the end of page (Scroll completed). Total companies processed: {len(saved_companies)}")
                break
        else:
            no_change_count = 0
            last_height = new_height

    driver.quit()
    
    final_list = list(saved_companies.values())
    if final_list:
        df = pd.DataFrame(final_list)
        df.to_excel("list_emails_residents_mitp.xlsx", index=False)
        print(f"\nSucces! File 'list_emails_residents_mitp.xlsx' contains all {len(lista_finala)} extracted companies.")
    else:
        print("\nCannot find data to save.")

if __name__ == "__main__":
    scrape_mitp_dinamic()
