import os
import subprocess

# 1. Pull your secrets
api_key = os.getenv("STEAM_API_KEY")
targets_secret = os.getenv("STEAM_TARGET_USERS")
smtp_password = os.getenv("SMTP_PASSWORD")
smtp_user = os.getenv("SMTP_USER")
receiver_email = os.getenv("RECEIVER_EMAIL")

if not api_key or not targets_secret or not smtp_password:
    print("System Error: Required secrets are missing.")
    exit(1)

# Write the API key to the hidden environment file
with open(".env", "w") as env_file:
    env_file.write(f"STEAM_API_KEY={api_key}\n")
    env_file.write(f"SMTP_PASSWORD={smtp_password}\n")

# 3. DYNAMIC INJECTION: Overwrite the fake emails in the config file
# (Note: Ensure "config.py" matches the actual name of your configuration file)
config_filename = "steam_monitor.conf"

if os.path.exists(config_filename):
    # Read the dummy file from the public repository
    with open(config_filename, "r") as file:
        config_data = file.read()

    # Swap the placeholder text with your secure hidden variables
    config_data = config_data.replace('"your_smtp_user"', f'"{smtp_user}"')
    config_data = config_data.replace('"your_receiver_email"', f'"{receiver_email}"')

    # Save the file locally on the temporary cloud machine
    with open(config_filename, "w") as file:
        file.write(config_data)
else:
    print(f"Warning: {config_filename} not found. Skipping dynamic injection.")

# Split the comma-separated secret into a usable Python list
target_list = [t.strip() for t in targets_secret.split(",")]

print("Starting Silent Cloud Tracker...")
print("Privacy Mode ENABLED: Console logs are suppressed. Relying on email alerts.")

# 2. Launch trackers in parallel using subprocess.Popen (Background Processes)
active_processes = []

for target in target_list:
    # Execute steam_monitor but FORCE the output into the void (DEVNULL)
    # This prevents the public GitHub logs from capturing any user data or activity
    p = subprocess.Popen(
        ["steam_monitor", target],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    active_processes.append(p)

# 3. Keep the main script alive while the background trackers run
for p in active_processes:
    p.wait()
