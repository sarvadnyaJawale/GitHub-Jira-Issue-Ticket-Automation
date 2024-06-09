from flask import Flask, jsonify, request
import requests
from requests.auth import HTTPBasicAuth
import json

app = Flask(__name__)

@app.route('/create', methods=['POST'])
def create_jira():
    # Get JSON payload from GitHub webhook
    data = request.get_json()
    
    # Check if the payload contains an issue comment
    if 'comment' not in data or 'body' not in data['comment']:
        return jsonify({"message": "No comment found in payload"}), 400
    
    comment = data['comment']['body']
    
    # Check if the comment contains "/jira"
    if "/jira" not in comment:
        return jsonify({"message": "Comment does not contain '/jira', issue not created"}), 200
    
    # Jira API details
    url = "https://sarvadnyajawle.atlassian.net/rest/api/3/issue"
    auth = HTTPBasicAuth("your mail Id", "YOUR_API_TOKEN_HERE")
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    # Payload for Jira API
    payload = json.dumps({
        "fields": {
            "summary": "This is first ticket created by python",
            "issuetype": {
                "id": "10009"
            },
            "project": {
                "key": "SGJA"
            },
            "description": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "type": "text",
                                "text": "Order entry fails when selecting supplier."
                            }
                        ]
                    }
                ]
            }
        }
    })

    # Send request to Jira API
    response = requests.post(
        url,
        headers=headers,
        auth=auth,
        data=payload
    )

    # Handle response from Jira API
    if response.status_code == 201:
        return jsonify({"message": "Issue created successfully", "issue_key": response.json().get("key")}), 201
    else:
        return jsonify({"message": "Failed to create issue", "details": response.json()}), response.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000)
