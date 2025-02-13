from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import pytz


class TimezoneAwareDate:
    """Class to handle day hours calculation considering DST transitions."""

    def __init__(self, date: datetime, timezone: str):
        """
        Args:
            date: The date to calculate hours for
            timezone: The timezone name (e.g., 'Europe/London')
        """
        self.date = date
        self.timezone = timezone

    def _is_dst(self, dt: datetime | None = None) -> bool:
        """Check if a given datetime is in DST for this timezone."""
        if dt is None:
            dt = datetime.now(tz=ZoneInfo(self.timezone))

        timezone = pytz.timezone(self.timezone)
        tz_aware_dt = timezone.localize(dt, is_dst=None)
        return tz_aware_dt.dst() != timedelta(0, 0)

    def is_start_of_dst(self) -> bool:
        """Check if this date is when DST starts (spring forward)."""
        next_day = (self.date + timedelta(days=1)).replace(hour=0)
        return (not self._is_dst(self.date)) and self._is_dst(next_day)

    def is_end_of_dst(self) -> bool:
        """Check if this date is when DST ends (fall back)."""
        next_day = (self.date + timedelta(days=1)).replace(hour=0)
        return self._is_dst(self.date) and (not self._is_dst(next_day))

    def get_day_hours(self) -> int:
        """
        Get the number of hours for this date, considering DST transitions.

        Returns:
            The number of hours for the date
        """
        day_hours: int = 24

        # Check if the date is in the limits of DST
        if self.is_start_of_dst():
            day_hours -= 1
        elif self.is_end_of_dst():
            day_hours += 1

        return day_hours
