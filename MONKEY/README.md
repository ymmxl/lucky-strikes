# 🐒 MONKEY Raffle Bot
[ARCHIVE]
> Note: This is a bot that submits automated entries for the sneaker store CCS that uses SurveyMonkey as a means of online raffle. This store has now switched to Google Form sign in. RIP to an era.


## The Ultimate SurveyMonkey Raffle Automation Tool

MONKEY is an advanced raffle entry automation system specifically designed to handle SurveyMonkey-based raffles for hyped sneaker releases. Built with speed, reliability, and intelligent form parsing at its core, this bot has delivered consistent wins across multiple drops.
>  A little flex that proves submitted entries were genuine


![MONKEY Bot Success](https://i.imgur.com/7cToH9Y.jpeg)

## 🔥 Real Results

This bot has been particularly effective for CCS raffles, which use SurveyMonkey's 5-minute form entries as their raffle system for limited sneaker releases. With thread-based multiprocessing, MONKEY can submit **1500+ entries per raffle**, dramatically increasing your chances of securing wins.


## ✨ Features

- **Intelligent Form Parsing**: Automatically detects and parses SurveyMonkey form questions and fields
- **Interactive Question Answering**: Beautiful selector interface using InquirerPy for easy answer selection
- **High-Speed Entry**: Multi-threaded architecture enables 1500+ entries in minimal time
- **Address Randomization**: Built-in address jig functions to vary submissions while maintaining deliverability
- **Email Management**: Supports both catchall domains and email lists
- **Proxy Support**: Compatible with residential and datacenter proxies
- **Offline Mode**: Test form submission answers without making actual requests
- **Robust Logging**: Detailed logs for successful and failed entries

## 🛠️ Technical Overview

MONKEY works by intelligently scraping SurveyMonkey forms, analyzing question types, and constructing proper submission data. The bot handles:

- Single/multiple choice questions
- Dropdown selectors
- Contact information fields
- Size selection with intelligent filtering
- Question matrices and other complex field types

## 📋 Requirements

- Python 3.6+
- InquirerPy
- BeautifulSoup4
- Proxies list (recommended for high-volume entries)
- Email list or catchall domain

## 🚀 Getting Started

1. Clone or download the repo
2. Install dependencies:
```bash
pip install inquirerpy bs4 colorama faker capmonster_python
```
3. Configure your `config.json` with:
   - Proxy settings
   - Address templates
   - Catchall domains (optional)
   - Thread count and retry parameters

4. Prepare email list in `emails.txt` (or use catchall option)

5. Run the bot:
```bash
python app.py
```

## 📊 Workflow

1. Bot loads configuration and email/proxy data
2. User provides SurveyMonkey raffle URL
3. Bot scrapes and analyzes the form structure
4. User selects answers through interactive prompts
5. Bot builds and submits entries across multiple threads
6. Results logged to `entered.txt` and log files

## 🧪 Testing Mode

For testing your form answers without making submissions, use the offline app:

```bash
python offline_app.py
```

This allows you to verify your answers are correctly formatted before launching a full entry campaign.

[offline_app_test](https://i.imgur.com/lPm7XOb.gif)
## ⚙️ Configuration

The `config.json` file controls key parameters:

```json
{
  "max_threads": 200,
  "retry_delay": 3,
  "max_retry": 5,
  "catchall": ["domain1.com", "domain2.com"],
  "address": [
    {
      "fname": "RANDOM",
      "lname": "RANDOM",
      "address1": "## %var=street% dr #suff#",
      "address2": "#pre#17A",
      "zip": "12345",
      "city": "City",
      "state": "ST"
    }
  ]
}
```

---

**Disclaimer**: This tool is provided for educational purposes only. Users are responsible for compliance with all applicable terms of service and laws in their jurisdiction.

*"Automate the boring stuff, win the hype stuff" - MONKEY Bot* 