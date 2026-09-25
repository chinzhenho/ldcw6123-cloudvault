"""
CloudVault - Cloud Storage Simulator
LDCW6123 Fundamentals of Digital Competence for Programmer - Group Project Part 2

Technology  : Cloud Computing
Application : Cloud Storage (inspired by Google Drive, OneDrive, Dropbox)

CloudVault simulates how a cloud storage service lets users manage files
remotely while monitoring the available storage capacity.
Run: python cloudvault.py
"""

import os
import re

# Turn on colour support in the Windows terminal
os.system("")

# ---------------------------------------------------------------------------
# Settings
# ---------------------------------------------------------------------------
STORAGE_CAPACITY_MB = 1000
WARNING_PERCENT = 70
CRITICAL_PERCENT = 90

# File extensions that belong to each category (anything else is "Other")
CATEGORY_EXTENSIONS = {
    "Documents": ["pdf", "docx", "txt"],
    "Images": ["jpg", "png"],
    "Videos": ["mp4", "mov"],
}
CATEGORIES = ["Documents", "Images", "Videos", "Other"]

# Terminal colours for the progress bars
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
GREY = "\033[90m"
RESET = "\033[0m"

# Input rules: letters and numbers only
ALNUM_PATTERN = re.compile(r"^[A-Za-z0-9]+$")
# File name rule: letters/numbers, one dot, then letters/numbers (e.g. report.pdf)
FILE_NAME_PATTERN = re.compile(r"^[A-Za-z0-9]+\.[A-Za-z0-9]+$")
MAX_NAME_LENGTH = 25

# Files already stored in the cloud when the program starts (sample data)
cloud_files = [
    {"name": "assignment.pdf", "size": 45, "category": "Documents"},
    {"name": "lecturenotes.docx", "size": 60, "category": "Documents"},
    {"name": "todo.txt", "size": 15, "category": "Documents"},
    {"name": "holiday.jpg", "size": 50, "category": "Images"},
    {"name": "profile.png", "size": 35, "category": "Images"},
    {"name": "presentation.mp4", "size": 350, "category": "Videos"},
    {"name": "projectbackup.zip", "size": 40, "category": "Other"},
]


# ---------------------------------------------------------------------------
# Input functions (keep asking until the input is valid)
# ---------------------------------------------------------------------------
def ask_alnum(prompt):
    """Ask until the user enters letters and numbers only."""
    while True:
        text = input(prompt).strip()
        if ALNUM_PATTERN.match(text):
            return text
        print("  Invalid input. Use letters and numbers only. Please try again.")


def ask_file_name(prompt):
    """Ask until the user enters a valid file name like report.pdf, or 0 to cancel."""
    while True:
        text = input(prompt).strip()
        if text == "0":
            return text
        if not FILE_NAME_PATTERN.match(text):
            print("  Invalid file name. Use letters and numbers with an extension, "
                  "e.g. report.pdf. Please try again.")
        elif len(text) > MAX_NAME_LENGTH:
            print(f"  File name is too long. Use {MAX_NAME_LENGTH} characters or fewer. "
                  "Please try again.")
        else:
            return text


def ask_whole_number(prompt):
    """Ask until the user enters a whole number (digits only)."""
    while True:
        text = input(prompt).strip()
        if text.isdigit() and text.isascii():
            return int(text)
        print("  Invalid input. Enter numbers only, e.g. 25. Please try again.")


def ask_yes_no(prompt):
    """Ask until the user enters y or n."""
    while True:
        answer = input(prompt).strip().lower()
        if answer in ("y", "n"):
            return answer == "y"
        print("  Invalid input. Enter y or n. Please try again.")


def pause():
    input("\nPress Enter to return to the dashboard...")


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------
def get_category(file_name):
    """Return the category of a file based on its extension."""
    extension = file_name.rsplit(".", 1)[1].lower()
    for category, extensions in CATEGORY_EXTENSIONS.items():
        if extension in extensions:
            return category
    return "Other"


def get_used_storage():
    """Return the total storage used in MB."""
    return sum(file["size"] for file in cloud_files)


def get_usage_percent():
    """Return the storage used as a percentage of capacity."""
    return get_used_storage() / STORAGE_CAPACITY_MB * 100


def get_storage_status(percent):
    """Return the storage status label for a usage percentage."""
    if percent >= CRITICAL_PERCENT:
        return "[CRITICAL]"
    elif percent >= WARNING_PERCENT:
        return "[WARNING]"
    else:
        return "[NORMAL]"


def find_file(file_name):
    """Return the file with this exact name (case-insensitive), or None."""
    for file in cloud_files:
        if file["name"].lower() == file_name.lower():
            return file
    return None


def print_file_table(files):
    """Print a list of files as a table."""
    print(f"  {'No.':<4}{'File Name':<28}{'Category':<12}{'Size (MB)':>10}")
    print("  " + "-" * 54)
    for number, file in enumerate(files, start=1):
        print(f"  {number:<4}{file['name']:<28}{file['category']:<12}{file['size']:>10}")


# ---------------------------------------------------------------------------
# Dashboard (main menu)
# ---------------------------------------------------------------------------
def show_dashboard():
    percent = get_usage_percent()
    print("\n" + "=" * 50)
    print("       CLOUDVAULT - Cloud Storage Simulator")
    print("=" * 50)
    print(f"  Storage: {get_used_storage()} / {STORAGE_CAPACITY_MB} MB "
          f"({percent:.1f}%)  {get_storage_status(percent)}")
    print("-" * 50)
    print("  1. Upload File")
    print("  2. Delete File")
    print("  3. Search Files")
    print("  4. View Files")
    print("  5. Storage Monitor")
    print("  6. Storage Breakdown")
    print("  0. Exit")
    print("-" * 50)


def main():
    print("Welcome to CloudVault - manage your files in the cloud.")
    while True:
        show_dashboard()

        # Ask until the user enters a valid menu option
        while True:
            choice = ask_alnum("Choose a function (0-6): ")
            if choice in ("0", "1", "2", "3", "4", "5", "6"):
                break
            print("  Invalid choice. Enter a number from 0 to 6. Please try again.")

        print("  This function is coming soon.")
        pause()


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        # Exit cleanly if the user presses Ctrl+C
        print("\nCloudVault closed. Goodbye!")