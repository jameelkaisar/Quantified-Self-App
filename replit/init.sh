#! /bin/sh

# Clone the repository
git clone https://github.com/JameelKaisar/Quantified-Self-App.git

# Change directory to project folder
cd Quantified-Self-App

# Install the dependencies
pip install -r requirements.txt

# Initialize the application
python3 app_init.py

# Start the application
python3 app_run.py
