# Contagious
An app to emulate the spread of airborne pathogens among a small
group of users.  The primary audience is intended to be businesses
and schools.

Contagious will use LE Bluetooth to detect other users of the app
who are nearby.  Once Contagious detects a period of contact,
it sends the information to a Django backend.  Additionally, Contagious
polls data from the backend and displays some minimal statistics
for the user.
