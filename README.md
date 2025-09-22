# Forex Factory High Impact Calendar

An automated system that fetches the Forex Factory economic calendar, filters for high-impact events only, and publishes the filtered calendar via GitHub Pages for easy subscription to Google Calendar.

## Features

- 🎯 **Automated Filtering**: Extracts only high-impact (red folder) economic events
- ⏰ **Daily Updates**: Runs automatically every morning at 6 AM Toronto time
- 📅 **Weekly Recheck**: Additional Saturday morning run for full coverage
- 🌐 **Public Access**: Hosted via GitHub Pages for easy calendar subscription
- 🧪 **Tested**: Comprehensive test suite with sample data validation

## Quick Start

### 1. Setup Repository

1. Fork this repository or create a new repository named `forex-factory-high-impact`
2. Enable GitHub Pages in repository settings:
   - Go to Settings → Pages
   - Source: Deploy from a branch
   - Branch: `gh-pages` (will be created automatically)

### 2. Subscribe to Calendar

Once the GitHub Actions workflow runs (automatically or manually), your filtered calendar will be available at:

```
https://[your-username].github.io/forex-factory-high-impact/high_impact_only.ics
```

#### Google Calendar Subscription:
1. Open Google Calendar
2. Click the "+" next to "Other calendars"
3. Select "From URL"
4. Paste the URL above
5. Click "Add calendar"

The calendar will be named "High Impact Economic Events" and will update automatically.

## Technical Details

### Calendar Filtering

Events are considered high-impact if their summary or description contains (case-insensitive):
- `Impact: High`
- `High Impact`
- `Red Folder`
- `Red Impact`
- `Red` (as standalone word)

### Automation Schedule

- **Daily**: 6:00 AM Toronto time (11:00 AM UTC)
- **Weekly**: Saturday 6:00 AM Toronto time (additional recheck)

### Output Format

The generated calendar includes:
- **Filename**: `high_impact_only.ics`
- **Calendar Name**: "High Impact Economic Events"
- **Product ID**: "-//forex-factory-high-impact//EN"
- **Timezone**: America/Toronto

## Development

### Prerequisites

- Python 3.11+
- Required packages (see `requirements.txt`)

### Installation

```bash
# Clone the repository
git clone https://github.com/[your-username]/forex-factory-high-impact.git
cd forex-factory-high-impact

# Install dependencies
pip install -r requirements.txt
```

### Running Locally

```bash
# Run the calendar filter
cd src
python forex_calendar_filter.py

# Run tests
pytest tests/
```

### Testing

The test suite includes:
- High-impact event detection validation
- Calendar filtering accuracy
- ICS file generation and parsing
- Case-insensitive pattern matching
- UID generation for events without UIDs

Run tests with:
```bash
pytest tests/ -v
```

## Project Structure

```
forex-factory-high-impact/
├── src/
│   └── forex_calendar_filter.py    # Main filtering script
├── tests/
│   ├── data/
│   │   └── sample_calendar.ics     # Test data
│   └── test_forex_calendar_filter.py # Test suite
├── .github/
│   └── workflows/
│       └── publish.yml             # GitHub Actions workflow
├── requirements.txt                # Python dependencies
└── README.md                      # This file
```

## Configuration

The script uses these default configurations:

```python
FOREX_FACTORY_ICS_URL = "https://nfs.faireconomy.media/ff_calendar_thisweek.ics"
OUTPUT_FILE = "high_impact_only.ics"
CALENDAR_NAME = "High Impact Economic Events"
```

To modify the source URL or filtering criteria, edit `src/forex_calendar_filter.py`.

## GitHub Actions Workflow

The automation workflow:

1. **Checkout**: Gets the latest code
2. **Setup Python**: Installs Python 3.11
3. **Install Dependencies**: Installs required packages
4. **Run Script**: Executes the calendar filtering
5. **Deploy**: Commits the generated ICS file to `gh-pages` branch

The workflow runs on schedule and can also be triggered manually from the Actions tab.

## Troubleshooting

### Common Issues

1. **Calendar not updating**: Check the Actions tab for workflow run status
2. **Subscription not working**: Verify GitHub Pages is enabled and the URL is correct
3. **No events showing**: Check if there are any high-impact events in the current week

### Logs

View detailed logs in:
- GitHub Actions workflow runs (Actions tab)
- Script output includes event count information

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `pytest tests/`
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For issues or questions:
1. Check the GitHub Issues tab
2. Review the troubleshooting section
3. Create a new issue with detailed information

---

**Last Updated**: Generated automatically by GitHub Actions
