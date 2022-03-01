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

# response = post(f"{protocol}://{host}:{port}/api/{version}/{token}/addTracker", data={"name": "Temperature"}).json()
# print(response)
