To run the Server, Install Docker on the system

Run `docker compose up`
This will launch the Python Fast API server localhost:8000.

We are mounting the /var/log folder to the container.

To check the swagger doc we can use localhost:8000/docs

There are 2 APIs

1. api/v1/files  --> This fetches all the file names from the logs directory. We can add a search query param for substring matching of file name
2. api/v1/logs --> This fetches the last entries (query param) lines from the Log File. We can add a search query param for substring matching of log line




To run the Tests of the EndPoints, 

We can install the requirements using `pip install -r requirements.txt`
Run `pytest tests/`

