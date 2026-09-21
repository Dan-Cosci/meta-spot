from datetime import datetime

from core import api_settings

get_current_timestamp = lambda: datetime.now().timestamp()
time_expires_in = lambda base: base + api_settings["expires_in"]
