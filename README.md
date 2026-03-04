# SafariBooks Downloader (UI + PDF Support)

Welcome to the SafariBooks Downloader! This project provides an easy-to-use graphical interface (built with PyQt6) to download books from Safari Books Online (O'Reilly Learning) and optionally convert them into beautiful PDFs. 

## Features
- **User-Friendly Desktop UI:** A simple interface to input your Book ID and paste your cookies.
- **EPUB and PDF Output:** Automatically generates an EPUB containing the book's content, and optionally converts it to a clean PDF with accurate page numbering (using PyPDF2 and ReportLab).
- **Cloudflare Bypass:** Integrates Cloudscraper to seamlessly retrieve content from the O'Reilly API.
- **Improved Formatting:** Fixes rendering issues on Apple Books by correctly defining character encoding and image aspect ratios.

## Setup and Installation

1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/prismaticamedia/Safaridownloader.git
   cd Safaridownloader
   ```
2. Install the required Python dependencies:
   ```bash
   pip3 install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python3 safaribooks_ui.py
   ```

## How to Use

1. **Get your Cookies**: Since the login endpoint is protected, you must log in to O'Reilly in your web browser and extract your session cookies.
2. **Paste Cookies**: Open the application, go to the "1. Paste Cookies" tab, paste your raw cookies, and click **Save cookies.json**.
3. **Download**: Navigate to the "2. Download Book" tab, enter the Book ID (e.g., `9781617299339`), choose whether you want a PDF generated, and click **Download**.

---

## Acknowledgments & Disclaimer

This tool is a heavily modified and modernized fork based on the incredible foundational work of [Lorenzo Di Fuccia's original safaribooks project](https://github.com/lorenzodifuccia/safaribooks). We have built upon their core logic to bring a desktop GUI and enhanced PDF capabilities.

### Important Disclaimer (adapted from the original author):
> Download and generate EPUB of your favorite books from Safari Books Online library.
> I'm not responsible for the use of this program, this is only for personal and educational purpose.
> Before any usage please read the O'Reilly's Terms of Service.
