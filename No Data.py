import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
 
# List of keywords to check for "NOT WORKING" sites
not_working_keywords = [
    "domain expired", "domain for sale", "coming soon", "opening soon",
    "privacy error", "lander", "under construction", "not found", "404"
]
 
# Function to check if a URL is working by sending a GET request
def check_url_status(url):
    try:
        # Send GET request with a timeout of 10 seconds
        response = requests.get(url, timeout=10)
       
        # If the status code is not 2xx, mark it as "NOT WORKING"
        if response.status_code != 200:
            return "NOT WORKING"
       
        # Parse the page content with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
       
        # Check if the page contains any "not working" keywords
        page_text = soup.get_text().lower()
        for keyword in not_working_keywords:
            if keyword in page_text:
                return "NOT WORKING"
       
        # If no issues found, mark the site as working
        return "WORKING"
 
    except requests.exceptions.RequestException:
        # Any request errors (e.g., timeout, connection error) result in "NOT WORKING"
        return "NOT WORKING"
    except Exception as e:
        # Catch any other unexpected errors
        print(f"Error checking URL {url}: {str(e)}")
        return "NOT WORKING"
 
# Function to process the Excel file and update the status
def update_url_status(excel_file):
    # Read the Excel file with URLs
    df = pd.read_excel(excel_file)
 
    # Assuming the URLs are in the first column (index 0) and there is a "Status" column for results
    for index, row in df.iterrows():
        url = row[0]  # Get the URL from the first column
        print(f"Checking URL: {url}")
        status = check_url_status(url)
        df.at[index, 'Status'] = status  # Update the 'Status' column with the result
 
    # Save the updated Excel file with the new status
    df.to_excel("C:\\Users\\ACER\\Downloads\\Tets\\Book1.xlsx", index=False)
    print("The updated status has been saved to 'updated_url_status.xlsx'.")
 
# Example usage
if __name__ == "__main__":
    # Specify the Excel file path containing the URLs
    excel_file = 'C:\\Users\\ACER\\Downloads\\Tets\\Book1.xlsx'  # Replace with your actual file path
    update_url_status('C:\\Users\\ACER\\Downloads\\Tets\\Book1.xlsx')
 