# 👘 SACAI Raffle Bot

[ARCHIVED]
> Advanced automation system for SACAI online raffles and account creation. Designed for sneaker enthusiasts seeking an edge in limited releases.[^1]

[^1]:The bot has now been obselete since the relaunch of the new website. Tweaks or even rewrite are needed and i know you are well capable in doing so. I hope the flow and my approach to creating accounts and entering raffles have been inspirational.

## The Ultimate SACAI Raffle Automation Tool

SACAI Bot is a sophisticated raffle entry automation system specifically engineered for SACAI's online raffles. Built with multi-threaded processing, captcha solving, and email verification capabilities, this bot delivers consistent entries across multiple limited sneaker drops. This bot is able to submit **thousands of entries per raffle**.

![SACAI Bot Entry Success](https://i.imgur.com/3M8rzgv.png)

## :fire: Results
![SACAI Bot Success](https://i.imgur.com/lvt88n4.jpeg)
![SACAI Order](https://i.imgur.com/FTdS6f6.jpeg)

## ✨ Features

- **Automated Account Creation**: Creates verified SACAI accounts at scale
- **Email Verification System**: Automatically retrieves verification links from inbox
- **Multi-threaded Architecture**: Submits hundreds of entries in minimal time
- **Address Randomization**: Built-in address jig functions for varied submissions
- **Captcha Solving**: Integration with CapMonster for automated captcha solving
- **Proxy Support**: Compatible with residential and datacenter proxies
- **Verification Link Extraction**: Automatically scans email for verification links
- **Robust Logging**: Detailed logs for successful and failed entries

## 🛠️ Technical Overview

SACAI Bot works through a multi-stage process:
1. Creates accounts on the SACAI store
2. Monitors email inbox for verification links
3. Completes verification process automatically
4. Submits raffle entries for specified models and sizes
5. Tracks successful entries in detailed logs

## 📋 Requirements

- Python 3.6+
- imap_tools
- BeautifulSoup4
- Requests
- CapMonster API key
- Proxies list (recommended for high-volume entries)
- Email accounts or catchall domain

## 🚀 Getting Started

1. Configure your `config.json` with:
   - CapMonster API key
   - Email settings (IMAP server, credentials)
   - Proxy settings
   - Address templates
   - Raffle URL

2. Prepare proxies in `proxies.txt` (one per line)

3. Run the account creator:
```bash
python v.py
```

4. Run the raffle entry bot:
```bash
python app.py
```

![interface](https://i.imgur.com/zhatnHI.jpeg)
## 📊 Workflow

1. Bot loads configuration and proxy data
2. Creates SACAI accounts in bulk with randomized information
3. Monitors inbox for verification emails
4. Automatically completes verification process
5. Submits raffle entries for target products
6. Results logged to success and failed files

## ⚙️ Configuration

The `config.json` file controls key parameters:

```json
{
  "domain": ["yourdomain.com"],
  "maxthread": 2,
  "amount": 200,
  "task_delay": 60,
  "retry_delay": 20,
  "capmon": "YOUR_CAPMONSTER_KEY",
  "raffle_url": "https://store.sacai.jp/item/detail/...",
  "size_range": [6, 6.5, 7, 7.5, 8, 8.5, 10.5, 11, 11.5, 12],
  "color": "random",
  "verifier": {
    "imap": "imap.gmail.com",
    "email_folder": "[Gmail]/All Mail",
    "login": {
      "user": "your_email@gmail.com",
      "pw": "your_password"
    }
  }
}
```

---

**Disclaimer**: This tool is provided for educational purposes only. Users are responsible for compliance with all applicable terms of service and laws in their jurisdiction.

*"Win the raffles, secure the grails" - SACAI Bot* 

