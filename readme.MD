### Fetch Points API 
This is a Flask REST API for tracking points from different payers and spending. The API allows adding points, spending points, and retrieving the current point balance.

# Requirements
Make sure you have Python 3 installed. This API uses Flask and other dependencies that can be installed via a requirements.txt file.

# Setup
Clone this repository and go into the project directory.
Create a virtual environment to manage the dependencies:

Type the follow command to create a virtual environment:

`python3 -m venv .venv`

Activate the virtual environment w/ following commands:

source .venv/bin/activate

To install all required dependencies, run:

`pip install -r requirements.txt`

To run the application now, type:

`python3 app.py`

The server will run on port 8000 on http://127.0.0.1:8000.

## The API Endpoints

1. Add Points
This endpoint adds points to a payer's account.

Route: /add
Method: POST

```bash
{
  "payer": "DANNON",
  "points": 300,
  "timestamp": "2022-10-31T10:00:00Z"
}
```
you can use cURL for testing the API endpoints and seeing the responses.

```bash
curl -X POST -H "Content-Type: application/json" \
-d '{"payer": "DANNON", "points": 300, "timestamp": "2022-10-31T10:00:00Z"}' \
http://127.0.0.1:8000/add
```
```bash
curl -X POST -H "Content-Type: application/json" \
-d '{"payer": "UNILEVER", "points": 200, "timestamp": "2022-10-31T11:00:00Z"}' \
http://127.0.0.1:8000/add
```
```bash
curl -X POST -H "Content-Type: application/json" \
-d '{"payer": "DANNON", "points": -200, "timestamp": "2022-10-31T15:00:00Z"}' \
http://127.0.0.1:8000/add
```
```bash
curl -X POST -H "Content-Type: application/json" \
-d '{"payer": "MILLER COORS", "points": 10000, "timestamp": "2022-11-01T14:00:00Z"}' \
http://127.0.0.1:8000/add
```
```bash
curl -X POST -H "Content-Type: application/json" \
-d '{"payer": "DANNON", "points": 1000, "timestamp": "2022-11-02T14:00:00Z"}' \
http://127.0.0.1:8000/add
```
2. Spend Points
This endpoint spends points from the user's account according to the criteria in the guidelines pdf. 
If a request was made to spend more points than what a user has in total, then it will return a status code of 400 and a message saying the user doesn’t have enough points. Else, the endpoint will respond with a status code of 200 and a list of payer names and the number of points that were subtracted.

Route: /spend
Method: POST

Below is an example req body.
```Bash
{
  "points": 5000
}
```
Below is an example cURL command for testing this endpoint.
```Bash
curl -X POST -H "Content-Type: application/json" \
-d '{"points": 5000}' \
http://127.0.0.1:8000/spend
```

Here is an example response:
```Bash
[
{ "payer": "DANNON", "points": -100 },
{ "payer": "UNILEVER", "points": -200 },
{ "payer": "MILLER COORS", "points": -4,700 }
]
```
3. Get Balance
This endpoint retrieves the current balance for all payers.

Route: /balance
Method: GET
```Bash
curl -X GET http://127.0.0.1:8000/balance
```
Example Response:
```Bash
{
  "DANNON": 1000,
  "UNILEVER": 0,
  "MILLER COORS": 5300
}
```

