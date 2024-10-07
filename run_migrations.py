import subprocess

def run_command(command):
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running command '{' '.join(command)}': {e}")
        raise

def run_migrations():
    # List of apps in the correct order
    apps = [
    'admission',
    'course',
    'exam',
    'fees',
    'institute',
    'library',
    'notice',
    'scholarship',
    'staff',
    'student',
    'subject',
    'task',
    'timetable',
    'accounts',   
    ]

    # Make migrations for each app
    for app in apps:
        print(f"Making migrations for {app}...")
        run_command(['python3', 'manage.py', 'makemigrations', app])

    # Migrate for each app
    for app in apps:
        print(f"Running migrations for {app}...")
        run_command(['python3', 'manage.py', 'migrate', app])

    print("All migrations completed successfully.")

if __name__ == "__main__":
    run_migrations()
