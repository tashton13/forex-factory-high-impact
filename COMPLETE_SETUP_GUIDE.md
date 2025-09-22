# Complete Setup Guide: Forex Factory High-Impact Calendar Automation

## 📋 Prerequisites

Before starting, ensure you have:
- A GitHub account (free tier is sufficient)
- A Google account with Google Calendar access
- Git installed on your computer
- Python 3.11+ installed
- Basic familiarity with command line operations

---

## 🚀 Phase 1: GitHub Repository Setup

### Step 1.1: Create the Repository

1. **Login to GitHub**:
   - Go to [github.com](https://github.com)
   - Sign in with your account

2. **Create New Repository**:
   - Click the green "New" button or the "+" icon in the top right
   - Repository name: `forex-factory-high-impact`
   - Description: `Automated high-impact economic calendar from Forex Factory`
   - Set to **Public** (required for GitHub Pages)
   - ✅ Check "Add a README file"
   - Click "Create repository"

### Step 1.2: Clone and Setup Local Repository

1. **Clone the repository**:
   ```bash
   git clone https://github.com/tashton13/forex-factory-high-impact.git
   cd forex-factory-high-impact
   ```

2. **Copy project files**:
   - Copy all files from your current `MACRO-CALENDAR-AUTOMATION` directory
   - Replace the default README.md with the project README.md

3. **Verify file structure**:
   ```
   forex-factory-high-impact/
   ├── src/
   │   └── forex_calendar_filter.py
   ├── tests/
   │   ├── data/
   │   │   └── sample_calendar.ics
   │   └── test_forex_calendar_filter.py
   ├── .github/
   │   └── workflows/
   │       └── publish.yml
   ├── requirements.txt
   ├── README.md
   ├── GOOGLE_CALENDAR_SETUP.md
   └── COMPLETE_SETUP_GUIDE.md
   ```

### Step 1.3: Push Files to GitHub

1. **Add all files**:
   ```bash
   git add .
   git commit -m "Initial commit: Forex Factory high-impact calendar automation"
   git push origin main
   ```

2. **Verify upload**:
   - Go to your GitHub repository page
   - Confirm all files are visible
   - **Critical check**: Verify the `.github` folder is visible in the repository
   - Click into `.github/workflows/` and confirm `publish.yml` exists
   - Check that the folder structure matches above

---

## ⚙️ Phase 2: GitHub Actions Setup (First Run)

**Important**: We need to run the GitHub Actions workflow first to create the `gh-pages` branch before we can configure GitHub Pages.

### Step 2.1: Note Your Future Pages URL

Your GitHub Pages site will be available at:
```
https://tashton13.github.io/forex-factory-high-impact/
```

**Important**: Replace `tashton13` with your actual GitHub username throughout this guide.

---

## 🤖 Phase 3: GitHub Actions Automation & Pages Setup

### Step 3.1: Trigger First Workflow Run

1. **Check Actions Tab**:
   - Go to the "Actions" tab in your repository
   - You should see "Update Forex Factory High Impact Calendar" workflow listed
   - **If you don't see it**: The workflow file may not have been pushed correctly

2. **If workflow is not visible**:
   - Verify `.github/workflows/publish.yml` exists in your repository
   - Check that you pushed all files including the `.github` folder
   - Refresh the Actions page after confirming the file exists

3. **Manual Trigger**:
   - Click "Update Forex Factory High Impact Calendar"
   - Click "Run workflow" → "Run workflow"
   - Wait 2-3 minutes for completion

2. **Monitor Progress**:
   - Click on the running workflow to see detailed logs
   - Verify all steps complete successfully:
     - ✅ Checkout repository
     - ✅ Set up Python
     - ✅ Install dependencies
     - ✅ Run calendar filter script
     - ✅ Deploy to gh-pages

### Step 3.2: Verify Automation Output

1. **Check gh-pages branch**:
   - After workflow completion, refresh your repository page
   - Switch to the "gh-pages" branch (will now be available in the branch dropdown)
   - Verify these files exist:
     - `high_impact_only.ics`
     - `index.html`

2. **Complete GitHub Pages Setup**:
   - **Now return to Settings → Pages**
   - Source: "Deploy from a branch"
   - Branch: Select "gh-pages" (now available in dropdown)
   - Folder: "/ (root)"
   - Click "Save"
   - Wait 2-3 minutes for deployment

3. **Test the calendar URL**:
   - Visit: `https://tashton13.github.io/forex-factory-high-impact/high_impact_only.ics`
   - Your browser should download an `.ics` file
   - Open the file in a text editor to verify it contains calendar events

4. **Check the webpage**:
   - Visit: `https://tashton13.github.io/forex-factory-high-impact/`
   - Should show a simple page with subscription instructions

---

## 📅 Phase 4: Google Calendar Integration

### Step 4.1: Subscribe to the Calendar Feed

1. **Open Google Calendar**:
   - Go to [calendar.google.com](https://calendar.google.com)
   - Sign in with your Google account

2. **Add Calendar by URL**:
   - In the left sidebar, click the "+" next to "Other calendars"
   - Select "From URL"

3. **Enter the subscription URL**:
   ```
   https://tashton13.github.io/forex-factory-high-impact/high_impact_only.ics
   ```
   - Paste this URL (replace `tashton13` with your username)
   - Click "Add calendar"

### Step 4.2: Configure Calendar Settings

1. **Find your new calendar**:
   - Look for "High Impact Economic Events" in your calendar list
   - It may take a few minutes to appear and sync

2. **Customize appearance**:
   - Click the three dots next to the calendar name
   - Choose a distinctive color (red recommended for high-impact events)
   - Adjust notification settings as desired

3. **Verify events**:
   - Check that economic events appear in your calendar
   - Events should include titles like "GDP Release", "Employment Data", etc.
   - Each event should show impact level and currency information

---

## 🔧 Phase 5: Testing and Validation

### Step 5.1: Local Testing (Optional)

If you want to test the script locally:

1. **Install dependencies**:
   ```bash
   cd forex-factory-high-impact
   pip install -r requirements.txt
   ```

2. **Run the script**:
   ```bash
   cd src
   python forex_calendar_filter.py
   ```

3. **Run tests**:
   ```bash
   cd ..
   python -m pytest tests/ -v
   ```

### Step 5.2: Verify Automation Schedule

1. **Check scheduled runs**:
   - The workflow is set to run daily at 6 AM Toronto time
   - Additional Saturday morning recheck for full coverage
   - You can see upcoming scheduled runs in the Actions tab

2. **Manual trigger anytime**:
   - Go to Actions → "Update Forex Factory High Impact Calendar"
   - Click "Run workflow" to update immediately

---

## 📊 Phase 6: Monitoring and Maintenance

### Step 6.1: Regular Monitoring

1. **Weekly checks**:
   - Verify the Actions tab shows successful runs
   - Check that your Google Calendar has recent events
   - Confirm the GitHub Pages URL still works

2. **Troubleshooting workflow failures**:
   - If a workflow fails, check the logs in the Actions tab
   - Common issues: Network timeouts, Forex Factory site changes
   - Re-run failed workflows by clicking "Re-run jobs"

### Step 6.2: Customization Options

**To modify filtering criteria**:
1. Edit `src/forex_calendar_filter.py`
2. Modify the `HIGH_IMPACT_PATTERNS` list
3. Commit and push changes
4. The automation will use new criteria on next run

**To change update schedule**:
1. Edit `.github/workflows/publish.yml`
2. Modify the `cron` expressions
3. Commit and push changes

---

## 🎯 Phase 7: Final Verification Checklist

### ✅ Repository Setup
- [ ] Repository created and public
- [ ] All project files uploaded
- [ ] GitHub Pages enabled
- [ ] Actions workflow running successfully

### ✅ Calendar Feed
- [ ] ICS file accessible at GitHub Pages URL
- [ ] File contains filtered high-impact events
- [ ] Events have proper formatting and metadata

### ✅ Google Calendar
- [ ] Successfully subscribed to calendar feed
- [ ] "High Impact Economic Events" appears in calendar list
- [ ] Economic events visible in calendar view
- [ ] Events show proper details (title, time, description)

### ✅ Automation
- [ ] GitHub Actions workflow runs without errors
- [ ] Daily schedule configured (6 AM Toronto time)
- [ ] Saturday recheck scheduled
- [ ] Manual trigger works

---

## 🚨 Troubleshooting Common Issues

### Issue: "Update Forex Factory High Impact Calendar" workflow not visible
**Solution**:
1. **Verify file structure**: Ensure `.github/workflows/publish.yml` exists in your repository
2. **Check git push**: Make sure you pushed ALL files including hidden `.github` folder
3. **Repository structure check**: Your repo should show the `.github` folder in the file browser
4. **Enable Actions**: Go to Settings → Actions → General → Allow all actions
5. **Wait and refresh**: Sometimes takes 1-2 minutes for workflows to appear

### Issue: GitHub Pages not working
**Solution**:
1. Ensure repository is public
2. Check that gh-pages branch exists (created after first workflow run)
3. Verify Pages settings point to gh-pages branch
4. Wait up to 10 minutes for initial deployment

### Issue: Calendar not updating in Google
**Solution**:
1. Try removing and re-adding the calendar subscription
2. Verify the ICS URL is accessible in a browser
3. Check that recent GitHub Actions runs completed successfully
4. Google Calendar can take up to 24 hours to sync external calendars

### Issue: No events showing
**Solution**:
1. Check if current week has high-impact events on Forex Factory
2. Verify the workflow completed successfully (check Actions tab)
3. Download and inspect the ICS file manually
4. Run the script locally to debug filtering logic

### Issue: Workflow failing
**Solution**:
1. Check the workflow logs for specific error messages
2. Verify the Forex Factory URL is still accessible
3. Check if any dependencies need updates
4. Re-run the workflow manually

---

## 📞 Support and Next Steps

### Getting Help
- Check the GitHub Issues tab for known problems
- Review workflow logs for detailed error messages
- Ensure your repository follows the exact structure shown above

### Enhancement Ideas
- Add more currency-specific filtering
- Create separate calendars for different impact levels
- Add email notifications for high-impact events
- Integrate with other economic calendar sources

### Security Note
- The automation uses only public data and APIs
- No sensitive credentials are required
- All code is open source and auditable

---

**🎉 Congratulations!** You now have a fully automated, self-updating calendar of high-impact economic events that will keep you informed of the most important market-moving news.

**Final URL**: `https://tashton13.github.io/forex-factory-high-impact/high_impact_only.ics`
**Calendar Name**: "High Impact Economic Events"
**Update Schedule**: Daily at 6 AM Toronto time + Saturday recheck
