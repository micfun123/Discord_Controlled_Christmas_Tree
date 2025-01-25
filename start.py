import os

SERVICE_NAME = "discordbot"
SERVICE_PATH = f"/etc/systemd/system/{SERVICE_NAME}.service"
DISCORD_BOT_DIR = "/root/Discord_Controlled_Christmas_Tree"
BOT_SCRIPT = f"{DISCORD_BOT_DIR}/discord/main.py"

# The service content
SERVICE_CONTENT = f"""[Unit]
Description=Discord Bot
After=network.target

[Service]
ExecStart=/usr/bin/python3 {BOT_SCRIPT}
WorkingDirectory={DISCORD_BOT_DIR}
User=root
Restart=always

[Install]
WantedBy=multi-user.target
"""

def install_dependencies():
    """Install required Python libraries."""
    print("Installing discord.py...")
    os.system("pip3 install discord")

def create_service_file():
    """Create the systemd service file."""
    print(f"Creating service file at {SERVICE_PATH}...")
    with open(SERVICE_PATH, "w") as f:
        f.write(SERVICE_CONTENT)
    
    os.system("chmod 644 " + SERVICE_PATH)

def enable_and_start_service():
    """Enable and start the systemd service."""
    print("Reloading systemd daemon...")
    os.system("systemctl daemon-reload")
    print("Enabling the Discord bot service...")
    os.system(f"systemctl enable {SERVICE_NAME}")
    print("Starting the Discord bot service...")
    os.system(f"systemctl start {SERVICE_NAME}")

def main():
    install_dependencies()
    create_service_file()
    enable_and_start_service()
    print("Setup complete. Check the service status with:")
    print(f"  sudo systemctl status {SERVICE_NAME}")

if __name__ == "__main__":
    main()
