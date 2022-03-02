from requests import get
from requests import post


protocol = "http"
host = "localhost"
port = 8000
version = "v1"
token = "45801bbd4697e784878a6f06387583c918578ff827240569cb62be9b0ad9902a"


# test
# ====
# print("test")

# response = get(f"{protocol}://{host}:{port}/api/{version}/test").json()
# print(response)


# checkToken
# ==========
# print("checkToken")

# response = get(f"{protocol}://{host}:{port}/api/{version}/xyz/checkToken").json()
# print(response)

# response = get(f"{protocol}://{host}:{port}/api/{version}/{token}/checkToken").json()
# print(response)


# getTrackerTypes
# ===============
# print("getTrackerTypes")

# response = get(f"{protocol}://{host}:{port}/api/{version}/xyz/getTrackerTypes").json()
# print(response)

# response = get(f"{protocol}://{host}:{port}/api/{version}/{token}/getTrackerTypes").json()
# print(response)


# getTrackers
# ===========
# print("getTrackers")

# response = get(f"{protocol}://{host}:{port}/api/{version}/xyz/getTrackers").json()
# print(response)

# response = get(f"{protocol}://{host}:{port}/api/{version}/{token}/getTrackers").json()
# print(response)


# getTrackerLogs
# ==============
# print("getTrackerLogs")

# response = get(f"{protocol}://{host}:{port}/api/{version}/xyz/getTrackerLogs/xyz").json()
# print(response)

# response = get(f"{protocol}://{host}:{port}/api/{version}/{token}/getTrackerLogs/xyz").json()
# print(response)

# response = get(f"{protocol}://{host}:{port}/api/{version}/{token}/getTrackerLogs/100").json()
# print(response)

# response = get(f"{protocol}://{host}:{port}/api/{version}/{token}/getTrackerLogs/1").json()
# print(response)


# addTracker
# ==========
# print("addTracker")

# response = post(f"{protocol}://{host}:{port}/api/{version}/xyz/addTracker").json()
# print(response)

# response = post(f"{protocol}://{host}:{port}/api/{version}/{token}/addTracker").json()
# print(response)

# response = post(f"{protocol}://{host}:{port}/api/{version}/{token}/addTracker", data={"tracker_name": ""}).json()
# print(response)

# response = post(f"{protocol}://{host}:{port}/api/{version}/{token}/addTracker", data={"tracker_name": "", "tracker_description": ""}).json()
# print(response)

# response = post(f"{protocol}://{host}:{port}/api/{version}/{token}/addTracker", data={"tracker_name": "", "tracker_description": "", "tracker_type_id": ""}).json()
# print(response)

# response = post(f"{protocol}://{host}:{port}/api/{version}/{token}/addTracker", data={"tracker_name": "Temperature", "tracker_description": "x"*257, "tracker_type_id": ""}).json()
# print(response)

# response = post(f"{protocol}://{host}:{port}/api/{version}/{token}/addTracker", data={"tracker_name": "Temperature", "tracker_description": "My Personal Temperature Tracker", "tracker_type_id": ""}).json()
# print(response)

# response = post(f"{protocol}://{host}:{port}/api/{version}/{token}/addTracker", data={"tracker_name": "Temperature", "tracker_description": "My Personal Temperature Tracker", "tracker_type_id": "xyz"}).json()
# print(response)

# response = post(f"{protocol}://{host}:{port}/api/{version}/{token}/addTracker", data={"tracker_name": "Temperature", "tracker_description": "My Personal Temperature Tracker", "tracker_type_id": "100"}).json()
# print(response)

# Boolean
# response = post(f"{protocol}://{host}:{port}/api/{version}/{token}/addTracker", data={"tracker_name": "Temperature", "tracker_description": "My Personal Temperature Tracker", "tracker_type_id": "1"}).json()
# print(response)

# Integer/Decimal
# response = post(f"{protocol}://{host}:{port}/api/{version}/{token}/addTracker", data={"tracker_name": "Temperature", "tracker_description": "My Personal Temperature Tracker", "tracker_type_id": "2"}).json()
# print(response)

# response = post(f"{protocol}://{host}:{port}/api/{version}/{token}/addTracker", data={"tracker_name": "Temperature", "tracker_description": "My Personal Temperature Tracker", "tracker_type_id": "2", "tracker_unit": ""}).json()
# print(response)

# response = post(f"{protocol}://{host}:{port}/api/{version}/{token}/addTracker", data={"tracker_name": "Temperature", "tracker_description": "My Personal Temperature Tracker", "tracker_type_id": "2", "tracker_unit": "C"}).json()
# print(response)

# Duration
# response = post(f"{protocol}://{host}:{port}/api/{version}/{token}/addTracker", data={"tracker_name": "Temperature", "tracker_description": "My Personal Temperature Tracker", "tracker_type_id": "4"}).json()
# print(response)

# Single Select/Multi Select
# response = post(f"{protocol}://{host}:{port}/api/{version}/{token}/addTracker", data={"tracker_name": "Temperature", "tracker_description": "My Personal Temperature Tracker", "tracker_type_id": "5"}).json()
# print(response)

# response = post(f"{protocol}://{host}:{port}/api/{version}/{token}/addTracker", data={"tracker_name": "Temperature", "tracker_description": "My Personal Temperature Tracker", "tracker_type_id": "5", "tracker_options": ""}).json()
# print(response)

# response = post(f"{protocol}://{host}:{port}/api/{version}/{token}/addTracker", data={"tracker_name": "Temperature", "tracker_description": "My Personal Temperature Tracker", "tracker_type_id": "5", "tracker_options": "xyz"}).json()
# print(response)

# response = post(f"{protocol}://{host}:{port}/api/{version}/{token}/addTracker", data={"tracker_name": "Temperature", "tracker_description": "My Personal Temperature Tracker", "tracker_type_id": "5", "tracker_options": []}).json()
# print(response)

# response = post(f"{protocol}://{host}:{port}/api/{version}/{token}/addTracker", data={"tracker_name": "Temperature", "tracker_description": "My Personal Temperature Tracker", "tracker_type_id": "5", "tracker_options": ["abc"]}).json()
# print(response)

# response = post(f"{protocol}://{host}:{port}/api/{version}/{token}/addTracker", data={"tracker_name": "Temperature", "tracker_description": "My Personal Temperature Tracker", "tracker_type_id": "5", "tracker_options": ["abc", "def"]}).json()
# print(response)

# response = post(f"{protocol}://{host}:{port}/api/{version}/{token}/addTracker", data={"tracker_name": "Temperature", "tracker_description": "My Personal Temperature Tracker", "tracker_type_id": "5", "tracker_options": ["abc", "", "def"]}).json()
# print(response)

# response = post(f"{protocol}://{host}:{port}/api/{version}/{token}/addTracker", data={"tracker_name": "Temperature", "tracker_description": "My Personal Temperature Tracker", "tracker_type_id": "6", "tracker_options": ["Option 1", "Option 2", "Option 3", "Option 4"]}).json()
# print(response)
