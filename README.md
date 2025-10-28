# KL Slack Bot

A Slack bot built with [Bolt for Python][1] that responds to messages and handles file uploads.

## Running with Docker Compose

This project is designed to run with Docker Compose and [Watchtower][2] for automatic updates.

### 1. Create Environment File

Create a `.env` file in the project root:

```bash
cat > .env << EOF
SLACK_BOT_TOKEN=xoxb-your-bot-token-here
SLACK_APP_TOKEN=xapp-your-app-token-here
SLACK_SERVICE_TOKEN=xoxs-your-service-token-here
EOF
```

**Where to get your tokens:**
- **SLACK_BOT_TOKEN**: Required. Slack App settings → OAuth & Permissions → Bot User OAuth Token
- **SLACK_APP_TOKEN**: Required. Slack App settings → Basic Information → App-Level Tokens → Socket Mode  
- **SLACK_SERVICE_TOKEN**: Only needed for deployments. Run `slack auth token` locally to get one

### 2. Build and Run

```bash
docker-compose up -d
```

The bot will start and automatically connect to Slack via Socket Mode.

### Deploying with Service Token

To deploy your app to Slack using the service token:

```bash
slack deploy --token $SLACK_SERVICE_TOKEN
```

This will use the service token to deploy your app's manifest and settings to Slack. See [Slack CLI docs](https://docs.slack.dev/tools/slack-cli/guides/authorizing-the-slack-cli#ci-cd-authorization) for more details.

### 3. Watchtower Setup

To enable automatic updates with Watchtower, add this service to your `docker-compose.yml`:

```yaml
services:
  watchtower:
    image: containrrr/watchtower
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    environment:
      - WATCHTOWER_CLEANUP=true
      - WATCHTOWER_POLL_INTERVAL=86400
    labels:
      - "com.centurylinklabs.watchtower.enable=true"
```

## Running Locally (Development)

### Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Run

```bash
# Set environment variables
export SLACK_BOT_TOKEN=xoxb-your-token
export SLACK_APP_TOKEN=xapp-your-token

# Start the app
python3 app.py
```

## Documentation

- [Bolt for Python][1]
- [Getting Started with Bolt][3]
- [More Bolt Examples][5]
- [Docker CI/CD Setup](DOCKER_CI_SETUP.md)
- [Watchtower][2]

[1]: https://slack.dev/bolt-python/
[2]: https://containrrr.dev/watchtower/
[3]: https://slack.dev/bolt-python/tutorial/getting-started#setting-up-events
[5]: https://github.com/slackapi/bolt-python/tree/main/examples