#!/usr/bin/env python3
"""
Forex Factory High Impact Calendar Filter

Fetches the Forex Factory economic calendar ICS feed, filters for high-impact events,
and generates a new .ics file containing only those events.
"""

import re
import hashlib
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional

import requests
from icalendar import Calendar, Event
from dateutil import tz


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configuration
FOREX_FACTORY_ICS_URL = "https://nfs.faireconomy.media/ff_calendar_thisweek.ics"
OUTPUT_FILE = "high_impact_only.ics"
CALENDAR_NAME = "High Impact Economic Events"
PRODID = "-//forex-factory-high-impact//EN"

# High impact indicators (case-insensitive regex patterns)
HIGH_IMPACT_PATTERNS = [
    r"impact:\s*high",
    r"high\s*impact",
    r"red\s*folder",
    r"red\s*impact",
    r"\bred\b"
]


def fetch_calendar_data(url: str) -> str:
    """Fetch ICS calendar data from the given URL."""
    try:
        logger.info(f"Fetching calendar data from: {url}")
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        logger.info(f"Successfully fetched {len(response.text)} characters")
        return response.text
    except requests.RequestException as e:
        logger.error(f"Failed to fetch calendar data: {e}")
        raise


def is_high_impact_event(event: Event) -> bool:
    """Check if an event is high impact based on summary and description."""
    text_to_check = ""
    
    # Get summary/title
    if 'summary' in event:
        text_to_check += str(event['summary']) + " "
    
    # Get description
    if 'description' in event:
        text_to_check += str(event['description']) + " "
    
    # Check against high impact patterns
    text_lower = text_to_check.lower()
    for pattern in HIGH_IMPACT_PATTERNS:
        if re.search(pattern, text_lower):
            logger.debug(f"High impact event found: {event.get('summary', 'No title')}")
            return True
    
    return False


def generate_stable_uid(event: Event) -> str:
    """Generate a stable UID for an event if one doesn't exist."""
    # Use existing UID if available
    if 'uid' in event:
        return str(event['uid'])
    
    # Generate UID from event details
    summary = str(event.get('summary', ''))
    dtstart = str(event.get('dtstart', ''))
    location = str(event.get('location', ''))
    
    uid_source = f"{summary}{dtstart}{location}"
    uid_hash = hashlib.md5(uid_source.encode()).hexdigest()
    return f"{uid_hash}@forex-factory-high-impact"


def filter_high_impact_events(calendar_data: str) -> Calendar:
    """Parse calendar and filter for high impact events."""
    try:
        # Parse the original calendar
        original_cal = Calendar.from_ical(calendar_data)
        logger.info("Successfully parsed original calendar")
        
        # Create new calendar for filtered events
        filtered_cal = Calendar()
        filtered_cal.add('prodid', PRODID)
        filtered_cal.add('version', '2.0')
        filtered_cal.add('calscale', 'GREGORIAN')
        filtered_cal.add('method', 'PUBLISH')
        filtered_cal.add('x-wr-calname', CALENDAR_NAME)
        filtered_cal.add('x-wr-timezone', 'America/Toronto')
        
        high_impact_count = 0
        total_events = 0
        
        # Filter events
        for component in original_cal.walk():
            if component.name == "VEVENT":
                total_events += 1
                if is_high_impact_event(component):
                    # Ensure the event has a UID
                    if 'uid' not in component:
                        component.add('uid', generate_stable_uid(component))
                    
                    filtered_cal.add_component(component)
                    high_impact_count += 1
        
        logger.info(f"Filtered {high_impact_count} high impact events from {total_events} total events")
        return filtered_cal
        
    except Exception as e:
        logger.error(f"Failed to parse/filter calendar: {e}")
        raise


def save_calendar(calendar: Calendar, output_path: str) -> None:
    """Save the filtered calendar to an ICS file."""
    try:
        output_file = Path(output_path)
        with open(output_file, 'wb') as f:
            f.write(calendar.to_ical())
        logger.info(f"Saved filtered calendar to: {output_file.absolute()}")
    except Exception as e:
        logger.error(f"Failed to save calendar: {e}")
        raise


def main():
    """Main function to fetch, filter, and save the calendar."""
    try:
        # Fetch calendar data
        calendar_data = fetch_calendar_data(FOREX_FACTORY_ICS_URL)
        
        # Filter for high impact events
        filtered_calendar = filter_high_impact_events(calendar_data)
        
        # Save the filtered calendar
        save_calendar(filtered_calendar, OUTPUT_FILE)
        
        print(f"Generated file: {OUTPUT_FILE}")
        print(f"Published at: https://tashton13.github.io/forex-factory-high-impact/{OUTPUT_FILE}")
        print(f"Subscribed Google Calendar: {CALENDAR_NAME}")
        
    except Exception as e:
        logger.error(f"Script failed: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
