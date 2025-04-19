# 📦 PRODIRECT Raffle Bot

> Advanced automation system for ProDirect online raffles. Designed for sneaker enthusiasts seeking an edge in limited releases.

## The Ultimate ProDirect Raffle Automation Tool

PRODIRECT Bot is a sophisticated raffle entry automation system specifically engineered for ProDirect's email-based raffles. Built with multi-threaded processing, address randomization, and email management capabilities, this bot delivers consistent entries across multiple limited sneaker drops. This bot is able to submit **thousands of entries per raffle**.

## ✨ Features

- **High-Volume Entry**: Submit thousands of entries to maximize winning chances
- **Address Randomization**: Built-in address jig functions for varied submissions
- **Email Management**: Support for high-volume email lists
- **Multi-threaded Architecture**: Submits hundreds of entries in minimal time
- **Proxy Support**: Compatible with residential and datacenter proxies
- **Robust Logging**: Detailed logs for successful and failed entries

## 🛠️ Technical Overview

PRODIRECT Bot works through a streamlined process:
1. Loads email list and proxies
2. Fetches the raffle form
3. Randomizes personal information and addresses
4. Submits entries for specified raffles
5. Tracks successful entries in detailed logs

## 📋 Requirements

- Python 3.6+
- Faker
- BeautifulSoup4
- Requests
- Proxy list (recommended for high-volume entries)
- Email list

## 🚀 Getting Started

1. Configure your `config.json` with:
   - Address templates
   - Thread count parameters

2. Prepare proxies in `proxies.txt` (one per line)
   
3. Add emails to `emails.txt`

4. Run the raffle entry bot:
```bash
python outlook.py
```

## ⚙️ Configuration

The `config.json` file controls key parameters:

```json
{
  "address": [
    {
      "address1": "## #pre#13 Ash%var=.,-,'%f%var=0,o%rd BC",
      "address2": "166 ## Feltham #suff#",
      "zip": "TW15 1YQ",
      "city": "Ashford", 
      "state": ""
    }
  ],
  "maxthread": 2,
  "amount": 3000
}
```

---

**Disclaimer**: This tool is provided for educational purposes only. Users are responsible for compliance with all applicable terms of service and laws in their jurisdiction.

*"When it comes to limited drops, automation is the difference maker" - PRODIRECT Bot* 