# sun_and_tides
Code to generate ical calendar file with sunrise/sunset and tidal information

Quite rough around the edges, just edit the timespan and latitude/longitude in the source file, and it will generate an ical file with events for sunrise, sunset, low tide and high tide for this period and location. The description for the sunrise event will also contain information on dusk and dawn. 

Note that when importing ical files into google calendar, google seems to choke on the number of events generated for an entire year, but I have been successful in importing one month at a time.
