Event Note Updates for EventPath.

What is Event Note Updates?

This application queries the EventPath database and checks for revisions made to Event Notes. 
Revisions found are collected and periodically emailed to select user groups, throughout the work day. 
Digest emails highlight the difference between the current text and the previous. 
Users may also log in to view current and past revisions for an event, or for a specific date.


Why Event Note Updates?

This application was created to solve the issue of changes made to an event's note fields going unnoticed. 
The note field for an Event is a free form field where staff can input a wide variety of information pertaining to their event. 
It's common to find more detailed information for schedules, timings, specific orders, contact info, directions or client request all in this field.
This application was succesful at notifying the approrioate parties that a change to an event was made and highlighted for them the change.

Eventually this program was depreacated when EventPath was retired.


How it works.
Eventupdate, when run, fetches all events in a select date range from the EventPath database. 
	Returned events are then processed as follows:
		- If an event does not exists in the database, create a new record and check-in the initial note.
		- If an event does exist, hash the note field and diff it against existing the last revision for the event.
			- If a difference is found, create a new revision record and notify staff about change.


Application Urls

/revision
Main Menu for web app

/revision/digest
Summary page of all revisions made on a current day.

/revision/search
Search for events or specific revisions.

/revision/{year}/{month}/{day}
View revisions made on a given date.

/revision/event/{event_id}/
View all revisions made for a select event.

/admin
Django Admin interface.

Application settings

REVISIONS_DATE_DELTA       = 3
How many weeks to search into the future. Default 3 weeks.

REVISIONS_EVENTDATE_FMT    = "%Y%m%d"
Date format for EventPath db.

REVISIONS_EVENT_QUERY      = "SELECT * FROM Events WHERE EventStartDate > '{start_date:%Y%m%d}' AND EventStartDate < '{end_date:%Y%m%d}'"
Query to check Event Notes.

REVISIONS_DBISAM_UTILITY   = os.path.abspath('../bin/dbisam_utility/dbisam_utility.exe')
Path to dbisam utility.

REVISIONS_EMAIL_SENDER     = ""
From email address


REVISIONS_EMAIL_RECIPIENTS = [

]
List of email recipients to receive updates, this can also be managed in the admin application.
 
REVISIONS_UPDATE_INTERVAL = 3
Defines how many times a date the schedule tasked should run, if using the setup_schedule managment command.