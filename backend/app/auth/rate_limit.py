from datetime import datetime, timedelta
from typing import Dict, Optional
import time
from fastapi import HTTPException, status
from collections import defaultdict

# In-memory storage for rate limiting (in production, use Redis or similar)
# Structure: {ip_address: [(timestamp, attempt_count)]}
failed_attempts: Dict[str, list] = defaultdict(list)


def check_rate_limit(ip_address: str, max_attempts: int = 5, window_minutes: int = 15) -> bool:
    """
    Check if the IP address has exceeded the rate limit for failed attempts.

    Args:
        ip_address: The IP address to check
        max_attempts: Maximum number of attempts allowed (default: 5)
        window_minutes: Time window in minutes (default: 15)

    Returns:
        bool: True if within rate limit, False if exceeded
    """
    current_time = datetime.utcnow()
    window_start = current_time - timedelta(minutes=window_minutes)

    # Clean up old attempts outside the window
    if ip_address in failed_attempts:
        failed_attempts[ip_address] = [
            attempt_time for attempt_time in failed_attempts[ip_address]
            if attempt_time > window_start
        ]

    # Check if within rate limit
    if len(failed_attempts[ip_address]) >= max_attempts:
        return False

    return True


def record_failed_attempt(ip_address: str):
    """
    Record a failed authentication attempt for the given IP address.

    Args:
        ip_address: The IP address of the failed attempt
    """
    failed_attempts[ip_address].append(datetime.utcnow())


def reset_attempts(ip_address: str):
    """
    Reset failed attempts for the given IP address (e.g., after successful auth).

    Args:
        ip_address: The IP address to reset
    """
    if ip_address in failed_attempts:
        del failed_attempts[ip_address]


# Middleware function to apply rate limiting
async def apply_rate_limit(ip_address: str):
    """
    Apply rate limiting to an authentication endpoint.

    Args:
        ip_address: The IP address making the request

    Raises:
        HTTPException: If rate limit is exceeded
    """
    if not check_rate_limit(ip_address):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many authentication attempts. Please try again later."
        )