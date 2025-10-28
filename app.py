import os
import requests
from datetime import datetime
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# This sample slack application uses SocketMode
# For the companion getting started setup guide, 
# see: https://slack.dev/bolt-python/tutorial/getting-started 

# Initializes your app with your bot token
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))


# Listens to incoming messages that contain "hello"
@app.message("hello")
def message_hello(message, say):
    # say() sends a message to the channel where the event was triggered
    say(
        blocks=[
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"Hey there <@{message['user']}>!"},
                "accessory": {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "Click Me"},
                    "action_id": "button_click",
                },
            }
        ],
        text=f"Hey there <@{message['user']}>!",
    )


@app.action("button_click")
def action_button_click(body, ack, say):
    # Acknowledge the action
    ack()
    say(f"<@{body['user']['id']}> clicked the button")


@app.event({"type": "message", "subtype": "file_share"})
def handle_file_shared(event, say, client, logger):
    # Debug: log the event structure
    logger.info(f"Event received: {event}")
    
    # Get the file from the message
    # The file might be in event['files'] or event['file']
    if "files" in event and len(event["files"]) > 0:
        file_info = event["files"][0]
    elif "file" in event:
        file_info = event["file"]
    else:
        logger.error("No file found in event")
        say("❌ No file found in the message.")
        return
    
    file_id = file_info["id"]
    logger.info(f"Processing file with ID: {file_id}")
    
    # Get detailed file information
    detailed_file_info = client.files_info(file=file_id)
    file_data = detailed_file_info["file"]
    
    # Check if it's a PDF
    if file_data.get("mimetype") != "application/pdf":
        say("Please upload only PDF files.")
        return
    
    # Download the file
    file_url = file_data["url_private_download"]
    filename = file_data["name"]
    
    # Create uploads directory if it doesn't exist
    os.makedirs("uploads", exist_ok=True)
    
    # Generate timestamped filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    local_filename = f"uploads/{timestamp}_{filename}"
    
    # Download file with authentication
    headers = {"Authorization": f"Bearer {os.environ.get('SLACK_BOT_TOKEN')}"}
    response = requests.get(file_url, headers=headers)
    
    if response.status_code == 200:
        # Save to disk
        with open(local_filename, "wb") as f:
            f.write(response.content)
        
        say(f"✅ PDF saved successfully as `{local_filename}`")
    else:
        say("❌ Failed to download the file.")


# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
