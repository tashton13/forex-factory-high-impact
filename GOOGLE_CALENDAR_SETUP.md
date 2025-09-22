# Google Calendar Setup Instructions

## Step-by-Step Guide to Subscribe to the High Impact Economic Calendar

### 1. Repository Setup

First, ensure your GitHub repository is properly configured:

1. **Create Repository**: Create a new repository named `forex-factory-high-impact` on GitHub
2. **Upload Files**: Push all the project files to your repository
3. **Enable GitHub Pages**:
   - Go to your repository Settings
   - Navigate to "Pages" in the left sidebar
   - Under "Source", select "Deploy from a branch"
   - Choose "gh-pages" as the branch (will be created automatically by the workflow)
   - Click "Save"

### 2. Trigger the Automation

The GitHub Actions workflow will run automatically, but you can trigger it manually:

1. Go to the "Actions" tab in your repository
2. Click on "Update Forex Factory High Impact Calendar" workflow
3. Click "Run workflow" → "Run workflow"
4. Wait for the workflow to complete (usually 1-2 minutes)

### 3. Verify the Calendar Feed

Once the workflow completes:

1. Your calendar will be available at: `https://[your-username].github.io/forex-factory-high-impact/high_impact_only.ics`
2. Test the URL in your browser - it should download an `.ics` file
3. The GitHub Pages site will also show a simple page with subscription instructions

### 4. Subscribe to Google Calendar

#### Method 1: Direct Subscription (Recommended)

1. **Open Google Calendar** (calendar.google.com)
2. **Add Calendar**:
   - Click the "+" next to "Other calendars" in the left sidebar
   - Select "From URL"
3. **Enter URL**:
   - Paste: `https://[your-username].github.io/forex-factory-high-impact/high_impact_only.ics`
   - Replace `[your-username]` with your actual GitHub username
4. **Add Calendar**:
   - Click "Add calendar"
   - Google Calendar will automatically fetch and subscribe to the feed

#### Method 2: Manual Import (Alternative)

1. **Download the ICS file** from the GitHub Pages URL
2. **Import to Google Calendar**:
   - In Google Calendar, click the gear icon → "Settings"
   - Click "Import & export" in the left sidebar
   - Click "Select file from your computer"
   - Choose the downloaded `.ics` file
   - Select which calendar to add events to
   - Click "Import"

**Note**: Method 1 (subscription) is preferred as it will automatically update when new events are published.

### 5. Calendar Settings

After subscription, you can customize your calendar:

1. **Calendar Name**: Will appear as "High Impact Economic Events"
2. **Color**: Choose a distinctive color (red recommended for high-impact events)
3. **Notifications**: Set up notifications for important events
4. **Visibility**: Make it visible/hidden as needed

### 6. Verification

To verify everything is working:

1. **Check Events**: You should see high-impact economic events in your calendar
2. **Event Details**: Events should include:
   - Event title (e.g., "GDP Release")
   - Time and date
   - Currency/location information
   - Impact level in description
3. **Updates**: The calendar will automatically refresh daily at 6 AM Toronto time

### 7. Troubleshooting

#### Calendar Not Updating
- Check that GitHub Actions workflow is running successfully
- Verify GitHub Pages is enabled and working
- Try re-subscribing to the calendar URL

#### No Events Showing
- Verify the current week has high-impact events in Forex Factory
- Check that the workflow completed successfully
- Ensure the URL is correct and accessible

#### Subscription Issues
- Try using the direct ICS file URL instead of the GitHub Pages URL
- Clear browser cache and retry
- Use Method 2 (manual import) as a fallback

### 8. Automation Schedule

Your calendar will automatically update:
- **Daily**: 6:00 AM Toronto time (11:00 AM UTC)
- **Weekly**: Saturday 6:00 AM Toronto time (additional recheck)
- **Manual**: You can trigger updates anytime from GitHub Actions

### 9. Multiple Calendars

To create additional filtered calendars:
1. Fork the repository
2. Modify the filtering criteria in `src/forex_calendar_filter.py`
3. Change the calendar name and output file name
4. Follow the same setup process

---

**Calendar URL Template**: `https://[your-username].github.io/forex-factory-high-impact/high_impact_only.ics`

**Example**: `https://tashton13.github.io/forex-factory-high-impact/high_impact_only.ics`
