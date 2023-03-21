# Mountain peaks

![mountain peaks](https://github.com/flavien-hugs/mountain-pics/blob/main/screenshort.png "screenshot description")


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


## Prerequisites
Clone or pull from the dev branch before you begin coding.
```
#cloning
git clone git@github.com:flavien-hugs/mountain-pics.git .

```

## Environment variable and secrets
Create a .env file from .env.template
    ```
    #
    Unix and MacOS
    cd mountain-pics && cp .flaskenv.template .flaskenv
    ```

## Fire up Docker:
> Note: You will need to make sure Docker is running on your machine!

Use the following command to build the docker images:
```
make build
```

### Finished
You should now be up and running!

* The web app is running on  http://localhost:5000/map/
* The api docs is running on  http://localhost:5000/api/
