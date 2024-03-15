# CyberNewsBot
A Discord bot which posts news articles from a specific RSS feed to a Discord channel. 
The script pulls the bot token from AWS SSM Parameter Store. If you are hosting your bot/tokens elsewhere, you don't need boto3.

## Dependencies

Run the following commands to install dependencies:

```
pip install discord
pip install boto3
pip install requests
```
