# Naukri Profile Updater

**Objective:**  
Automatically refresh your Naukri profile daily to update the "last updated" timestamp. This helps improve your visibility to recruiters and potentially increases your chances of being shortlisted for job opportunities.

## Overview
This script logs into Naukri, navigates to your profile update section, and uploads your resume—ensuring your profile appears current to recruiters. Optionally, it can modify your resume by embedding hidden text (controlled by a flag), though by default it simply uploads the existing file.

## Prerequisites
- Python 3.x
- Google Chrome installed
- Required Python packages:
  - `selenium`
  - `webdriver_manager`
  - `pypdf`
  - `reportlab`

## Setup
1. **Clone or Download the Script:**  
   Save the provided Python script `NaukriProfileAutomation.py` to your machine.

2. **Install Dependencies:**  
   Create and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate   # On Windows use: .\venv\Scripts\activate
   ```
   Then install required packages:
   ```bash
   pip install selenium webdriver_manager pypdf reportlab
   ```

3. **Configure the Script:**  
   - Update the resume paths (`originalResumePath` and `modifiedResumePath`) to point to your resume file.
   - Enter your Naukri username, password, and mobile number(not used in profile update anymore)) in the script.
   - Set `updatePDF = False` if you wish to upload the resume without modification.
   - Set `headless = False` to see the browser; change to `True` to run Chrome without a GUI.

## Usage
Run the script using:
```bash
python NaukriProfileAutomation.py
```

## Notes
- Ensure your file permissions allow the script to read your resume and write updates.
- Use at your own risk; secure your credentials appropriately.

![python](https://img.shields.io/badge/Python-1f405f.svg)
![selenium](https://img.shields.io/badge/Selenium-1f425f.svg)
