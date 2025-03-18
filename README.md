# v2ray-tel-bot

This repository contains a Telegram bot built using the Pyrogram library that get account information using Subscription Link, QRCode, UUID, Vless, Vmess, Shadowsocks, and remark.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/nyeinkokoaung404/v2ray-tel-bot.git
    cd v2ray-tel-bot
    ```

2. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Configuration

Create a `config.py` file in the project directory and add the following configuration variables:

```python
# config.py

API_ID = 'your_api_id'
API_HASH = 'your_api_hash'
BOT_TOKEN = 'your_bot_token'
```

Replace the placeholder values with your actual API keys and tokens.

## Usage

To run the Bot, use the following command:
```sh
python main.py
```
