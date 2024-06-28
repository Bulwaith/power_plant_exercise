# Simple Python App for Energy Plants Map Backend
Simple Flask app, which provides the backend functionalities for the Energy Plant Map Frontend.

**Assumptions**
- Plants tab is the PLNT22. Probably other info are stored in the file, but I'll keep it simple and load only that tab.
- Every plant has a unique ID, which is the column `Plant file sequence number`, translated as `plant_id`.


**Notes**: 
- The app runs through gunicorn, an easy way to reload the app if any code change, to speed up the development.
- The chosen DB is the `SQLite 3` for simplicity of this exercise. It will be completeley regenerated on each run, unless the application runs on a specific exernal volume. The module/class responsible for the DB interaction could be easily swapped with another technology/DB, keeping the same interface.
- Still for simplicity and readability reasons, the code does not contain many optmizations, sanity checks and comprehensive error detection.


## Application workflow
To start the application, [Docker Desktop]("https://www.docker.com/products/docker-desktop/") is required.
The application will run throuh the `Makefile` commands:
1) Build
```
make build
```
which will call the `docker-compose -f docker/docker-compose.yml build`

2) Start
```
make start
```
which will call the `docker-compose -f docker/docker-compose.yml up -d`

3) Stop
```
make stop
```
which will call the `docker-compose -f docker/docker-compose.yml down`


### This goes through few steps:

### 1) Docker build
An image will be built, starting from the official `Python:3.11` image, the code is copied in the image and few basic libraries are installed.
At the end of the building process, the command to run the app with Python is defined and the port `8000` is defined as listening port.

### 2) App initialization
As soon as the app starts, the app does some initializing process:
- a `SQLite3` DB is initialized. Main table is created;
- a default/provided `XLSX file` gets loaded via pandas and the specific tab extracted;
- the data available in the file get then read, cleaned and stored into the DB;
- the API service starts listening.

### 3) API endpoints
We will be using the local address, provided by the endpoint automatically.

1) GET Plants in the State
```
/get-plants/<state>
Eg: http://localhost:8000/get-plants/CA
```
This will call all the plants (and their info) having that state

2) GET Plants in the area (longitude, latitude and radius)
```
/get-plants-in-area?latitude=<latitude>&longitude=<longitude>&radius=<radius>
Eg: http://localhost:8000/get-plants-in-area?latitude=32&longitude=-111&radius=2
```
I guessed that a list of plants could be returned if the user is browsing a portion of the map.

3) Get a specific plant, identified by its ID
```
/get-plant/<plant_id>
Eg: http://localhost:8000/get-plant/300
```


### TESTS
Pytest could be called before running the app, to run unit test and integration tests.
For time constraints, this is not available in this version. 🥲
