# Git History Cleanup Guide

This guide explains how to clean sensitive information from your Git history before making the repository public.

## Why Clean Git History?

Even if you've removed sensitive files from your current codebase, they may still be accessible in your Git history. Anyone with access to your repository can view previous commits and potentially extract sensitive information.

## Using BFG Repo-Cleaner

BFG Repo-Cleaner is a faster, simpler alternative to `git filter-branch` for removing unwanted data from Git repositories.

### 1. Install BFG

Download the BFG jar file from the [official website](https://rtyley.github.io/bfg-repo-cleaner/).

```bash
# On macOS with Homebrew
brew install bfg

# Or download the jar file
wget https://repo1.maven.org/maven2/com/madgag/bfg/1.14.0/bfg-1.14.0.jar -O bfg.jar
```

### 2. Create a Fresh Clone of Your Repository

BFG needs a fresh clone to work effectively:

```bash
# Create a fresh, mirror clone of your repository
git clone --mirror git://github.com/yourusername/raffle.git raffle-mirror
```

### 3. Run BFG to Remove Sensitive Files

```bash
# Remove files containing sensitive data (using patterns)
java -jar bfg.jar --delete-files "*credentials*" raffle-mirror
java -jar bfg.jar --delete-files "entered.txt" raffle-mirror
java -jar bfg.jar --delete-files "emails*.txt" raffle-mirror
java -jar bfg.jar --delete-files "*proxies*.txt" raffle-mirror
java -jar bfg.jar --delete-files "*secret*" raffle-mirror

# Or remove text within files (replace PATTERN with your API key or other sensitive data)
java -jar bfg.jar --replace-text passwords.txt raffle-mirror
```

Create a `passwords.txt` file with patterns like:
```
APIKEY = "6b2cda1c0a44874df55ea050f854f8a5" ==> APIKEY = "***REMOVED***"
```

### 4. Clean and Update the Repository

```bash
# Go into the mirrored repository
cd raffle-mirror

# Strip out the unwanted dirty data
git reflog expire --expire=now --all && git gc --prune=now --aggressive

# Push the cleaned history to GitHub
git push
```

### 5. Refresh Your Working Copy

```bash
# Clone the repository with the cleaned history
git clone git://github.com/yourusername/raffle.git clean-raffle
```

## Important Notes

- Always change sensitive information (API keys, passwords) after cleaning your repository, as they should be considered compromised.
- After cleaning, all collaborators should clone a fresh copy of the repository.
- This process rewrites Git history and changes commit hashes, which can impact collaboration workflows.

## Further Resources

- [BFG Repo-Cleaner Documentation](https://rtyley.github.io/bfg-repo-cleaner/)
- [GitHub Help: Removing sensitive data from a repository](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository) 