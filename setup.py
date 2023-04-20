import os
import sys
import subprocess


def run_command(command):
    if command.startswith("flask"):
        command = "python -m " + command
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        print(f"Error: {stderr.decode('utf-8')}")
    else:
        print(stdout.decode('utf-8'))



def main():
    # Check Python version
    if sys.version_info < (3, 6):
        print("Error: Python 3.6 or higher is required.")
        sys.exit(1)

    # Install required libraries
    print("Installing required libraries...")
    run_command("pip install flask flask-sqlalchemy flask-migrate flask-cors discord.py requests")

    # Initialize the database
    print("Initializing the database...")
    run_command("flask db init")
    run_command("flask db migrate")
    run_command("flask db upgrade")

    # Start the server
    print("Starting the server...")
    run_command("set FLASK_APP=discord_mmo_server.py")
    run_command("flask run")


if __name__ == "__main__":
    main()
