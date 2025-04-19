# 🏆 Sneaker Raffle Automation Suite

> A comprehensive collection of specialized raffle entry systems designed for various sneaker platforms. Created for educational purposes and sneaker enthusiasts seeking to understand automated raffle entry techniques.

**[ARCHIVED]**

## The Ultimate Raffle Entry Toolkit

This repository contains a collection of sophisticated raffle entry automation systems engineered for specific sneaker platforms. Each bot is tailored to handle the unique requirements and challenges of its target platform, delivering consistent entries across limited sneaker drops.

![SACAI Bot Success](https://i.imgur.com/lvt88n4.jpeg)

## 🔒 Security & Environment Setup

### Setting Up Environment Variables

This project uses environment variables to securely manage sensitive information like API keys:

1. Copy the `.env.template` file to create your own `.env` file:
   ```bash
   cp .env.template .env
   ```

2. Edit the `.env` file and add your own values:
   ```
   CAPTCHA_API_KEY="your_captcha_service_key"
   NOTRE_SITEKEY="captcha_site_key"
   ```

3. The `.env` file is excluded from git through `.gitignore` to prevent accidental exposure of credentials.

### Security Precautions

- **Never commit sensitive information** directly in the code
- **Never share your `.env` file** with others
- If you've accidentally committed sensitive information, change your credentials immediately
- Use template files for configuration with placeholder values

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/raffle.git
cd raffle

# Set up a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.template .env
# Edit .env with your actual credentials
```

## �� Featured Systems

### Proven Winners

- **[SACAI Bot](SACAI/)** [ARCHIVED] - Sophisticated system for SACAI.jp with account creation, email verification, and multi-threaded entries. Demonstrated multiple wins with **photographic proof of success**.

![SACAI Order](https://i.imgur.com/FTdS6f6.jpeg)

- **[MONKEY Bot](MONKEY/)** [ARCHIVED] - Advanced system for SurveyMonkey-based raffles (like CCS), featuring intelligent form parsing and question answering capabilities. **Documented success** with multiple wins.

![MONKEY Bot Success](https://i.imgur.com/7cToH9Y.jpeg)

### Past Development now Archived

- **[PRODIRECT Bot](PRODIRECT/)** - Specialized for ProDirect's email-based raffles with high-volume entry capabilities.

- **[NOTRE Bot](NOTRE/)** - Engineered for Notre's raffles, featuring captcha solving and question-based verification.

- **[VIRALSWEEP Bot](VIRALSWEEP/)** - Designed for ViralSweep platform raffles with user agent rotation and configurable timing controls.

## ✨ Key Features Across Systems

- **Platform-Specific Optimization**: Each bot is individually tailored to its target platform
- **Address Randomization**: Built-in address jig functions for varied, legitimate-looking submissions
- **Multi-threaded Architecture**: High-volume entry capabilities across all systems
- **Proxy Support**: Compatible with residential and datacenter proxies
- **Email Management**: Various email handling techniques from catchalls to verification
- **Captcha Handling**: Integration with solving services where required
- **Robust Logging**: Detailed logs for monitoring performance

## 📋 Common Requirements

- Python 3.6+
- Requests
- BeautifulSoup4
- Faker
- Proxy lists
- Various platform-specific dependencies

## 🔍 Implementation Notes

The SACAI and MONKEY bots, while now obsolete due to website redesigns, showcase particularly robust methodologies:

1. **SACAI's Multi-Stage Approach**:
   - Account creation with randomized information
   - Email inbox monitoring for verification links
   - Automated link extraction and verification
   - Raffle entry with size selection
   
   This flow demonstrates a complete end-to-end solution for platforms requiring verified accounts.

2. **MONKEY's Form Intelligence**:
   - Dynamic form parsing and question analysis
   - Intelligent question answering
   - Answer selection interfaces for quick configuration
   
   This methodology showcases how to handle complex, variable form structures.

The utils/ directory contains shared tools utilized across multiple systems, particularly for address manipulation, proxy handling, and other common functions.

## 🛠️ Inspiration for Development

While some systems are now obsolete due to website changes, the methodologies and approaches remain valuable for developers interested in:

- Web automation techniques
- Form submission strategies
- Captcha handling processes
- Multi-threaded request management
- Detection avoidance methods

The code is structured to be educational and inspirational rather than immediately operational on current platforms.

## 🧪 Technical Learning Opportunities

Each bot in this suite demonstrates different technical approaches:

- API interaction vs. form submission
- Session management and cookie handling
- Request timing and threading models
- User agent rotation and fingerprinting
- Proxy implementation strategies

---

**Disclaimer**: This toolkit is provided for educational purposes only. Users are responsible for compliance with all applicable terms of service and laws in their jurisdiction.

*"Understanding how systems work is the first step to innovation."* 