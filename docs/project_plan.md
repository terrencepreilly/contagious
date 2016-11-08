# Project Plan

## time slot
Since I'm working by myself, a time slot won't be too difficult.
I plan on working on the project on Sunday mornings.

## list of features
  - There should be a backend API with the following features:
    - The ability to post a "contact" (when two phones are near
      one another)
    - The ability to get a list of contacts.
    - The ability to create a new user or group.
    - The ability to authenticate the user
    - The ability to add a user to a group
    - The ability to return statistics on users or groups
  - The phone app itself should have the following features:
    - The ability to determine if another phone running the app
      is nearby (using LE bluetooth)
    - The ability to display statistics for a particular
      user or the user's groups
    - The ability to send data to the backend

## work plan
The app and backend can function independently of one another,
so I can mock data pretty easily, and develop features in a
non-linear fashion.  I plan on completing the most difficult
features first: user authentication and connecting through
LE bluetooth.  Once those are down, I would like to work on
connecting the phone app and the backend.  Then, I would like
to add the statistics calculations and displays.  Finally,
I would like to add groups (since groups will have many of
the same features as individual users -- they could be dropped
if there are time constraints.)  The last thing I plan on
doing will be to figure out deployment. (It shouldn't be too
bad, since I'll be developing with Docker.)

## documentation plan
I'm going to have pretty traditional documentation for open
source apps: a README.md, documentation in the form of unit
tests (for the backend, anyway), and maybe a short writeup
for the phone app itself.  I'll probably write all of this in
markdown, and use pandoc to convert to PDF or HTML on a whim.
