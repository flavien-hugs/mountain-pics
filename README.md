The context of this test is to provide a simple web service for storing and retrieving mountain peaks.

Using the python web framework of your choosing and a database (prefer postgres solution) and implement the following features:

- models/db tables for storing a peak location and attribute: lat, lon, altitude, name
- REST api endpoints to :
    * create/read/update/delete a peak
    * retrieve a list of peaks in a given geographical bounding box
- add an api/docs url to allow viewing the documentation of the api and send requests on endpoints
- deploy all this stack using docker and docker-compose
- [Optional] add ip filtering with a country whitelist settings. Connections from a country not in the list should return a http 403. An admin page protected
with user/password authentication should allow viewing rejected connections.
- [Optional] add an an html page to view the peaks on a map (use open source packages)
