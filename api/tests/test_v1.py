from requests import get
from requests import post
from requests import delete


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

# response = get(f"{protocol}://{host}:{port}/api/{version}/checkToken").json()
# print(response)

# response = get(f"{protocol}://{host}:{port}/api/{version}/checkToken", headers={"APIToken": "xyz"}).json()
# print(response)

# response = get(f"{protocol}://{host}:{port}/api/{version}/checkToken", headers={"APIToken": token}).json()
# print(response)


# getTrackerTypes
# ===============
# print("getTrackerTypes")

# response = get(f"{protocol}://{host}:{port}/api/{version}/getTrackerTypes").json()
# print(response)

# response = get(f"{protocol}://{host}:{port}/api/{version}/getTrackerTypes", headers={"APIToken": "xyz"}).json()
# print(response)

# response = get(f"{protocol}://{host}:{port}/api/{version}/getTrackerTypes", headers={"APIToken": token}).json()
# print(response)


# getTrackers
# ===========
# print("getTrackers")

# response = get(f"{protocol}://{host}:{port}/api/{version}/getTrackers").json()
# print(response)

# response = get(f"{protocol}://{host}:{port}/api/{version}/getTrackers", headers={"APIToken": "xyz"}).json()
# print(response)

# response = get(f"{protocol}://{host}:{port}/api/{version}/getTrackers", headers={"APIToken": token}).json()
# print(response)


# getLogs
# =======
# print("getLogs")

# response = get(f"{protocol}://{host}:{port}/api/{version}/getLogs/xyz").json()
# print(response)

# response = get(f"{protocol}://{host}:{port}/api/{version}/getLogs/xyz", headers={"APIToken": "xyz"}).json()
# print(response)

# response = get(f"{protocol}://{host}:{port}/api/{version}/getLogs/xyz", headers={"APIToken": token}).json()
# print(response)

# response = get(f"{protocol}://{host}:{port}/api/{version}/getLogs/100", headers={"APIToken": token}).json()
# print(response)

# response = get(f"{protocol}://{host}:{port}/api/{version}/getLogs/1", headers={"APIToken": token}).json()
# print(response)


# getStats
# ========
# print("getStats")

# response = get(f"{protocol}://{host}:{port}/api/{version}/getStats/xyz").json()
# print(response)

# response = get(f"{protocol}://{host}:{port}/api/{version}/getStats/xyz", headers={"APIToken": "xyz"}).json()
# print(response)

# response = get(f"{protocol}://{host}:{port}/api/{version}/getStats/xyz", headers={"APIToken": token}).json()
# print(response)

# response = get(f"{protocol}://{host}:{port}/api/{version}/getStats/100", headers={"APIToken": token}).json()
# print(response)

# response = get(f"{protocol}://{host}:{port}/api/{version}/getStats/1", headers={"APIToken": token}).json()
# print(response)

# response = get(f"{protocol}://{host}:{port}/api/{version}/getStats/2", headers={"APIToken": token}).json()
# print(response)

# response = get(f"{protocol}://{host}:{port}/api/{version}/getStats/3", headers={"APIToken": token}).json()
# print(response)

# response = get(f"{protocol}://{host}:{port}/api/{version}/getStats/4", headers={"APIToken": token}).json()
# print(response)

# response = get(f"{protocol}://{host}:{port}/api/{version}/getStats/5", headers={"APIToken": token}).json()
# print(response)

# response = get(f"{protocol}://{host}:{port}/api/{version}/getStats/6", headers={"APIToken": token}).json()
# print(response)


# addTracker
# ==========
# print("addTracker")

# response = post(f"{protocol}://{host}:{port}/api/{version}/addTracker").json()
# print(response)

# response = post(f"{protocol}://{host}:{port}/api/{version}/addTracker", headers={"APIToken": "xyz"}).json()
# print(response)

# response = post(f"{protocol}://{host}:{port}/api/{version}/addTracker", data={"tracker_name": ""}, headers={"APIToken": "xyz"}).json()
# print(response)

# response = post(f"{protocol}://{host}:{port}/api/{version}/addTracker", data={"tracker_name": "", "tracker_type_id": ""}, headers={"APIToken": "xyz"}).json()
# print(response)

# response = post(f"{protocol}://{host}:{port}/api/{version}/addTracker", data={"tracker_name": "", "tracker_type_id": ""}, headers={"APIToken": token}).json()
# print(response)

# response = post(f"{protocol}://{host}:{port}/api/{version}/addTracker", data={"tracker_name": "Temperature", "tracker_description": "x"*257, "tracker_type_id": ""}, headers={"APIToken": token}).json()
# print(response)

# response = post(f"{protocol}://{host}:{port}/api/{version}/addTracker", data={"tracker_name": "Temperature", "tracker_description": "My Personal Temperature Tracker", "tracker_type_id": ""}, headers={"APIToken": token}).json()
# print(response)

# response = post(f"{protocol}://{host}:{port}/api/{version}/addTracker", data={"tracker_name": "Temperature", "tracker_description": "My Personal Temperature Tracker", "tracker_type_id": "xyz"}, headers={"APIToken": token}).json()
# print(response)

# response = post(f"{protocol}://{host}:{port}/api/{version}/addTracker", data={"tracker_name": "Temperature", "tracker_description": "My Personal Temperature Tracker", "tracker_type_id": "100"}, headers={"APIToken": token}).json()
# print(response)

# Boolean
# response = post(f"{protocol}://{host}:{port}/api/{version}/addTracker", data={"tracker_name": "Temperature", "tracker_description": "My Personal Temperature Tracker", "tracker_type_id": "1"}, headers={"APIToken": token}).json()
# print(response)

# Integer/Decimal
# response = post(f"{protocol}://{host}:{port}/api/{version}/addTracker", data={"tracker_name": "Temperature", "tracker_description": "My Personal Temperature Tracker", "tracker_type_id": "2"}, headers={"APIToken": token}).json()
# print(response)

# response = post(f"{protocol}://{host}:{port}/api/{version}/addTracker", data={"tracker_name": "Temperature", "tracker_description": "My Personal Temperature Tracker", "tracker_type_id": "2", "tracker_unit": ""}, headers={"APIToken": token}).json()
# print(response)

# response = post(f"{protocol}://{host}:{port}/api/{version}/addTracker", data={"tracker_name": "Temperature", "tracker_description": "My Personal Temperature Tracker", "tracker_type_id": "2", "tracker_unit": "C"}, headers={"APIToken": token}).json()
# print(response)

# Duration
# response = post(f"{protocol}://{host}:{port}/api/{version}/addTracker", data={"tracker_name": "Temperature", "tracker_description": "My Personal Temperature Tracker", "tracker_type_id": "4"}, headers={"APIToken": token}).json()
# print(response)

# Single Select/Multi Select
# response = post(f"{protocol}://{host}:{port}/api/{version}/addTracker", data={"tracker_name": "Temperature", "tracker_description": "My Personal Temperature Tracker", "tracker_type_id": "5"}, headers={"APIToken": token}).json()
# print(response)

# response = post(f"{protocol}://{host}:{port}/api/{version}/addTracker", data={"tracker_name": "Temperature", "tracker_description": "My Personal Temperature Tracker", "tracker_type_id": "5", "tracker_options": ""}, headers={"APIToken": token}).json()
# print(response)

# response = post(f"{protocol}://{host}:{port}/api/{version}/addTracker", data={"tracker_name": "Temperature", "tracker_description": "My Personal Temperature Tracker", "tracker_type_id": "5", "tracker_options": "xyz"}, headers={"APIToken": token}).json()
# print(response)

# response = post(f"{protocol}://{host}:{port}/api/{version}/addTracker", data={"tracker_name": "Temperature", "tracker_description": "My Personal Temperature Tracker", "tracker_type_id": "5", "tracker_options": []}, headers={"APIToken": token}).json()
# print(response)

# response = post(f"{protocol}://{host}:{port}/api/{version}/addTracker", data={"tracker_name": "Temperature", "tracker_description": "My Personal Temperature Tracker", "tracker_type_id": "5", "tracker_options": ["abc"]}, headers={"APIToken": token}).json()
# print(response)

# response = post(f"{protocol}://{host}:{port}/api/{version}/addTracker", data={"tracker_name": "Temperature", "tracker_description": "My Personal Temperature Tracker", "tracker_type_id": "5", "tracker_options": ["abc", "def", 123]}, headers={"APIToken": token}).json()
# print(response)

# response = post(f"{protocol}://{host}:{port}/api/{version}/addTracker", data={"tracker_name": "Temperature", "tracker_description": "My Personal Temperature Tracker", "tracker_type_id": "5", "tracker_options": ["abc", "", "def"]}, headers={"APIToken": token}).json()
# print(response)

# response = post(f"{protocol}://{host}:{port}/api/{version}/addTracker", data={"tracker_name": "Temperature", "tracker_description": "My Personal Temperature Tracker", "tracker_type_id": "6", "tracker_options": ["Option 1", "Option 2", "Option 3", "Option 4"]}, headers={"APIToken": token}).json()
# print(response)


# addLog
# ======
# print("addLog")

# response = post(f"{protocol}://{host}:{port}/api/{version}/addLog/xyz").json()
# print(response)

# response = post(f"{protocol}://{host}:{port}/api/{version}/addLog/xyz", headers={"APIToken": "xyz"}).json()
# print(response)

# response = post(f"{protocol}://{host}:{port}/api/{version}/addLog/xyz", data={"log_time": ""}, headers={"APIToken": "xyz"}).json()
# print(response)

# response = post(f"{protocol}://{host}:{port}/api/{version}/addLog/xyz", data={"log_time": "", "log_value": ""}, headers={"APIToken": "xyz"}).json()
# print(response)

# response = post(f"{protocol}://{host}:{port}/api/{version}/addLog/xyz", data={"log_time": "", "log_value": ""}, headers={"APIToken": token}).json()
# print(response)

# response = post(f"{protocol}://{host}:{port}/api/{version}/addLog/1", data={"log_time": "", "log_value": ""}, headers={"APIToken": token}).json()
# print(response)

# response = post(f"{protocol}://{host}:{port}/api/{version}/addLog/1", data={"log_time": "2022-03-04 02:05", "log_value": ""}, headers={"APIToken": token}).json()
# print(response)

# Boolean
# response = post(f"{protocol}://{host}:{port}/api/{version}/addLog/1", data={"log_time": "2022-03-04 02:05", "log_value": "xyz"}, headers={"APIToken": token}).json()
# print(response)

# response = post(f"{protocol}://{host}:{port}/api/{version}/addLog/1", data={"log_time": "2022-03-04 02:05", "log_value": "No"}, headers={"APIToken": token}).json()
# print(response)

# response = post(f"{protocol}://{host}:{port}/api/{version}/addLog/1", data={"log_time": "2022-03-04 02:05", "log_note": "Sample Log Note", "log_value": "Yes"}, headers={"APIToken": token}).json()
# print(response)

# Integer
# response = post(f"{protocol}://{host}:{port}/api/{version}/addLog/2", data={"log_time": "2022-03-04 02:05", "log_value": "xyz"}, headers={"APIToken": token}).json()
# print(response)

# response = post(f"{protocol}://{host}:{port}/api/{version}/addLog/2", data={"log_time": "2022-03-04 02:05", "log_value": 1.0}, headers={"APIToken": token}).json()
# print(response)

# response = post(f"{protocol}://{host}:{port}/api/{version}/addLog/2", data={"log_time": "2022-03-04 02:05", "log_note": "Sample Log Note", "log_value": "2"}, headers={"APIToken": token}).json()
# print(response)

# Decimal
# response = post(f"{protocol}://{host}:{port}/api/{version}/addLog/3", data={"log_time": "2022-03-04 02:05", "log_value": "xyz"}, headers={"APIToken": token}).json()
# print(response)

# response = post(f"{protocol}://{host}:{port}/api/{version}/addLog/3", data={"log_time": "2022-03-04 02:05", "log_value": 1.56}, headers={"APIToken": token}).json()
# print(response)

# response = post(f"{protocol}://{host}:{port}/api/{version}/addLog/3", data={"log_time": "2022-03-04 02:05", "log_note": "Sample Log Note", "log_value": "1.567"}, headers={"APIToken": token}).json()
# print(response)

# Duration
# response = post(f"{protocol}://{host}:{port}/api/{version}/addLog/4", data={"log_time": "2022-03-04 02:05", "log_value": "xyz"}, headers={"APIToken": token}).json()
# print(response)

# response = post(f"{protocol}://{host}:{port}/api/{version}/addLog/4", data={"log_time": "2022-03-04 02:05", "log_value": 1000000}, headers={"APIToken": token}).json()
# print(response)

# response = post(f"{protocol}://{host}:{port}/api/{version}/addLog/4", data={"log_time": "2022-03-04 02:05", "log_note": "Sample Log Note", "log_value": 3723}, headers={"APIToken": token}).json()
# print(response)

# response = post(f"{protocol}://{host}:{port}/api/{version}/addLog/4", data={"log_time": "2022-03-04 02:05", "log_note": "Sample Log Note", "log_value": "120"}, headers={"APIToken": token}).json()
# print(response)

# Single Select
# response = post(f"{protocol}://{host}:{port}/api/{version}/addLog/5", data={"log_time": "2022-03-04 02:05", "log_value": "xyz"}, headers={"APIToken": token}).json()
# print(response)

# response = post(f"{protocol}://{host}:{port}/api/{version}/addLog/5", data={"log_time": "2022-03-04 02:05", "log_value": "100"}, headers={"APIToken": token}).json()
# print(response)

# response = post(f"{protocol}://{host}:{port}/api/{version}/addLog/5", data={"log_time": "2022-03-04 02:05", "log_value": 1}, headers={"APIToken": token}).json()
# print(response)

# response = post(f"{protocol}://{host}:{port}/api/{version}/addLog/5", data={"log_time": "2022-03-04 02:05", "log_note": "Sample Log Note", "log_value": "2"}, headers={"APIToken": token}).json()
# print(response)

# Multi Select
# response = post(f"{protocol}://{host}:{port}/api/{version}/addLog/6", data={"log_time": "2022-03-04 02:05", "log_value": "xyz"}, headers={"APIToken": token}).json()
# print(response)

# response = post(f"{protocol}://{host}:{port}/api/{version}/addLog/6", data={"log_time": "2022-03-04 02:05", "log_value": "100"}, headers={"APIToken": token}).json()
# print(response)

# response = post(f"{protocol}://{host}:{port}/api/{version}/addLog/6", data={"log_time": "2022-03-04 02:05", "log_value": ["100"]}, headers={"APIToken": token}).json()
# print(response)

# response = post(f"{protocol}://{host}:{port}/api/{version}/addLog/6", data={"log_time": "2022-03-04 02:05", "log_value": 4}, headers={"APIToken": token}).json()
# print(response)

# response = post(f"{protocol}://{host}:{port}/api/{version}/addLog/6", data={"log_time": "2022-03-04 02:05", "log_note": "Sample Log Note", "log_value": [5]}, headers={"APIToken": token}).json()
# print(response)

# response = post(f"{protocol}://{host}:{port}/api/{version}/addLog/6", data={"log_time": "2022-03-04 02:05", "log_note": "Sample Log Note", "log_value": ["4", "", 6, "7", "xyz"]}, headers={"APIToken": token}).json()
# print(response)


# deleteTracker
# =============
# print("deleteTracker")

# response = delete(f"{protocol}://{host}:{port}/api/{version}/deleteTracker/xyz").json()
# print(response)

# response = delete(f"{protocol}://{host}:{port}/api/{version}/deleteTracker/xyz", headers={"APIToken": "xyz"}).json()
# print(response)

# response = delete(f"{protocol}://{host}:{port}/api/{version}/deleteTracker/xyz", headers={"APIToken": token}).json()
# print(response)

# response = delete(f"{protocol}://{host}:{port}/api/{version}/deleteTracker/11", headers={"APIToken": token}).json()
# print(response)


# deleteLog
# =========
# print("deleteLog")

# response = delete(f"{protocol}://{host}:{port}/api/{version}/deleteLog/xyz/xyz").json()
# print(response)

# response = delete(f"{protocol}://{host}:{port}/api/{version}/deleteLog/xyz/xyz", headers={"APIToken": "xyz"}).json()
# print(response)

# response = delete(f"{protocol}://{host}:{port}/api/{version}/deleteLog/xyz/xyz", headers={"APIToken": token}).json()
# print(response)

# response = delete(f"{protocol}://{host}:{port}/api/{version}/deleteLog/11/xyz", headers={"APIToken": token}).json()
# print(response)

# response = delete(f"{protocol}://{host}:{port}/api/{version}/deleteLog/11/46", headers={"APIToken": token}).json()
# print(response)
