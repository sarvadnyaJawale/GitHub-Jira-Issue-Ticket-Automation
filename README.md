# GitHub-Jira-Issue-Ticket-Automation

![Blank diagram (1)](https://github.com/sarvadnyaJawale/GitHub-Jira-Issue-Ticket-Automation/assets/127713222/22e976d7-6002-4056-a68e-4fe6f3505bae)


**Introduction:**
Have you ever encountered a critical issue in your development project, only to realize the cumbersome task of manually creating a Jira ticket for it? This back-and-forth between GitHub and Jira disrupts workflow and slows down resolution times. But what if there was a way to automate the process?

This project introduces an innovative solution built with Python to bridge the gap between GitHub and Jira. By leveraging the power of webhooks and APIs, we'll create a streamlined workflow that automatically generates Jira tickets from designated comments within your GitHub issues. Imagine this:

A developer encounters a crucial bug in your application's code.

They add a simple comment like "/jira" to the corresponding GitHub issue.

Behind the scenes, our Python application springs into action.

It intercepts the notification from the GitHub webhook, capturing details about the issue.

Using the Jira API, the application connects to your Jira project and creates a corresponding ticket.

This seamless integration ensures that all team members are instantly informed about critical issues, facilitating faster collaboration and resolution. No more manual ticket creation! By automating this task, we free up valuable time for developers to focus on what they do best – writing exceptional code.

Throughout this blog series, we'll delve into the technical aspects of this project. We'll explore:

Setting up a Jira account and generating an API token.

Understanding the Jira Python library for programmatic interaction.

Building the Python script with Flask for webhook handling and API calls.

Deploying the application on an AWS EC2 instance for continuous operation.

By the end, you'll be equipped with the knowledge and resources to create your own automated Jira ticket creation system, enhancing your development team's efficiency and communication. Buckle up and get ready to streamline your workflow!

Step 1: Setting Up Your Jira Account and Project

The foundation of our automated workflow lies within your Jira account. In this step, we'll guide you through creating a project specifically designed to handle tickets generated from GitHub issues. Here's how:

1.1 Sign Up for a Free Atlassian Account (if you haven't already):

Head over to Atlassian and create a free account if you don't have one. This account will grant you access to Jira, where we'll manage our project-specific details.

1.2 Create a Scrum Project:

Once you're logged in, navigate to the project creation section. Jira offers various project templates. For this automation, we recommend selecting the "Scrum" project type. This aligns well with Agile development methodologies, which emphasize iterative development and rapid response to issues.

Team-managed project: Choose this option when creating the scrum project. This ensures you have full control over the project's settings and configuration.

1.3 Configure Your Project Details:

Provide a descriptive name for your project that reflects its purpose, such as "GitHub-Generated Jira Tickets." This will help team members easily identify its function. Additionally, assign a unique project key, which is a short identifier used with project-specific tasks and issues.

1.4 Familiarize Yourself with Your Jira Dashboard:

After creating the project, you'll be redirected to your Jira dashboard. This dashboard serves as the central hub for managing your project, including viewing existing tickets, creating new ones, and monitoring progress.

Optional (But Highly Recommended): Explore the different boards and workflows offered within the "Scrum" project type. You can customize these aspects later based on your team's specific needs.

This concludes Step 1! We've successfully laid the groundwork for our automated workflow by setting up a dedicated Jira project. In the next step, we'll delve into generating an API token – a crucial key that unlocks programmatic interaction between our Python script and your Jira project.

Step 2: Generating an API Token for Programmatic Access

Now that we have our Jira project in place, it's time to establish a secure connection between our Python script and Jira. This connection will allow the script to interact with Jira programmatically, enabling the creation of tickets directly from GitHub issue comments. To achieve this, we'll need to generate an API token.

2.1 Accessing Your Profile Settings:

Navigate to your profile picture in the top-right corner of your Jira dashboard. Click on it to reveal a dropdown menu.

2.2 Managing Your Profile and Applications:

From the dropdown menu, select "Manage my profile and applications." This will lead you to a page containing your account settings and various applications linked to Jira.

2.3 Creating an API Token:

Locate the "Security" section on the settings page. Within this section, find the option for "API tokens." Click on "Create API token" to initiate the token creation process.

2.4 Securely Storing Your API Token:

Jira will display a newly generated API token. This token is critical for our Python script to communicate with Jira. It's crucial to note that this token will only be displayed once, so make sure to copy it securely! Consider using a password manager or a secure text file for storing this sensitive information.

Understanding API Tokens:

Think of an API token as a digital key that grants specific access to your Jira account. In this case, the token we've created authorizes our Python script to create new issues within the designated project.

Important Security Reminder:

Never share your API token publicly or with unauthorized individuals. Treat it with the same level of care you would any other sensitive login credential.

By completing this step, we've established a secure communication channel between our Python script and Jira, paving the way for automated ticket creation in the coming steps. In the next section, we'll delve into understanding the Jira Python library, which will serve as the backbone of our script's interaction with Jira's API.

Step 3: Interacting with the Jira API Using Python

To automate the creation of Jira tickets, we will use the Jira API. We'll reference the Jira API documentation to understand how to interact with it using Python. Follow these steps to get started:

Step-by-Step Guide to Interacting with Jira API

Access Jira API Documentation:

Go to the Jira API documentation.

On the left sidebar, search for "Project" and select "Create project".

Select Python Documentation:

In the "Create project" section, you will see examples in various languages. Select the Python documentation to see how to make API calls using Python.

Set Up Python Environment:

Ensure you have Python installed on your system. If not, download and install it from the official Python website.

Install the necessary Python packages. You will need the requests library to make HTTP requests. Install it using pip:

pip install requests

Create a Python Script:

Create a new Python script file (e.g., create_jira_ticket.py).

Update Your Credentials:

In the Python script, update your email ID, Atlassian site, and the API token you copied in the last step. Below is an example script to create a Jira ticket:

Here is Code Sample:

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

Introduction to Flask Framework

Flask is a micro web framework for Python that allows developers to build web applications easily and quickly. It provides the essential tools and functionalities needed to create web applications or APIs, such as routing, request handling, and response rendering. Flask is lightweight, flexible, and designed to be modular, allowing developers to add extensions as needed.

Python Flask Script Overview

This script sets up a Flask web application that listens for POST requests at the /create endpoint. When a comment is made on a GitHub issue containing the string /jira, the script creates a corresponding issue in Jira using the Jira API.

Imports:

pythonCopy codefrom flask import Flask, jsonify, request
import requests
from requests.auth import HTTPBasicAuth
import json

Flask: The main class for creating a Flask web application.

jsonify: A function to convert Python dictionaries to JSON responses.

request: An object to handle HTTP requests.

requests: A library for making HTTP requests.

HTTPBasicAuth: A class for handling basic HTTP authentication.

json: A library for working with JSON data.

Initialize Flask Application:

pythonCopy codeapp = Flask(__name__)

Creates an instance of the Flask class, initializing the web application.

Define the Route and Function to Handle Requests:

pythonCopy code@app.route('/create', methods=['POST'])
def create_jira():

@app.route('/create', methods=['POST']): A decorator that binds the URL path /create to the create_jira function. It specifies that this route only accepts POST requests.

def create_jira(): The function that will be called when a POST request is made to /create.

Get JSON Payload from GitHub Webhook:

data = request.get_json()

data = request.get_json(): Extracts the JSON payload from the incoming request.

Check for Issue Comment in Payload:

if 'comment' not in data or 'body' not in data['comment']:
 return jsonify({"message": "No comment found in payload"}), 400

Validates that the payload contains a comment. If not, it returns a 400 Bad Request response.

Extract Comment Text:

comment = data['comment']['body']

Extracts the body of the comment from the payload.

Check for/jira in Comment:

if "/jira" not in comment:
return jsonify({"message": "Comment does not contain '/jira', issue not created"}), 200

Checks if the comment contains /jira. If not, it returns a 200 OK response with a message indicating no issue was created.

Jira API Details:

url = "https://sarvadnyajawle.atlassian.net/rest/api/3/issue"
auth = HTTPBasicAuth("sarvadnyajawle@gmail.com", "YOUR_API_TOKEN_HERE")
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

url: The Jira API endpoint for creating issues.

auth: HTTP Basic Authentication using the user's email and API token.

headers: HTTP headers indicating the content type and acceptance of JSON.

Payload for Jira API:

load = json.dumps({
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

payload: A JSON string containing the details of the Jira issue to be created, including the project key, issue type, summary, and description.

Send Request to Jira API:

response = requests.post(
    url,
    headers=headers,
    auth=auth,
    data=payload
)

requests.post: Makes a POST request to the Jira API endpoint with the specified headers, authentication, and payload.

Handle Response from Jira API:

if response.status_code == 201:
    return jsonify({"message": "Issue created successfully", "issue_key": response.json().get("key")}), 201
else:
    return jsonify({"message": "Failed to create issue", "details": response.json()}), response.status_code

Checks if the response status code is 201 (Created). If successful, it returns a JSON response with the issue key.

If the request fails, it returns a JSON response with the error details and the appropriate status code.

Run the Flask Application:

pythonCopy codeif __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000)

Runs the Flask application on host 0.0.0.0 (accessible from any IP address) and port 6000.

**Brief Introduction to APIs**

An API (Application Programming Interface) is a set of rules that allows different software entities to communicate with each other. APIs define the methods and data structures for interaction between different systems, making it easier to integrate various software components.

**Types of APIs:**

**1. REST (Representational State Transfer):**

Uses HTTP requests to perform CRUD (Create, Read, Update, Delete) operations.

Stateless and follows a resource-based approach.

Commonly used for web services.

**2. SOAP (Simple Object Access Protocol):**

Uses XML for message format and typically relies on HTTP or SMTP for message negotiation and transmission.

More rigid and standardized compared to REST.

Often used in enterprise environments.

**3. GraphQL:**

Developed by Facebook, it allows clients to request exactly the data they need.

Uses a single endpoint and provides more flexibility than REST.

Suitable for complex queries and large-scale applications.

**Workflow of the Application:**

1. A developer writes a comment /jira on a GitHub issue.

2. The GitHub webhook sends a JSON payload to the Flask application's /create endpoint.

3. The Flask application parses the JSON payload and checks for the /jira keyword.

4. If /jira is found, the application constructs a payload for the Jira API.

5. The application sends a POST request to the Jira API to create an issue.

6. The Jira API responds with the status of the issue creation.

7. The Flask application returns an appropriate JSON response based on the success or failure of the issue creation.

8. This comprehensive setup automates the process of creating Jira tickets from GitHub comments, streamlining project management and issue tracking for development teams.

**Acknowledgement:**

Special thanks to Abhishek Veeramalla for the incredible project idea and guidance. Your insights and expertise have been invaluable in bringing this project to life. Thank you for inspiring and helping developers streamline their workflows with this seamless GitHub-Jira integration.


