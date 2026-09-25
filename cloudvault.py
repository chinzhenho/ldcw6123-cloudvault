"""
CloudVault - Cloud Storage Simulator
LDCW6123 Fundamentals of Digital Competence for Programmer - Group Project Part 2

Technology  : Cloud Computing
Application : Cloud Storage (inspired by Google Drive, OneDrive, Dropbox)

CloudVault simulates a cloud storage service. Users can upload, delete,
search and view files, and monitor how much storage is used.
Run: python cloudvault.py
"""

# os: turns on colours in the terminal | re: checks the input format
import os
import re

# Turn on colour support in the Windows terminal
os.system("")

# ===========================================================================
# SECTION 1: SETTINGS
# Fixed values used by the whole program: storage size, warning levels,
# file categories, colours and input rules.
# ===========================================================================
STORAGE_CAPACITY_MB = 1000   # total storage: 1000 MB
WARNING_PERCENT = 70         # 70% used -> warning
CRITICAL_PERCENT = 90        # 90% used -> critical

# Each category and the file types it accepts (other types go to "Other")
CATEGORY_EXTENSIONS = {
    "Documents": ["pdf", "docx", "txt"],
    "Images": ["jpg", "png"],
    "Videos": ["mp4", "mov"],
}
CATEGORIES = ["Documents", "Images", "Videos", "Other"]

# Colour codes for the terminal text and progress bars
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
GREY = "\033[90m"
RESET = "\033[0m"

# Input rules: only letters and numbers are allowed
ALNUM_PATTERN = re.compile(r"^[A-Za-z0-9]+$")
# File name rule: name + dot + file type, e.g. report.pdf
FILE_NAME_PATTERN = re.compile(r"^[A-Za-z0-9]+\.[A-Za-z0-9]+$")
MAX_NAME_LENGTH = 25         # longest file name allowed

# ===========================================================================
# SECTION 2: CLOUD STORAGE DATA
# A list of files already stored in the cloud (595 MB at the start).
# Each file has a name, a size in MB and a category.
# ===========================================================================
cloud_files = [
    {"name": "assignment.pdf", "size": 45, "category": "Documents"},
    {"name": "lecturenotes.docx", "size": 60, "category": "Documents"},
    {"name": "todo.txt", "size": 15, "category": "Documents"},
    {"name": "holiday.jpg", "size": 50, "category": "Images"},
    {"name": "profile.png", "size": 35, "category": "Images"},
    {"name": "presentation.mp4", "size": 350, "category": "Videos"},
    {"name": "projectbackup.zip", "size": 40, "category": "Other"},
]


# ===========================================================================
# SECTION 3: INPUT FUNCTIONS (ERROR HANDLING)
# These functions keep asking again until the user enters a valid input,
# so the program never crashes because of wrong input.
# ===========================================================================
def ask_alnum(prompt):
    """Accept letters and numbers only. Used for menu choices."""
    while True:
        text = input(prompt).strip()
        if ALNUM_PATTERN.match(text):
            return text
        print("  Invalid input. Use letters and numbers only. Please try again.")


def ask_file_name(prompt):
    """Accept a valid file name like report.pdf (max 25 characters), or 0 to cancel."""
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
    """Accept whole numbers only. Used for file size and file number."""
    while True:
        text = input(prompt).strip()
        if text.isdigit() and text.isascii():
            return int(text)
        print("  Invalid input. Enter numbers only, e.g. 25. Please try again.")


def ask_yes_no(prompt):
    """Accept y or n only. Used to confirm before deleting a file."""
    while True:
        answer = input(prompt).strip().lower()
        if answer in ("y", "n"):
            return answer == "y"
        print("  Invalid input. Enter y or n. Please try again.")


def pause():
    """Wait for Enter so the user can read the result."""
    input("\nPress Enter to return to the dashboard...")


# ===========================================================================
# SECTION 4: HELPER FUNCTIONS
# Small functions that do calculations and display tasks.
# The main functions reuse them.
# ===========================================================================
def get_category(file_name):
    """Find a file's category from its file type, e.g. report.pdf -> Documents."""
    extension = file_name.rsplit(".", 1)[1].lower()
    for category, extensions in CATEGORY_EXTENSIONS.items():
        if extension in extensions:
            return category
    return "Other"


def get_used_storage():
    """Add up the size of all files to get the storage used."""
    return sum(file["size"] for file in cloud_files)


def get_usage_percent():
    """Calculate the storage used as a percentage: used / 1000 x 100."""
    return get_used_storage() / STORAGE_CAPACITY_MB * 100


def get_storage_status(percent):
    """Return the status: Normal (0-69%), Warning (70-89%) or Critical (90-100%)."""
    if percent >= CRITICAL_PERCENT:
        return "[CRITICAL]"
    elif percent >= WARNING_PERCENT:
        return "[WARNING]"
    else:
        return "[NORMAL]"


def get_status_colour(percent):
    """Return the bar colour: green (0-69%), yellow (70-89%) or red (90-100%)."""
    if percent >= CRITICAL_PERCENT:
        return RED
    elif percent >= WARNING_PERCENT:
        return YELLOW
    else:
        return GREEN


def draw_bar_only(percent, colour=GREEN, width=30):
    """Draw a coloured progress bar, e.g. ██████░░░░."""
    filled = int(round(percent / 100 * width))
    return colour + "█" * filled + GREY + "░" * (width - filled) + RESET


def draw_bar(percent, colour=GREEN, width=30):
    """Draw a progress bar with the percentage, e.g. ██████░░░░ 12.0%."""
    return f"{draw_bar_only(percent, colour, width)} {percent:5.1f}%"


def find_file(file_name):
    """Check if a file name already exists. Used to stop duplicate names."""
    for file in cloud_files:
        if file["name"].lower() == file_name.lower():
            return file
    return None


def print_file_table(files):
    """Show files in a table with No., File Name, Category and Size."""
    print(f"  {'No.':<4}{'File Name':<28}{'Category':<12}{'Size (MB)':>10}")
    print("  " + "-" * 54)
    for number, file in enumerate(files, start=1):
        print(f"  {number:<4}{file['name']:<28}{file['category']:<12}{file['size']:>10}")


# ===========================================================================
# SECTION 5: STORAGE WARNING
# Alerts the user when storage reaches 70% (warning) or 90% (critical).
# ===========================================================================
def check_storage_warning():
    """Show a yellow warning at 70% or a red critical alert at 90%."""
    percent = get_usage_percent()
    if percent >= CRITICAL_PERCENT:
        print(f"\n  {RED}!!! CRITICAL: Storage is {percent:.1f}% full. "
              f"Delete files to free up space.{RESET}")
    elif percent >= WARNING_PERCENT:
        print(f"\n  {YELLOW}!   WARNING: Storage is {percent:.1f}% full. "
              f"You are running low on space.{RESET}")


# ===========================================================================
# SECTION 6: MAIN FUNCTIONS (the 6 menu options)
# ===========================================================================

# ---------------------------------------------------------------------------
# FUNCTION 1: UPLOAD FILE
# The user chooses a category, enters a file name and a file size.
# The program checks the input, then saves the file to the cloud.
# ---------------------------------------------------------------------------
def ask_category():
    """Upload step 1: the user chooses a category."""
    print("\nStep 1 of 3: Choose a category")
    print("  1. Documents  (.pdf, .docx, .txt)")
    print("  2. Images     (.jpg, .png)")
    print("  3. Videos     (.mp4, .mov)")
    print("  4. Other      (.zip or any other file type)")
    print("  0. Cancel")
    while True:
        choice = ask_alnum("Enter category number (0-4): ")
        if choice in ("1", "2", "3", "4"):
            return CATEGORIES[int(choice) - 1]
        if choice == "0":
            return None
        print("  Invalid choice. Enter a number from 0 to 4. Please try again.")


def ask_upload_name(category):
    """Upload step 2: the user enters a file name that matches the category."""
    if category == "Other":
        allowed_text = ".zip or any type not listed in the other categories"
        example = "backup.zip"
    else:
        allowed_text = ", ".join("." + ext for ext in CATEGORY_EXTENSIONS[category])
        example = "myfile." + CATEGORY_EXTENSIONS[category][0]

    print("\nStep 2 of 3: Enter the file name")
    print("  - Use letters and numbers only, then a dot and the file type")
    print(f"  - Maximum {MAX_NAME_LENGTH} characters")
    print(f"  - Allowed file types for {category}: {allowed_text}")
    print(f"  - Example: {example}")
    print("  - Enter 0 to cancel")

    while True:
        file_name = ask_file_name("File name: ")
        if file_name == "0":
            return None
        if get_category(file_name) != category:
            # Wrong file type for this category
            extension = file_name.rsplit(".", 1)[1].lower()
            print(f"  '.{extension}' is not allowed for {category}. "
                  f"Allowed: {allowed_text}. Please try again.")
        elif find_file(file_name) is not None:
            # File name already exists
            print(f"  '{file_name}' already exists in CloudVault. "
                  "Please enter a different name.")
        else:
            return file_name


def ask_upload_size():
    """Upload step 3: the user enters a size that fits in the space left."""
    available = STORAGE_CAPACITY_MB - get_used_storage()
    print("\nStep 3 of 3: Enter the file size")
    print("  - Whole number in MB, e.g. 25")
    print(f"  - Available storage: {available} MB")
    print("  - Enter 0 to cancel")

    while True:
        size = ask_whole_number("File size (MB): ")
        if size == 0:
            return None
        if size <= available:
            return size
        print(f"  Not enough storage. The file must be {available} MB or less. "
              "Please try again.")


def upload_file():
    """Run the 3 upload steps, save the file and check the storage status."""
    print("\n=== UPLOAD FILE ===")
    # Stop if the storage is already full
    if get_used_storage() >= STORAGE_CAPACITY_MB:
        print("  Storage is full. Delete some files before uploading.")
        return

    category = ask_category()
    if category is None:
        print("  Upload cancelled.")
        return

    file_name = ask_upload_name(category)
    if file_name is None:
        print("  Upload cancelled.")
        return

    size = ask_upload_size()
    if size is None:
        print("  Upload cancelled.")
        return

    # Save the new file into the cloud storage list
    cloud_files.append({"name": file_name, "size": size, "category": category})
    print("\n  Upload successful!")
    print(f"  File     : {file_name}")
    print(f"  Category : {category}")
    print(f"  Size     : {size} MB")
    print(f"  Storage used: {get_used_storage()} / {STORAGE_CAPACITY_MB} MB")
    check_storage_warning()


# ---------------------------------------------------------------------------
# FUNCTION 2: DELETE FILE
# The user picks a file by its number, confirms with y/n,
# and the file is removed to free up space.
# ---------------------------------------------------------------------------
def delete_file():
    """Remove a file chosen by the user after confirmation."""
    print("\n=== DELETE FILE ===")
    if len(cloud_files) == 0:
        print("  CloudVault is empty. Nothing to delete.")
        return

    print_file_table(cloud_files)
    print("\nEnter 0 to cancel.")

    # Ask until the user picks a file number that exists
    while True:
        number = ask_whole_number("Enter the No. of the file to delete: ")
        if number == 0:
            print("  Delete cancelled.")
            return
        if 1 <= number <= len(cloud_files):
            break
        print(f"  No such file. Enter a number from 1 to {len(cloud_files)}.")

    file = cloud_files[number - 1]
    if ask_yes_no(f"Delete '{file['name']}' ({file['size']} MB)? (y/n): "):
        cloud_files.remove(file)
        print(f"  Deleted '{file['name']}'. Freed {file['size']} MB.")
        print(f"  Storage used: {get_used_storage()} / {STORAGE_CAPACITY_MB} MB")
        check_storage_warning()
    else:
        print("  Delete cancelled.")


# ---------------------------------------------------------------------------
# FUNCTION 3: SEARCH FILES
# The user types a keyword, file name or category,
# and the program shows all matching files.
# ---------------------------------------------------------------------------
def search_files():
    """Find files by keyword (e.g. holiday), file name or category (e.g. videos)."""
    print("\n=== SEARCH FILES ===")
    while True:
        keyword = input("Enter file name or keyword (e.g. holiday, holiday.jpg, videos): ").strip()
        if ALNUM_PATTERN.match(keyword) or FILE_NAME_PATTERN.match(keyword):
            keyword = keyword.lower()
            break
        print("  Invalid input. Use letters and numbers only (a file name may "
              "include one dot, e.g. holiday.jpg). Please try again.")

    # Keep only the files that match the keyword
    results = [file for file in cloud_files
               if keyword in file["name"].lower() or keyword == file["category"].lower()]

    if len(results) == 0:
        print(f"  No files found matching '{keyword}'.")
    else:
        print(f"  Found {len(results)} file(s):\n")
        print_file_table(results)


# ---------------------------------------------------------------------------
# FUNCTION 4: VIEW FILES
# Shows all files stored in the cloud with the total size.
# ---------------------------------------------------------------------------
def view_files():
    """List all stored files, the number of files and the total size."""
    print("\n=== ALL FILES ===")
    if len(cloud_files) == 0:
        print("  CloudVault is empty.")
        return
    print_file_table(cloud_files)
    print(f"\n  Total: {len(cloud_files)} file(s), {get_used_storage()} MB")


# ---------------------------------------------------------------------------
# FUNCTION 5: STORAGE MONITOR
# Shows used and available storage, a progress bar and the storage status.
# ---------------------------------------------------------------------------
def storage_monitor():
    """Show capacity, used and available storage, progress bar and status."""
    print("\n=== STORAGE MONITOR ===")
    used = get_used_storage()
    percent = get_usage_percent()
    print(f"  Capacity  : {STORAGE_CAPACITY_MB} MB")
    print(f"  Used      : {used} MB")
    print(f"  Available : {STORAGE_CAPACITY_MB - used} MB")
    print(f"  Usage     : {draw_bar(percent, get_status_colour(percent))}")
    print(f"  Status    : {get_storage_status(percent)}")
    print("\n  Status guide: 0-69% Normal | 70-89% Warning | 90-100% Critical")
    check_storage_warning()


# ---------------------------------------------------------------------------
# FUNCTION 6: STORAGE BREAKDOWN
# Shows how much storage each category uses, with a coloured progress bar
# and percentage for each category.
# ---------------------------------------------------------------------------
def storage_breakdown():
    """Show a table of each category's size, progress bar and percentage."""
    print("\n=== STORAGE BREAKDOWN ===")
    print("  Category % = share of the storage currently used")
    print(f"  Total %    = storage used out of the {STORAGE_CAPACITY_MB} MB capacity")
    print(f"  Colour     = {GREEN}Green{RESET} 0-69%  |  "
          f"{YELLOW}Yellow{RESET} 70-89%  |  {RED}Red{RESET} 90-100%\n")

    # Bar colour depends on usage: green (<70%), yellow (70-89%), red (90%+)
    bar_width = 30
    line = "  +" + "-" * 12 + "+" + "-" * 9 + "+" + "-" * (bar_width + 2) + "+" + "-" * 9 + "+"

    print(line)
    print(f"  | {'Category':<10} | {'Size':>7} | {'Usage':<{bar_width}} | {'Percent':>7} |")
    print(line)
    # One row for each category
    for category in CATEGORIES:
        category_size = sum(file["size"] for file in cloud_files
                            if file["category"] == category)
        used = get_used_storage()
        percent = category_size / used * 100 if used > 0 else 0
        bar = draw_bar_only(percent, get_status_colour(percent), bar_width)
        print(f"  | {category:<10} | {category_size:>4} MB | {bar} | {percent:>6.1f}% |")
        print(line)

    # Total row: storage used out of 1000 MB
    total_percent = get_usage_percent()
    total_bar = draw_bar_only(total_percent, get_status_colour(total_percent), bar_width)
    print(f"  | {'Total':<10} | {get_used_storage():>4} MB | {total_bar} | {total_percent:>6.1f}% |")
    print(line)


# ===========================================================================
# SECTION 7: DASHBOARD AND MAIN PROGRAM
# Shows the menu, runs the function the user chooses,
# then returns to the menu until the user chooses 0 to exit.
# ===========================================================================
def show_dashboard():
    """Show the main menu with the current storage usage and status."""
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
    """Main loop: show the menu, run the chosen function, repeat until exit."""
    print("Welcome to CloudVault - manage your files in the cloud.")
    while True:
        show_dashboard()

        # Ask until the user enters a valid menu option
        while True:
            choice = ask_alnum("Choose a function (0-6): ")
            if choice in ("0", "1", "2", "3", "4", "5", "6"):
                break
            print("  Invalid choice. Enter a number from 0 to 6. Please try again.")

        # Run the function the user chose
        if choice == "1":
            upload_file()
        elif choice == "2":
            delete_file()
        elif choice == "3":
            search_files()
        elif choice == "4":
            view_files()
        elif choice == "5":
            storage_monitor()
        elif choice == "6":
            storage_breakdown()
        else:
            # Choice 0: exit the program
            print("Thank you for using CloudVault. Goodbye!")
            break
        pause()


# Start the program
if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        # Exit cleanly if the user presses Ctrl+C
        print("\nCloudVault closed. Goodbye!")
