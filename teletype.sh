#!/bin/bash

# Get the current date and time
COMMIT_MESSAGE="Scripted commit ($(date '+%Y-%m-%d %H:%M:%S'))"

# Function to handle errors
handle_error() {
    echo "Error: $1"
    echo "Git error message: $2"
    exit 1
}

# Pull changes from the remote repository
if ! git pull >> /dev/null 2>&1; then
    handle_error "Error when pulling" "$(git pull 2>&1)"
else
    echo "Finished pulling."
fi

# Add all files recursively
if ! git add . >> /dev/null 2>&1; then
    handle_error "Error when adding files" "$(git add . 2>&1)"
else
    echo "Finished adding."
fi

# Commit with the specified message
if ! git commit -m "$COMMIT_MESSAGE" >> /dev/null 2>&1; then
    handle_error "Error when registering a commit" "$(git commit -m "$COMMIT_MESSAGE" 2>&1)"
else
    echo "Finished committing."
fi

# Push the commit to the remote repository
if ! git push >> /dev/null 2>&1; then
    handle_error "Error when pushing" "$(git push 2>&1)"
else
    echo "Finished pushing."
fi

echo "Finished."
