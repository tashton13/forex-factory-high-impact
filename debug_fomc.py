#!/usr/bin/env python3
"""Debug script to test FOMC detection"""

import sys
import re
sys.path.append('.')
from forex_calendar_filter import *
from icalendar import Event

def test_fomc_detection():
    # Test the FOMC detection
    event = Event()
    event.add('summary', 'FOMC Member Barkin Speaks')
    event.add('description', 'Impact: Medium - Federal Reserve official speech')

    print('=== Testing FOMC Detection ===')
    print(f'Event: {event.get("summary")}')
    print(f'Red folder event: {is_red_folder_event(event)}')
    print(f'VIP medium impact: {is_vip_medium_impact_event(event)}')
    print(f'Should include: {should_include_event(event)}')

    # Let's also check what patterns we're matching
    text = 'FOMC Member Barkin Speaks Impact: Medium - Federal Reserve official speech'
    print(f'\nText to match: {text}')
    print(f'Text lowercased: {text.lower()}')
    
    print('\n=== Medium Impact Pattern Check ===')
    for pattern in MEDIUM_IMPACT_PATTERNS:
        if re.search(pattern, text.lower()):
            print(f'✓ Medium impact pattern matched: {pattern}')
            medium_found = True
            break
    else:
        print('✗ No medium impact pattern matched')
        medium_found = False

    print('\n=== VIP Keyword Check ===')
    for keyword in VIP_KEYWORDS:
        if re.search(keyword, text.lower()):
            print(f'✓ VIP keyword matched: {keyword}')
            vip_found = True
            break
    else:
        print('✗ No VIP keyword matched')
        vip_found = False

    print(f'\nMedium found: {medium_found}, VIP found: {vip_found}')
    
    # Test with different variations
    print('\n=== Testing Variations ===')
    variations = [
        'FOMC Member Barkin Speaks',
        'fomc member speaks',
        'Federal Reserve FOMC',
        'Gov Bailey speaks',
        'President Lagarde announcement',
        'Trump speech'
    ]
    
    for variation in variations:
        for keyword in VIP_KEYWORDS:
            if re.search(keyword, variation.lower()):
                print(f'✓ "{variation}" matches keyword: {keyword}')
                break
        else:
            print(f'✗ "{variation}" - no VIP keyword match')

if __name__ == "__main__":
    test_fomc_detection()
