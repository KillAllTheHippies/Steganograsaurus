# Image Steganography Application

A GUI application for encoding and decoding text messages in images using LSB (Least Significant Bit) and alpha channel steganography.

## Features

Functionality:
- LSB encoding (RGB channels)
- Alpha channel encoding
- Message decoding
- Image format validation
- Capacity calculation
- Image preview generation

Compatible Image Types:
- PNG
- BMP
- TIFF
- WEBP (RGB/RGBA only)

### User Interface
- **Modern Look and Feel:** The application sports a clean, dark theme for improved aesthetics.
- **Customizable Layout:** Features dockable widgets for the image preview, message input area, and encoding options, allowing you to arrange the workspace to your preference.

## Requirements
- Python 3.8+
- PyQt5
- Pillow (Version 9.5.0 recommended for PyQt5 compatibility with ImageQt)
- NumPy

## Setup and Run with Ubuntu Script (`run_steganography_app.sh`)

For users on Ubuntu, a helper script `run_steganography_app.sh` is provided to simplify the setup and launch process. This script is particularly useful for setting up the `ui-revamp` branch of the application which includes the latest UI changes and dependencies.

**Script Content:**
```bash
#!/bin/bash -e

# Define repository URL and branch name
REPO_URL="https://github.com/your-username/your-repository-name.git" # IMPORTANT: Replace with your actual Git repository URL
BRANCH_NAME="ui-revamp" # Branch with the latest UI and features
APP_DIR="image-steganography-app" # Local directory for the app

# 0. Inform user about script actions
echo "This script will perform the following actions:"
echo "1. Clone or update the repository from $REPO_URL into the '$APP_DIR' directory."
echo "2. Check out the '$BRANCH_NAME' branch."
echo "3. Install system dependencies for PyQt5 and GUI elements (may require sudo)."
echo "4. Create/activate a Python virtual environment in '$APP_DIR/$VENV_DIR'."
echo "5. Install Python dependencies from 'image_steganography/requirements.txt'."
echo "6. Launch the Image Steganography application."
echo "--------------------------------------------------------------------------"
read -p "Do you want to continue? (y/N): " confirmation
if [[ "$confirmation" != "y" && "$confirmation" != "Y" ]]; then
    echo "Aborted by user."
    exit 0
fi

# 1. Clone or update the repository
if [ -d "$APP_DIR" ]; then
    echo "Repository directory '$APP_DIR' already exists. Pulling latest changes..."
    cd "$APP_DIR"
    # Stash any local changes before attempting to pull or checkout
    git stash push -m "Autostash before script update" || true
    git fetch origin
    # Ensure main branch exists and is up-to-date before switching
    if git branch -r --list "origin/main" > /dev/null; then
        git checkout main
        git pull origin main
    else
        echo "Warning: 'main' branch not found on remote. Attempting to continue with current branch for update."
    fi
else
    echo "Cloning repository into '$APP_DIR'..."
    git clone "$REPO_URL" "$APP_DIR"
    cd "$APP_DIR"
fi

# 2. Check out the specified branch
echo "Checking out '$BRANCH_NAME' branch..."
if git rev-parse --verify "$BRANCH_NAME" > /dev/null 2>&1; then
    git checkout "$BRANCH_NAME"
else
    echo "Branch '$BRANCH_NAME' does not exist locally. Attempting to check out from remote 'origin/$BRANCH_NAME'..."
    git checkout -t "origin/$BRANCH_NAME" || { echo "Error: Branch '$BRANCH_NAME' not found locally or on remote. Please check the branch name and repository URL."; exit 1; }
fi
git pull origin "$BRANCH_NAME" # Ensure it's up-to-date

# 3. Install system dependencies for PyQt5 and other GUI elements
echo "Installing system dependencies (may require sudo)..."
sudo apt-get update
sudo apt-get install -y python3-pyqt5 python3-dev libxcb-xinerama0 libqt5gui5 libxkbcommon-x11-0 xvfb

# 4. Create a Python virtual environment
VENV_DIR=".venv"
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating Python virtual environment in '$PWD/$VENV_DIR'..."
    python3 -m venv "$VENV_DIR"
fi

# Activate the virtual environment
echo "Activating virtual environment..."
source "$VENV_DIR/bin/activate"

# 5. Install Python dependencies
echo "Installing Python dependencies from image_steganography/requirements.txt..."
# The script is inside APP_DIR at this point.
if [ -f "image_steganography/requirements.txt" ]; then
    pip install -r image_steganography/requirements.txt
    # Pillow 9.5.0 is known to work with PyQt5 for ImageQt
    pip install "Pillow==9.5.0"
else
    echo "Error: 'image_steganography/requirements.txt' not found. Please ensure the repository structure is correct."
    deactivate
    exit 1
fi

# 6. Launch the application using Xvfb for headless environments if needed
echo "Launching the Image Steganography application..."
# Check if DISPLAY is set. If not, and Xvfb is installed, use it.
if [ -z "$DISPLAY" ] && command -v xvfb-run > /dev/null; then
    echo "No display detected. Attempting to launch with Xvfb..."
    xvfb-run python image_steganography/main.py
else
    python image_steganography/main.py
fi

echo "Application closed."
deactivate
echo "Virtual environment deactivated."
```

**How to Use:**
1.  **Save the script:** Copy the content above and save it to a file named `run_steganography_app.sh` in your desired location (e.g., your home directory).
2.  **Replace Placeholder URL:** Open the script with a text editor and **IMPORTANTLY** replace `https://github.com/your-username/your-repository-name.git` with the actual HTTPS or SSH URL of this Git repository.
3.  **Make it executable:** Open your terminal, navigate to where you saved the script, and run:
    ```bash
    chmod +x run_steganography_app.sh
    ```
4.  **Run the script:** Execute the script from your terminal:
    ```bash
    ./run_steganography_app.sh
    ```
The script will guide you through:
    - Creating a directory named `image-steganography-app`.
    - Cloning the repository into it (or updating it if it already exists).
    - Checking out the correct branch (`ui-revamp`).
    - Installing all necessary system and Python dependencies (including a specific Pillow version for compatibility).
    - Launching the application (using Xvfb if no display is detected, useful for some environments).

## Notes
- For LSB encoding, use lossless formats like PNG.
- For alpha channel encoding, use images with transparency.
- Larger images can store more data.
- The application shows the maximum message capacity for the selected image and method.

## License
MIT License
