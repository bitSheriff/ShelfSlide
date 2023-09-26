#!/bin/bash

# Path to the Python program
PROGRAM_PATH="$HOME/ShelfSlide/shelfslide.py"

# Name of the systemd service
SERVICE_NAME="shelfslide"

# Get the username of the person running the script
CURRENT_USER="$USER"

# Check if the service already exists
if systemctl is-active --quiet ${SERVICE_NAME}.service; then
  echo "The service ${SERVICE_NAME} already exists."
  exit 1
fi

# Check if the script is executed with root privileges
if [ "$EUID" -ne 0 ]; then
    echo "This script requires root privileges. Please run it as root."
    exit 1
fi

# Create the unit file
cat <<EOF > /etc/systemd/system/${SERVICE_NAME}.service
[Unit]
Description=ShelfSlide Python Program

[Service]
ExecStart=/usr/bin/python3 ${PROGRAM_PATH}
WorkingDirectory=$HOME/ShelfSlide
User=$CURRENT_USER
Group=$CURRENT_USER

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd
systemctl daemon-reload

# Enable and start the service
systemctl enable ${SERVICE_NAME}.service
systemctl start ${SERVICE_NAME}.service

# Display the status of the service
systemctl status ${SERVICE_NAME}.service
