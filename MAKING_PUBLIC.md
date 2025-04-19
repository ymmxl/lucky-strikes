# Making This Repository Public: Checklist

Before making this repository public, ensure you've taken all necessary steps to protect sensitive information. This checklist will help you do that safely.

## Pre-Publication Checklist

### 1. Remove Sensitive Files

- [ ] Delete all email lists (`emails.txt`, `emails_fsd.txt`, etc.)
- [ ] Delete all entry data files (`entered.txt`, etc.)
- [ ] Remove API keys from source code
- [ ] Delete any files containing personal information
- [ ] Check research directories for sensitive data
- [ ] Remove all authentication tokens, cookies, and session data

### 2. Use Environment Variables & Templates

- [ ] Ensure all API keys are moved to environment variables
- [ ] Verify `.env.template` exists (without real credentials)
- [ ] Create template config files for each module
- [ ] Ensure `proxies.template.txt` exists (without real proxies)
- [ ] Verify templates are included in version control while real files are ignored

### 3. Clean Git History

- [ ] Follow instructions in `GIT_HISTORY_CLEANUP.md` to clean history
- [ ] Verify sensitive data has been purged using `git log -p`
- [ ] Check that history doesn't contain API keys, email lists, etc.

### 4. Check Documentation

- [ ] README.md has clear setup instructions
- [ ] Security precautions are documented
- [ ] License is appropriate and present
- [ ] Usage guidelines and disclaimers are clear

### 5. Final Verification

- [ ] Clone repo to a new location and check for sensitive data
- [ ] Verify all template files work as expected
- [ ] Test running the code with proper environment variables
- [ ] Review all documentation for accuracy

## Making the Repository Public

Once you've completed the checklist above:

1. Go to your repository on GitHub
2. Click on "Settings"
3. Scroll down to the "Danger Zone"
4. Find "Change repository visibility"
5. Select "Make public"
6. Confirm by typing the repository name

## After Publication

- Monitor the repository for issues or sensitive data that might have been missed
- Regularly review and update documentation
- Consider setting up automated scanning tools to detect secrets in code
- Engage with the community responsibly and emphasize ethical use 