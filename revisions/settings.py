import os

from django.conf import settings

REVISIONS_DATE_DELTA       = 3

REVISIONS_EVENTDATE_FMT    = "%Y%m%d"

# REVISIONS_EVENT_QUERY      = "SELECT * FROM Events WHERE EventStartDate > '{start_date}' AND EventStartDate < '{end_date}'"
REVISIONS_EVENT_QUERY      = "SELECT * FROM Events WHERE EventStartDate > '{start_date:%Y%m%d}' AND EventStartDate < '{end_date:%Y%m%d}'"

REVISIONS_DBISAM_UTILITY   = os.path.abspath('../bin/dbisam_utility/dbisam_utility.exe')

REVISIONS_EMAIL_SENDER     = ""

REVISIONS_EMAIL_RECIPIENTS = [

]
 
REVISIONS_UPDATE_INTERVAL = 3

REVISIONS_KEY = """ZjFmNWM5MjYxODQ2Y2E3MDUzMDM1OWI5YjhjYjA1ZjZhNjRjMGEwNTqAAl1xAShVCGpvbmF0aGFu
cQJVCGF5bGp3cTA5cQNlLg==
"""