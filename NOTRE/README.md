# 🏛️ NOTRE Raffle Bot

> Advanced automation system for Notre's online raffles. Designed for sneaker enthusiasts seeking to secure limited releases through Notre's platform.

## The Ultimate Notre Raffle Automation Tool

NOTRE Bot is a sophisticated raffle entry automation system specifically engineered for Notre online raffles. Built with captcha solving, question answering, and address randomization capabilities, this bot delivers consistent entries for exclusive sneaker releases. The bot integrates with Notre's question-based verification system to ensure legitimate-looking entries.

## ✨ Features

- **Automated Registration**: Submit registrations to Notre's raffle platform  
- **Question Answering System**: Automatically answers verification questions correctly
- **Captcha Solving**: Integration with captcha solving services
- **Address Randomization**: Built-in address jig functions for varied submissions
- **Multi-parameter Input**: Customizable name, address, and contact information
- **Proxy Support**: Compatible with residential and datacenter proxies
- **API Integration**: Works with Notre's API endpoints directly

## 🛠️ Technical Overview

NOTRE Bot works through a multi-stage process:
1. Loads configuration and proxy settings
2. Fetches raffle details and verification questions
3. Automatically answers verification questions using pre-defined answer sets
4. Solves captcha challenges using external service
5. Submits registration with randomized information
6. Tracks submissions in detailed logs

## 📋 Requirements

- Python 3.6+
- Requests
- BeautifulSoup4
- Faker
- InquirerPy
- Captcha solving API key
- Proxy list (recommended)

## 🚀 Getting Started

1. Configure your `config.json` with:
   - Address templates
   - Personal information formatting

2. Prepare proxies in `proxies.txt` (one per line)

3. Add emails to `emails.txt`

4. Update answers in `answers.json` based on Notre's question database

5. Run the raffle entry bot:
```bash
python app.py
```

## ⚙️ Configuration

The `config.json` file controls key parameters:

```json
{
  "address": [
    {
      "fname": "RANDOM",
      "lname": "RANDOM",
      "address1": "## clinton dr #suff#",
      "address2": "#pre#17A",
      "zip": "03049",
      "city": "Hollis",
      "state": "NH"
    }
  ]
}
```

The `answers.json` file stores question/answer mappings for Notre's verification system:

```json
[
  {
    "id": 1,
    "answer": 0
  },
  {
    "id": 2,
    "answer": 1
  }
]
```

---

**Disclaimer**: This tool is provided for educational purposes only. Users are responsible for compliance with all applicable terms of service and laws in their jurisdiction.

*"Smart answers, strategic entries, secured sneakers" - NOTRE Bot* 