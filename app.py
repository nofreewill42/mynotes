from flask import Flask, request, jsonify, send_from_directory
import json
from pathlib import Path
import git
import os

app = Flask(__name__, static_url_path='')

DATA_FILE = Path('notes_data.json')

# Ensure the file exists
if not DATA_FILE.exists():
    with open(DATA_FILE, 'w') as f:
        json.dump({"notes": [], "connections": []}, f)

@app.route('/')
def index():
    return send_from_directory('', 'index.html')

@app.route('/data', methods=['GET', 'POST'])
def manage_data():
    if request.method == 'POST':
        data = request.json.get('data')
        commit_message = request.json.get('commit_message', 'Updated notes and connections')
        
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=4)

        # Commit the changes to git
        repo = git.Repo(os.getcwd())
        repo.git.add(DATA_FILE)
        repo.index.commit(commit_message)

        return jsonify({'status': 'success'}), 201

    return send_from_directory('', 'notes_data.json')

if __name__ == '__main__':
    app.run(debug=True)
