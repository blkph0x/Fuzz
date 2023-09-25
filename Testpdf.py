import os
import time
import pygetwindow as gw
import pyautogui

# Define the path to the folder containing the test cases
testcase_folder = 'testcases'

# List all PDF files in the folder
pdf_files = [file for file in os.listdir(testcase_folder) if file.endswith(".pdf")]

# Function to close the currently focused window using ALT+F4
def close_current_window():
    pyautogui.hotkey('alt', 'f4')

# Iterate through each PDF file and open, check, and close automatically
for pdf_file in pdf_files:
    pdf_path = os.path.join(testcase_folder, pdf_file)
    
    try:
        # Open the PDF file with the default PDF viewer
        os.startfile(pdf_path)
        print(f"Opened: {pdf_file}")
        
        # Wait for a few seconds (adjust the duration as needed)
        time.sleep(5)  # Wait for 5 seconds for observation
        
        # Check for errors or crashes here (you can use pyautogui to interact with the PDF viewer)
        # For example, you can look for specific GUI elements or conditions
        
        # Close the PDF file automatically using pygetwindow
        pdf_window = gw.getWindowsWithTitle(pdf_file)
        if pdf_window:
            pdf_window[0].close()
        
    except Exception as e:
        # Handle errors or crashes here
        print(f"Error/Crash in: {pdf_file}")

print("All test cases processed.")
