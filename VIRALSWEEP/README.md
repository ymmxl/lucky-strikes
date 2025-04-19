# 🌊 VIRALSWEEP Raffle Bot

> Advanced automation system for ViralSweep-powered raffles. Designed for sneaker enthusiasts seeking an edge in limited releases hosted on the ViralSweep platform.

## The Ultimate ViralSweep Raffle Automation Tool

VIRALSWEEP Bot is a sophisticated raffle entry automation system specifically engineered for online raffles using the ViralSweep platform. Built with multi-threaded processing, intelligent form submission, and randomized user data, this bot delivers consistent entries across multiple limited sneaker drops. The bot can submit **thousands of entries per raffle** with configurable timing controls.

## ✨ Features

- **High-Volume Entry**: Submit thousands of entries to maximize winning chances
- **User Agent Rotation**: Uses diverse browser fingerprints to avoid detection
- **Smart Email Generation**: Creates realistic email variations using multiple formats
- **Multi-threaded Architecture**: Distributes requests across multiple parallel processes
- **Proxy Support**: Compatible with residential and datacenter proxies
- **Interactive Controls**: Exit functionality to gracefully stop the entry process
- **Configurable Timing**: Adjustable sleep times between submissions to avoid rate limits
- **Robust Logging**: Detailed logs for successful and failed entries

## 🛠️ Technical Overview

VIRALSWEEP Bot works through a streamlined process:
1. Loads configuration, proxy settings, and user agents
2. Generates randomized user information and emails
3. Submits entries to the ViralSweep API endpoints
4. Uses staggered timing to avoid detection
5. Tracks successful entries in detailed logs

## 📋 Requirements

- Python 3.6+
- Requests
- BeautifulSoup4
- Faker
- InquirerPy
- Brotli (for response processing)
- User agent list

## 🚀 Getting Started

1. Configure your `config.json` with:
   - Address templates
   - Thread count and timing parameters

2. Prepare proxies in `proxies.txt` (one per line)

3. Ensure `user_agents.txt` contains a variety of browser user agents

4. Run the raffle entry bot:
```bash
python app.py
```

## 📊 Workflow

1. Bot loads configuration, proxy data, and user agents
2. Creates a queue of entry tasks based on configured amount
3. Launches multiple threads to process the queue
4. Each thread:
   - Generates a random user profile and email
   - Selects random shoe size
   - Submits entry to ViralSweep API
   - Logs results and sleeps according to configuration
5. Results logged to `Entered.txt` and `Failed.txt`

## ⚙️ Configuration

The `config.json` file controls key parameters:

```json
{
  "address": [
    {
      "address1": "## #pre#13 Ash%var=.,-,'%f%var=0,o%rd BC",
      "address2": "166 ## Feltham #suff#",
      "zip": "",
      "city": "",
      "state": ""
    }
  ],
  "maxthread": 2,
  "amount": 30000,
  "time_sleep": 30,
  "stagger": 30
}
```
Address Jigs are available through `utils` in `tools`
---

**Disclaimer**: This tool is provided for educational purposes only. Users are responsible for compliance with all applicable terms of service and laws in their jurisdiction.

*"When everyone enters once, enter thousands of times" - VIRALSWEEP Bot* 