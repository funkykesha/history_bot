# Deployment Guide

This document provides instructions for deploying the Telegram Chat History Export Bot.

## Prerequisites

- Python 3.11 or higher
- Git
- Railway CLI
- Telegram Bot Token
- GitHub account
- Railway account

## Local Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/telegram-chat-export-bot.git
   cd telegram-chat-export-bot
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create `.env` file:
   ```
   BOT_TOKEN=your_telegram_bot_token
   EXPORT_DIR=exports
   MAX_EXPORT_AGE_DAYS=7
   ```

5. Run tests:
   ```bash
   pytest
   ```

## Railway Deployment

### Manual Deployment

1. Install Railway CLI:
   ```bash
   curl -fsSL https://railway.app/install.sh | sh
   ```

2. Login to Railway:
   ```bash
   railway login
   ```

3. Link your project:
   ```bash
   railway link
   ```

4. Set environment variables:
   ```bash
   railway variables set BOT_TOKEN=your_telegram_bot_token
   railway variables set EXPORT_DIR=exports
   railway variables set MAX_EXPORT_AGE_DAYS=7
   ```

5. Deploy:
   ```bash
   railway up
   ```

### Automated Deployment (GitHub Actions)

1. Fork the repository to your GitHub account

2. Add secrets to your GitHub repository:
   - `RAILWAY_TOKEN`: Your Railway API token
   - `CODECOV_TOKEN`: Your Codecov token (optional)

3. Push to main branch to trigger deployment:
   ```bash
   git push origin main
   ```

## Monitoring

1. Check deployment status:
   ```bash
   railway status
   ```

2. View logs:
   ```bash
   railway logs
   ```

3. Monitor metrics in Railway dashboard

## Troubleshooting

### Common Issues

1. **Bot not responding**
   - Check if bot token is correct
   - Verify environment variables are set
   - Check Railway logs for errors

2. **Export fails**
   - Verify user has permission to access chat history
   - Check if export directory exists and is writable
   - Review error logs

3. **Deployment fails**
   - Check GitHub Actions logs
   - Verify Railway token is valid
   - Ensure all required environment variables are set

### Getting Help

1. Check the [GitHub Issues](https://github.com/yourusername/telegram-chat-export-bot/issues)
2. Review [Telegram Bot API documentation](https://core.telegram.org/bots/api)
3. Contact Railway support for deployment issues

## Security Considerations

1. Never commit `.env` file or sensitive tokens
2. Use environment variables for all sensitive data
3. Regularly rotate bot tokens
4. Monitor bot usage and set rate limits
5. Keep dependencies updated

## Maintenance

1. Regular updates:
   ```bash
   pip install --upgrade -r requirements.txt
   ```

2. Database maintenance:
   - Monitor export directory size
   - Clean up old exports regularly

3. Backup:
   - Export directory should be backed up regularly
   - Keep configuration backups

## Rollback

1. Revert to previous version:
   ```bash
   railway rollback
   ```

2. Or deploy specific commit:
   ```bash
   railway up --commit <commit-hash>
   ``` 