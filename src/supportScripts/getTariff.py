import argparse
import unittest
from datetime import datetime

from supportScripts.connectorWorkFreeDays.connectorWorkFreeDays import isWorkFreeDay

# Define the updated tariff structure based on the table
tariff_structure = {
    'higher': {
        'workday': [
            {'start': 7,  'end': 14, 'tariff': 1},  # Block 1
            {'start': 6,  'end': 7,  'tariff': 2},  # Block 2
            {'start': 14, 'end': 16, 'tariff': 2},  # Block 2
            {'start': 20, 'end': 22, 'tariff': 2},  # Block 2
            {'start': 16, 'end': 20, 'tariff': 1},  # Block 1
            {'start': 0,  'end': 6,  'tariff': 5},  # Block 5
            {'start': 22, 'end': 24, 'tariff': 5},  # Block 5
        ],
        'weekend': [
            {'start': 7,  'end': 14, 'tariff': 1},  # Block 1
            {'start': 16, 'end': 20, 'tariff': 1},  # Block 1
            {'start': 6,  'end': 7,  'tariff': 3},  # Block 3
            {'start': 14, 'end': 16, 'tariff': 3},  # Block 3
            {'start': 20, 'end': 22, 'tariff': 3},  # Block 3
            {'start': 0,  'end': 6,  'tariff': 5},  # Block 5
            {'start': 22, 'end': 24, 'tariff': 5},  # Block 5
        ]
    },
    'lower': {
        'workday': [
            {'start': 7,  'end': 14, 'tariff': 1},  # Block 1
            {'start': 16, 'end': 20, 'tariff': 1},  # Block 1
            {'start': 6,  'end': 7,  'tariff': 2},  # Block 2
            {'start': 14, 'end': 16, 'tariff': 2},  # Block 2
            {'start': 20, 'end': 22, 'tariff': 2},  # Block 2
            {'start': 0,  'end': 6,  'tariff': 4},  # Block 4
            {'start': 22, 'end': 24, 'tariff': 4},  # Block 4
        ],
        'weekend': [
            {'start': 7,  'end': 14, 'tariff': 1},  # Block 1
            {'start': 16, 'end': 20, 'tariff': 1},  # Block 1
            {'start': 6,  'end': 7,  'tariff': 3},  # Block 3
            {'start': 14, 'end': 16, 'tariff': 3},  # Block 3
            {'start': 20, 'end': 22, 'tariff': 3},  # Block 3
            {'start': 0,  'end': 6,  'tariff': 4},  # Block 4
            {'start': 22, 'end': 24, 'tariff': 4},  # Block 4
        ]
    }
}



def is_weekend(date_time):
    """Check if the current day is a weekend."""
    return date_time.weekday() >= 5  # 5 = Saturday, 6 = Sunday

def get_tariff(date_time: datetime, tariff_structure: dict) -> int:
    # Define periods for summer and winter (higher and lower seasons)
    higher_season_start = datetime(date_time.year, 6, 1)
    higher_season_end = datetime(date_time.year, 8, 31)
    
    # Check if it's higher or lower season
    if higher_season_start <= date_time <= higher_season_end:
        season = 'higher'
    else:
        season = 'lower'
    
    # Check if it's a weekend or holiday

    countryIso2 = "SI";
    
    
    if isWorkFreeDay(date_time, countryIso2) or is_weekend(date_time):
        day_type = 'weekend'
    else:
        day_type = 'workday'
    
    # Get the appropriate tariff periods for the current season and day type
    tariff_periods = tariff_structure[season][day_type]
    
    # Determine which time period the current time falls into
    for period in tariff_periods:
        if period['start'] <= date_time.hour < period['end']:
            return period['tariff']
    
    # Default case if no period is matched (which shouldn't happen)
    return -1  # Error code, indicating no valid tariff found

# Main function to accept date and time input from the command line
def main():
    parser = argparse.ArgumentParser(description="Tariff calculation based on date and time.")
    parser.add_argument('date_input', type=str, help="Date input in YYYY-MM-DD format")
    parser.add_argument('time_input', type=str, help="Time input in HH:MM format")
    
    args = parser.parse_args()
    
    try:
        # Parse the date and time input
        date_time_str = f"{args.date_input} {args.time_input}"
        date_time = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M")
        
        # Get the tariff
        tariff = get_tariff(date_time, tariff_structure)
        print(f"The tariff band is: {tariff}")
    
    except ValueError as e:
        print(f"Invalid input: {e}")

if __name__ == "__main__":
    main()


class TestTariffCalculation(unittest.TestCase):

    def test_summer_workday_morning(self):
        """Test tariff during a summer workday morning (Block 1)"""
        date_time = datetime(2024, 7, 15, 9, 0)  # July 15, 9:00 AM (summer, workday)
        expected_tariff = 1  # Block 1 for workday
        self.assertEqual(get_tariff(date_time, tariff_structure), expected_tariff)

    def test_summer_weekend_evening(self):
        """Test tariff during a summer weekend evening (Block 5)"""
        date_time = datetime(2024, 7, 13, 22, 0)  # July 13, 10:00 PM (summer, weekend)
        expected_tariff = 5  # Block 5 for weekend
        self.assertEqual(get_tariff(date_time, tariff_structure), expected_tariff)

    def test_winter_workday_afternoon(self):
        """Test tariff during a winter workday afternoon (Block 2)"""
        date_time = datetime(2024, 12, 15, 14, 30)  # December 15, 2:30 PM (winter, workday)
        expected_tariff = 2  # Block 2 for workday
        self.assertEqual(get_tariff(date_time, tariff_structure), expected_tariff)

    def test_winter_weekend_night(self):
        """Test tariff during a winter weekend night (Block 4)"""
        date_time = datetime(2024, 12, 16, 5, 0)  # December 16, 5:00 AM (winter, weekend)
        expected_tariff = 4  # Block 4 for weekend
        self.assertEqual(get_tariff(date_time, tariff_structure), expected_tariff)

    def test_holiday_tariff(self):
        """Test tariff on a holiday (treated as weekend)"""
        date_time = datetime(2024, 12, 25, 14, 0)  # December 25, 2:00 PM (holiday)
        expected_tariff = 3  # Block 3 for weekend (because holiday is treated as a weekend)
        self.assertEqual(get_tariff(date_time, tariff_structure), expected_tariff)

    def test_invalid_date_format(self):
        """Test handling of an invalid date format"""
        with self.assertRaises(ValueError):
            date_time_str = "invalid date"  # Invalid date string
            datetime.strptime(date_time_str, "%Y-%m-%d %H:%M")

if __name__ == '__main__':
    unittest.main()