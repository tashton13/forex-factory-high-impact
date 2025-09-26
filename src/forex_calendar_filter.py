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
FOREX_FACTORY_BASE_URL = "https://nfs.faireconomy.media/ff_calendar_"
OUTPUT_FILE = "enhanced_economic_calendar.ics"
CALENDAR_NAME = "Enhanced Economic Events (3-Week Outlook)"
PRODID = "-//forex-factory-enhanced//EN"

# High impact indicators (case-insensitive regex patterns) - RED FOLDER ITEMS
RED_FOLDER_PATTERNS = [
    r"impact:\s*high",
    r"high\s*impact", 
    r"red\s*folder",
    r"red\s*impact",
    r"\bred\b"
]

# Medium impact indicators (yellow/orange folder) - SELECTIVE KEYWORDS
MEDIUM_IMPACT_PATTERNS = [
    r"impact:\s*medium",
    r"medium\s*impact",
    r"yellow\s*folder", 
    r"orange\s*folder",
    r"\byellow\b",
    r"\borange\b"
]

# VIP Keywords for medium impact events (case-insensitive)
VIP_KEYWORDS = [
    r"\btrump\b",
    r"\bfomc\b", 
    r"\bopec\b",
    r"president\s+lagarde",
    r"lagarde\b",
    r"gov\s+bailey",
    r"governor\s+bailey",
    r"\bbailey\b"
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


def fetch_multi_week_calendar_data(weeks: int = 3) -> str:
    """Fetch multiple weeks of calendar data and combine them."""
    all_calendar_data = []
    
    # Primary URL that definitely works
    primary_url = f"{FOREX_FACTORY_BASE_URL}thisweek.ics"
    
    # Alternative URLs to try for more weeks
    week_urls = [
        primary_url,
        f"{FOREX_FACTORY_BASE_URL}nextweek.ics",
        f"{FOREX_FACTORY_BASE_URL}week3.ics",
        f"{FOREX_FACTORY_BASE_URL}week2.ics",
        "https://www.forexfactory.com/calendar.ics"
    ]
    
    # Always fetch at least the current week
    try:
        logger.info("Fetching current week calendar data...")
        data = fetch_calendar_data(primary_url)
        all_calendar_data.append(data)
    except Exception as e:
        logger.error(f"Failed to fetch current week data: {e}")
        raise Exception("Cannot proceed without current week data")
    
    # Try to fetch additional weeks
    for i, url in enumerate(week_urls[1:weeks], 2):
        try:
            logger.info(f"Attempting to fetch week {i} calendar data...")
            data = fetch_calendar_data(url)
            all_calendar_data.append(data)
        except Exception as e:
            logger.warning(f"Week {i} not available ({e}), continuing with available data")
            continue
    
    logger.info(f"Successfully fetched {len(all_calendar_data)} weeks of calendar data")
    return all_calendar_data


def is_red_folder_event(event: Event) -> bool:
    """Check if an event is red folder (high impact)."""
    text_to_check = ""
    
    # Get summary/title
    if 'summary' in event:
        text_to_check += str(event['summary']) + " "
    
    # Get description
    if 'description' in event:
        text_to_check += str(event['description']) + " "
    
    # Check against red folder patterns
    text_lower = text_to_check.lower()
    for pattern in RED_FOLDER_PATTERNS:
        if re.search(pattern, text_lower):
            return True
    
    return False


def is_vip_keyword_event(event: Event) -> bool:
    """Check if an event contains VIP keywords (regardless of impact level)."""
    text_to_check = ""
    
    # Get summary/title
    if 'summary' in event:
        text_to_check += str(event['summary']) + " "
    
    # Get description
    if 'description' in event:
        text_to_check += str(event['description']) + " "
    
    text_lower = text_to_check.lower()
    
    # Check for VIP keywords regardless of impact level
    for keyword in VIP_KEYWORDS:
        if re.search(keyword, text_lower):
            logger.debug(f"VIP keyword event found: {event.get('summary', 'No title')} (keyword: {keyword})")
            return True
    
    return False


def should_include_event(event: Event) -> bool:
    """Determine if an event should be included in the filtered calendar."""
    # Include all red folder events
    if is_red_folder_event(event):
        logger.debug(f"Red folder event: {event.get('summary', 'No title')}")
        return True
    
    # Include ANY event with VIP keywords (regardless of impact level)
    if is_vip_keyword_event(event):
        logger.debug(f"VIP keyword event: {event.get('summary', 'No title')}")
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


def filter_enhanced_events(calendar_data_list: List[str]) -> Calendar:
    """Parse multiple weeks of calendar data and filter for enhanced events."""
    try:
        # Create new calendar for filtered events
        filtered_cal = Calendar()
        filtered_cal.add('prodid', PRODID)
        filtered_cal.add('version', '2.0')
        filtered_cal.add('calscale', 'GREGORIAN')
        filtered_cal.add('method', 'PUBLISH')
        filtered_cal.add('x-wr-calname', CALENDAR_NAME)
        filtered_cal.add('x-wr-timezone', 'America/Toronto')
        
        total_included = 0
        total_events = 0
        red_folder_count = 0
        vip_keyword_count = 0
        seen_uids = set()  # To avoid duplicates across weeks
        
        # Process each week's calendar data
        for week_num, calendar_data in enumerate(calendar_data_list, 1):
            try:
                original_cal = Calendar.from_ical(calendar_data)
                logger.info(f"Successfully parsed week {week_num} calendar")
                
                # Filter events from this week
                for component in original_cal.walk():
                    if component.name == "VEVENT":
                        total_events += 1
                        
                        if should_include_event(component):
                            # Ensure the event has a UID
                            if 'uid' not in component:
                                component.add('uid', generate_stable_uid(component))
                            
                            # Check for duplicates across weeks
                            event_uid = str(component['uid'])
                            if event_uid not in seen_uids:
                                seen_uids.add(event_uid)
                                filtered_cal.add_component(component)
                                total_included += 1
                                
                                # Count event types
                                if is_red_folder_event(component):
                                    red_folder_count += 1
                                elif is_vip_keyword_event(component):
                                    vip_keyword_count += 1
                            
            except Exception as e:
                logger.warning(f"Failed to parse week {week_num} calendar: {e}")
                continue
        
        logger.info(f"Filtered {total_included} events from {total_events} total events across {len(calendar_data_list)} weeks")
        logger.info(f"  - {red_folder_count} red folder (high impact) events")
        logger.info(f"  - {vip_keyword_count} VIP keyword events (any impact level)")
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
    """Main function to fetch, filter, and save the enhanced calendar."""
    try:
        # Fetch 3 weeks of calendar data
        calendar_data_list = fetch_multi_week_calendar_data(weeks=3)
        
        # Filter for enhanced events (red folder + VIP medium impact)
        filtered_calendar = filter_enhanced_events(calendar_data_list)
        
        # Save the filtered calendar
        save_calendar(filtered_calendar, OUTPUT_FILE)
        
        print(f"Generated file: {OUTPUT_FILE}")
        print(f"Published at: https://tashton13.github.io/forex-factory-high-impact/{OUTPUT_FILE}")
        print(f"Subscribed Google Calendar: {CALENDAR_NAME}")
        print(f"Enhanced filtering: All red folder events + ALL VIP keyword events (any impact)")
        print(f"VIP Keywords: Trump, FOMC, OPEC, Lagarde, Bailey")
        print(f"Coverage: 3 weeks ahead with daily updates")
        
    except Exception as e:
        logger.error(f"Script failed: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
