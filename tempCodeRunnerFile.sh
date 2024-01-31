#!/bin/bash

# Set environment variables
export FLASK_APP=main
export PYTHONPATH=.:$PYTHONPATH

# Check if sqlite3 is installed
if ! command -v sqlite3 &> /dev/null; then
    echo "Error: sqlite3 is not installed. Please install it before running this script."
    exit 1
fi

# Check if python3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 is not installed. Please install it before running this script."
    exit 1
fi

# Check if Flask is installed
if ! python3 -m flask --version &> /dev/null; then
    echo "Error: Flask is not installed. Please install it before running this script."
    exit 1
fi

# Check if the migration directory exists
if [ ! -d "migrations" ]; then
    echo "Initializing migration for the first time..."
    python3 -m flask db init
fi

# Check if sqlite.db does not exists and there is a sqlite-backup.db file
# . restore from backup before migration
if [ ! -e "instance/volumes/sqlite.db" ] && [ -e "instance/volumes/sqlite-backup.db" ]; then
    echo "No sqlite.db found, using sqlite-backup.db to generate the file."
    
    # Copy backup file to primary (sqlite.db)
    cp "instance/volumes/sqlite-backup.db" "instance/volumes/sqlite.db"

    # Extract the new Alembic version from the backup database
    backup_version=$(sqlite3 instance/volumes/sqlite.db "SELECT version_num FROM alembic_version;")
    echo "Version ${backup_version} detected"

    python3 -m flask db stamp "${backup_version}"

# Check if sqlite.db exists
# . backup before migration
elif [ -e "instance/volumes/sqlite.db" ]; then
    # Create a timestamp for the backup file
    timestamp=$(date "+%Y%m%d%H%M%S")
    backup_file="instance/volumes/sqlite-backup-${timestamp}.db"

    # Backup SQLite database
    sqlite3 instance/volumes/sqlite.db ".backup instance/volumes/sqlite-backup.db"
    sqlite3 instance/volumes/sqlite.db ".backup ${backup_file}"
fi


# Perform database migrations
python3 -m flask db migrate

# Perform database upgrade
python3 -m flask db upgrade

# Run a custom command to generate data
python3 -m flask custom generate_data
