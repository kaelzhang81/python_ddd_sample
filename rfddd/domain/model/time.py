import math
import struct
import datetime


def utc_now():
    """A UTC timestamp in seconds.

    When called quickly this function may return the same result twice,
    depending on the precision of the system clock.

    Returns:
        A float timestamp in seconds in the UTC timezone.
    """
    return datetime.datetime.now(datetime.timezone.utc).timestamp()

_previous = utc_now()


def monotonic_utc_now():
    """A UTC timestamp in seconds.

    This function will never return the same value twice. The result
    will always monotonically increase. When called quickly in rapid
    succession the smallest possible float increment will be added
    to the actual timestamp to guarantee monotonicity.

    Returns:
        A float timestamp in seconds in the UTC timezone.
    """
    global _previous
    result = utc_now()
    if result <= _previous:
        result = _next_up(_previous)
    _previous = result
    return result


def _next_up(x):
    """Returns the next-largest float towards positive infinity.

    Args:
        A floating point number.

    Returns:
        The next-largest float towards positive infinity. If NaN
        or positive infinity is passed, the argument is returned.

    """
    if math.isnan(x) or (math.isinf(x) and x > 0):
        return x

    # 0.0 and -0.0 both map to the smallest +ve float.
    if x == 0.0:
        x = 0.0

    n = struct.unpack('<q', struct.pack('<d', x))[0]
    if n >= 0:
        n += 1
    else:
        n -= 1
    return struct.unpack('<d', struct.pack('<q', n))[0]


_MAX_TIMESTAMP = float("inf")
