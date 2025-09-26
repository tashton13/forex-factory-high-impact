#!/usr/bin/env python3
"""
Tests for Forex Factory High Impact Calendar Filter
"""

import pytest
from pathlib import Path
import sys
import tempfile
import os

# Add src directory to path for imports
src_dir = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_dir))

from forex_calendar_filter import (
    filter_enhanced_events,
    should_include_event,
    is_red_folder_event,
    is_vip_medium_impact_event,
    generate_stable_uid,
    save_calendar
)
from icalendar import Calendar, Event


class TestForexCalendarFilter:
    """Test cases for the Forex calendar filtering functionality."""
    
    @pytest.fixture
    def sample_calendar_data(self):
        """Load sample calendar data for testing."""
        test_data_path = Path(__file__).parent / "data" / "sample_calendar.ics"
        with open(test_data_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def test_red_folder_detection_impact_high(self):
        """Test detection of 'Impact: High' events."""
        event = Event()
        event.add('summary', 'GDP Release')
        event.add('description', 'Impact: High - Major economic indicator')
        
        assert is_red_folder_event(event) == True
        assert should_include_event(event) == True
    
    def test_red_folder_detection_red_folder(self):
        """Test detection of 'red folder' events."""
        event = Event()
        event.add('summary', 'Red Folder Inflation Report')
        event.add('description', 'This is marked as red impact level')
        
        assert is_red_folder_event(event) == True
        assert should_include_event(event) == True
    
    def test_vip_medium_impact_detection(self):
        """Test detection of VIP medium impact events."""
        event = Event()
        event.add('summary', 'FOMC Meeting Minutes')
        event.add('description', 'Impact: Medium - Federal Reserve meeting')
        
        assert is_vip_medium_impact_event(event) == True
        assert should_include_event(event) == True
    
    def test_trump_vip_keyword(self):
        """Test detection of Trump VIP keyword."""
        event = Event()
        event.add('summary', 'Trump Speech on Trade Policy')
        event.add('description', 'Impact: Medium - Presidential announcement')
        
        assert is_vip_medium_impact_event(event) == True
        assert should_include_event(event) == True
    
    def test_low_impact_not_vip(self):
        """Test that low impact events are not detected."""
        event = Event()
        event.add('summary', 'Minor Employment Data')
        event.add('description', 'Impact: Low - Minor indicator')
        
        assert is_red_folder_event(event) == False
        assert is_vip_medium_impact_event(event) == False
        assert should_include_event(event) == False
    
    def test_medium_impact_without_vip(self):
        """Test that medium impact events without VIP keywords are not included."""
        event = Event()
        event.add('summary', 'Regular Housing Data')
        event.add('description', 'Impact: Medium - Housing statistics')
        
        assert is_red_folder_event(event) == False
        assert is_vip_medium_impact_event(event) == False
        assert should_include_event(event) == False
    
    def test_filter_enhanced_events(self, sample_calendar_data):
        """Test filtering of enhanced events from sample data."""
        filtered_cal = filter_enhanced_events([sample_calendar_data])
        
        # Count events in filtered calendar
        event_count = 0
        high_impact_summaries = []
        
        for component in filtered_cal.walk():
            if component.name == "VEVENT":
                event_count += 1
                high_impact_summaries.append(str(component.get('summary', '')))
        
        # Should have 2 high impact events based on sample data
        assert event_count == 2
        assert 'High Impact GDP Release' in high_impact_summaries
        assert 'Red Folder Inflation Report' in high_impact_summaries
        assert 'Low Impact Employment Data' not in high_impact_summaries
        assert 'Medium Impact Trade Balance' not in high_impact_summaries
    
    def test_calendar_metadata(self, sample_calendar_data):
        """Test that filtered calendar has correct metadata."""
        filtered_cal = filter_enhanced_events([sample_calendar_data])
        
        assert str(filtered_cal.get('prodid')) == '-//forex-factory-enhanced//EN'
        assert str(filtered_cal.get('x-wr-calname')) == 'Enhanced Economic Events (3-Week Outlook)'
        assert str(filtered_cal.get('version')) == '2.0'
    
    def test_uid_generation(self):
        """Test UID generation for events without UIDs."""
        from datetime import datetime, timezone
        
        event = Event()
        event.add('summary', 'Test Event')
        event.add('dtstart', datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc))
        event.add('location', 'USD')
        
        uid1 = generate_stable_uid(event)
        uid2 = generate_stable_uid(event)
        
        # Should generate consistent UIDs
        assert uid1 == uid2
        assert '@forex-factory-high-impact' in uid1
    
    def test_save_and_reload_calendar(self, sample_calendar_data):
        """Test saving calendar and reloading it as valid ICS."""
        filtered_cal = filter_enhanced_events([sample_calendar_data])
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(mode='wb', suffix='.ics', delete=False) as tmp_file:
            tmp_path = tmp_file.name
            
        try:
            save_calendar(filtered_cal, tmp_path)
            
            # Verify file exists and is readable
            assert os.path.exists(tmp_path)
            assert os.path.getsize(tmp_path) > 0
            
            # Try to parse the saved file
            with open(tmp_path, 'rb') as f:
                reloaded_cal = Calendar.from_ical(f.read())
            
            # Verify it's a valid calendar
            assert reloaded_cal.get('version') is not None
            
            # Count events in reloaded calendar
            event_count = 0
            for component in reloaded_cal.walk():
                if component.name == "VEVENT":
                    event_count += 1
            
            assert event_count == 2  # Should have 2 high impact events
            
        finally:
            # Clean up
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
    
    def test_case_insensitive_matching(self):
        """Test that impact matching is case insensitive."""
        red_folder_cases = [
            ('IMPACT: HIGH', True),
            ('impact: high', True),
            ('Impact: High', True),
            ('HIGH IMPACT EVENT', True),
            ('red folder analysis', True),
            ('RED IMPACT LEVEL', True),
        ]
        
        for description, expected in red_folder_cases:
            event = Event()
            event.add('summary', 'Test Event')
            event.add('description', description)
            
            result = is_red_folder_event(event)
            assert result == expected, f"Red folder test failed for: {description}"
        
        vip_medium_cases = [
            ('Impact: Medium - FOMC meeting', True),
            ('Trump announcement - medium impact', True),
            ('Governor Bailey speech - medium', True),
            ('impact: medium regular data', False),
            ('low impact', False),
        ]
        
        for description, expected in vip_medium_cases:
            event = Event()
            event.add('summary', 'Test Event')
            event.add('description', description)
            
            result = is_vip_medium_impact_event(event)
            assert result == expected, f"VIP medium test failed for: {description}"


if __name__ == "__main__":
    pytest.main([__file__])
