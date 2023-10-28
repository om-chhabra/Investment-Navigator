from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd
# Setup WebDriver (assuming you have the Chrome WebDriver installed)
driver = webdriver.Firefox()
detail_data=[]
def extract_value_by_label(soup, label):
    try:
        divs = soup.find_all("div", class_="txn--display-flex-row")
        for div in divs:
            bold_texts = div.find_all("div", class_="txn--text-body-bold")
            for bold_text in bold_texts:
                if label in bold_text.text:
                    value_div = div.find("div", class_="txn--text-body")
                    if value_div:
                        return value_div.text.strip()
    except Exception as e:
        print(f"Error extracting {label}: {e}")
    return None
try:
    # Navigate to the URL
    driver.get('https://tracxn.com/a/s/query/t/companiescovered/t/all/card?h=186597849406d9eee16fb7406239c1f0477828d780d0b5262297abf8a0df5be9&s=sort%3Drelevance%7Corder%3DDEFAULT')
    username_field = driver.find_element(By.ID, "email_")
    username_field.send_keys("shubham.vishwakarma55@svkmmumbai.onmicrosoft.com")
    username_field.submit()
    time.sleep(2) 

    password_field = driver.find_element(By.ID, "password_")
    password_field.send_keys("SV@12345")
    password_field.submit()
    time.sleep(25)
    # Get the page source   
    page_source = driver.page_source

    # Create a Beautiful Soup obje
    soup = BeautifulSoup(page_source, 'html.parser')
       # Extracting data
    companies = [a.text for a in soup.find_all('a', {'class': 'txn--link txn--text-decoration-none txn--text-subheading txn--font-medium txn--text-color-curious-blue'})]
    data = [span.text for span in soup.find_all('span', {'class': 'company-card--location txn--display-inline-block'})]
    # for company in companies:
    #     anchor_tag = driver.find_element(By.LINK_TEXT,company)
    #     anchor_tag.click()
    #     page_source = driver.page_source
    #     soup2 = BeautifulSoup(page_source, 'html.parser')
    #     time.sleep(5)
    #     last_funding_round = extract_value_by_label(soup2, "Last Funding Round")
    #     post_money_valuation = extract_value_by_label(soup2, "Post-Money Valuation")
    #     annual_revenue = extract_value_by_label(soup2, "Annual Revenue")
    #     employee_count = extract_value_by_label(soup2, "Employee Count")
    #     detail_data.append([last_funding_round,post_money_valuation,annual_revenue,employee_count])
    #     print(detail_data)
    #     close = driver.find_element(By.CSS_SELECTOR, "[aria-label='Close Overlay']")
    #     close.click()
    #     time.sleep(5)

#     description = soup.find('span', {'class': 'font-black'}).text
#     location_element = soup.find('span', {'class': 'txn--comp-multi-location company-card--location txn--display-inline-block txn--display-inline-block'})

#     # Check if the element was found before attempting to access its text attribute
#     if location_element is not None:
#         location = location_element.text
#     else:
#         location = "Location not found"

#     founding_year = soup.find_all('span', {'class': 'company-card--location txn--display-inline-block'})[0].text
#     total_funding = soup.find_all('span', {'class': 'company-card--location txn--display-inline-block'})[1].text
#     investment_round = soup.find_all('span', {'class': 'company-card--location txn--display-inline-block'})[2].text
#     div_element = soup.find('div', {'class': 'company-card--margin-xxs'})

# # Check if the div element was found
#     if div_element is not None:
#         # Attempt to find the a element within the div element
#         a_element = div_element.find('a')
        
#         # Check if the a element was found
#         if a_element is not None:
#             part_of = a_element.text
#         else:
#             part_of = "a tag not found"
#     else:
#         part_of = "div not found"

#     # Investors (the actual names are blurred, but you can find the structure here)
#     investors = soup.find('div', {'title': 'Investors'}).text

#     # Key People
#     key_people = [a.text for a in soup.find_all('a', {'class': 'txn--link-minimal txn--text-color-mine-shaft'})]

#     # Acquisitions
#     acquisitions = [a.text for a in soup.find_all('a', {'class': ' txn--text-color-dark-gray font-black'})]

    # Display extracted data
    print(companies)
    
    # Reshape data list into a 2D list with each inner list representing a startup's info
    reshaped_data = [data[i:i+3] for i in range(0, len(data), 3)]

    # Combine company names and reshaped data
    combined_data = list(zip(companies, reshaped_data))

    # Create DataFrame
    df = pd.DataFrame(combined_data, columns=['Company', 'Info'])

    # Split 'Info' column into separate columns
    df[['Founded Year', 'Funding Raised', 'Funding Round']] = pd.DataFrame(df['Info'].tolist(), index=df.index)

    # Drop the now redundant 'Info' column
    df = df.drop(columns=['Info'])

    # Display the DataFrame
    print(df)

    
    # print(f'Description: {description}')
    # print(f'Location: {location}')
    # print(f'Founding Year: {founding_year}')
    # print(f'Total Funding: {total_funding}')
    # print(f'Investment Round: {investment_round}')
    # print(f'Part of: {part_of}')
    # print(f'Investors: {investors}')
    # print(f'Key People: {key_people}')
    # print(f'Acquisitions: {acquisitions}')
    
finally:
    # It's a good practice to close the driver to clean up
    driver.quit()