# Docker CI/CD Setup with Slack CLI

This Dockerfile includes the Slack CLI for deployment and management of your Slack app.

## Service Token Setup for CI/CD

Since this Docker container is designed for CI/CD, you'll need to use a **service token** instead of interactive authentication.

### Step 1: Obtain a Service Token

Run the following command **locally** to get a service token:

```bash
slack auth token
```

This will display:
1. An authorization ticket slash command (e.g., `/slackauthticket ABC123...`)
2. A prompt for a challenge code

1. Copy the slash command and paste it into any Slack channel in your workspace
2. A modal will appear - click **Confirm**
3. A new modal will appear with a challenge code
4. Copy the challenge code and paste it back into your terminal

The service token will be displayed in your terminal. **Save this securely** - it will not be saved to your local credentials file.

### Step 2: Use Service Token in CI/CD

Set the service token as an environment variable when building/running the Docker container:

#### Option A: Environment Variable
```bash
docker build -t kl .
docker run -e SLACK_SERVICE_TOKEN=<your-service-token> kl
```

#### Option B: CI/CD Pipeline (GitHub Actions example)
```yaml
- name: Run Docker container
  run: |
    docker run -e SLACK_SERVICE_TOKEN=${{ secrets.SLACK_SERVICE_TOKEN }} \
               -e SLACK_BOT_TOKEN=${{ secrets.SLACK_BOT_TOKEN }} \
               -e SLACK_APP_TOKEN=${{ secrets.SLACK_APP_TOKEN }} \
               kl
```

### Step 3: Using the Slack CLI in Container

Once the container is running with the service token, you can execute Slack CLI commands:

```bash
# Authenticate with the service token
docker exec -it <container-id> slack --token <your-service-token> auth list

# Deploy your app
docker exec -it <container-id> slack --token <your-service-token> deploy
```

### Best Practices

1. **Use a Service Account**: Create a dedicated Slack user account for CI/CD operations
2. **Store Securely**: Never commit service tokens to version control
3. **Rotate Regularly**: If a token is compromised, revoke it with:
   ```bash
   slack auth revoke --token <your-service-token>
   ```

## GitHub Actions CI/CD

This repository includes a GitHub Actions workflow that automatically builds and pushes the Docker image to GitHub Container Registry (GHCR) when code is merged to the `main` branch.

### How It Works

The workflow (`.github/workflows/docker-push.yml`) uses the [docker-build-push-action](https://github.com/marketplace/actions/docker-build-push-action) to:
- Build the Docker image on every push to `main`
- Tag it with the build number and `latest`
- Push to `ghcr.io/${{ github.repository_owner }}/kl`

### Setting Up GitHub Actions

1. **Enable Packages**: Navigate to your repository → Settings → Actions → General
2. **Enable read and write permissions**: For "Workflow permissions", select "Read and write permissions"
3. **Save the settings**

### Using the Docker Image from GHCR

After a successful build, you can pull and run the image:

```bash
# Login to GHCR (first time only)
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin

# Pull the image
docker pull ghcr.io/YOUR-USERNAME/kl:latest

# Run the container
docker run -e SLACK_BOT_TOKEN=<token> -e SLACK_APP_TOKEN=<token> ghcr.io/YOUR-USERNAME/kl:latest
```

## Building and Testing Locally

### Build the Image
```bash
docker build -t kl .
```

### Test with Colima

1. Start Colima (if not already running):
   ```bash
   colima start
   ```

2. Build the Docker image:
   ```bash
   docker build -t kl .
   ```

3. Run the container:
   ```bash
   docker run --rm kl
   ```

## Environment Variables Required

Your Slack app requires these environment variables:

- `SLACK_BOT_TOKEN` - Bot User OAuth Token
- `SLACK_APP_TOKEN` - App-Level Token (for Socket Mode)
- `SLACK_SERVICE_TOKEN` - Service token for CI/CD operations (optional, for CLI use)

Set these when running the container:
```bash
docker run -e SLACK_BOT_TOKEN=<token> -e SLACK_APP_TOKEN=<token> kl
```

