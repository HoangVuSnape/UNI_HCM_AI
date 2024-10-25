# README for `crawl.py` and `crawlOnePdf.py`

## Overview

This project is designed to automate the process of logging into a student portal, retrieving information from web pages, and interacting with PDF documents. The project consists of two Python scripts—`crawl.py` and `crawlOnePdf.py`—that utilize Selenium WebDriver to automate web scraping and interaction with a PDF viewer. Additionally, shared functions are abstracted into a `functions.py` file, and credentials are securely stored in a JSON file for easy access and reuse.

---

## `crawl.py`

### Purpose:
The `crawl.py` script automates the process of logging into a web portal, navigating through multiple pages (Page 1, Page 2, and Page 3), and retrieving titles, links, and additional information from these pages. The gathered data is saved to corresponding text files (`page1.txt`, `page2.txt`, `page3.txt`).

### Main Functions:
1. **Login Automation**: Reads login credentials (MSSV and password) from a JSON file, logs into the student portal, and navigates to the regulations page.
2. **Data Extraction**: For each page, it scrapes the titles, links, and additional information from specific page elements.
3. **Write to File**: The extracted data is written to text files, with each page's data being saved into its own file (`page1.txt`, `page2.txt`, `page3.txt`).
4. **Navigation**: Automates the process of clicking through various pages on the site to extract the required data.

### How it Works:
- The script uses Selenium WebDriver to simulate human interactions with the website.
- Credentials are read from `credentials.json` via the `read_credentials` function from the `functions.py` module.
- Data extraction is done using the `get_title_link_info` function, and the output is saved via the `write_to_file` function.
- After scraping the data, the browser instance is gracefully closed.

### Key Code Sections:
- **Login**: Automatically fills out the login form with credentials from the JSON file.
- **Data Extraction**: Extracts titles, links, and department information from each page and saves them.
- **Page Navigation**: Iterates through multiple pages to gather data.

---

## `crawlOnePdf.py`

### Purpose:
The `crawlOnePdf.py` script extends the functionality of `crawl.py` by logging into the portal, navigating to a specific PDF document, and automatically scrolling through the entire PDF. This is particularly useful for handling multi-page PDFs embedded within a webpage.

### Main Functions:
1. **Login Automation**: Similar to `crawl.py`, this script reads credentials from a JSON file and logs into the student portal.
2. **PDF Navigation**: It locates and interacts with a PDF viewer on the regulations page, determines the number of pages in the PDF, and scrolls through each page.
3. **Scrolling Automation**: The script automates scrolling through the entire PDF and ensures that all content is loaded.

### How it Works:
- After logging in and navigating to the PDF link, the script identifies the PDF viewer container on the webpage.
- It extracts the total number of pages from the PDF viewer and uses the `scroll_pdf_viewer` function to scroll through each page.
- The browser is closed once the PDF is fully scrolled.

### Key Code Sections:
- **PDF Viewer**: Locates the PDF container and extracts the total number of pages from the element displaying "of X" where X is the total number of pages.
- **Scrolling**: Automates the scrolling process through each page of the PDF.
  
---

## `functions.py`

### Purpose:
The `functions.py` file contains reusable functions that are shared between `crawl.py` and `crawlOnePdf.py` for streamlined code maintenance and better modularity.

### Functions:
1. **`read_credentials(file_path)`**:
   - Reads the `mssv` (student ID) and `password` from a JSON file.
   - Returns the credentials for use in both scripts.
   - Example of JSON format:
     ```json
     {
         "mssv": "521H0517",
         "password": "****"
     }
     ```

2. **`get_title_link_info(driver, page_titles, page_link, page_phong)`**:
   - Extracts titles, links, and additional information (such as department or date) from a webpage.
   - Returns the data lists for further processing or writing to a file.

3. **`write_to_file(page_titles, page_link, page_phong, filename)`**:
   - Takes extracted data and writes it to a specified text file.
   - The file format includes numbered entries with titles, links, and additional information.

4. **`scroll_pdf_viewer(driver, container, scroll_height)`**:
   - Automates scrolling through a PDF viewer embedded on a webpage by a given scroll height.
   - Useful for navigating multi-page PDFs.

---

## `credentials.json`

### Purpose:
This file securely stores the login credentials for the student portal in a structured JSON format. It is read by the `read_credentials` function in `functions.py`.

### Example Content:
```json
{
    "mssv": "521H0517",
    "password": "****"
}
