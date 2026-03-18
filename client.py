import requests
import json


# Register
# response = requests.post(
#     "http://localhost:8000/register/", json={"username": "test", "email": "cheche@example.com", "password": "testpass123"}
# )

# Login
response = requests.post(
    "http://localhost:8000/login/",
    json={
        "username": "cheche",
        "email": "checheomenife@gmail.com",
        "password": "cheche199200",
    },
)
print(response.json())

# response = requests.post(
#     "http://localhost:8000/login/", json={"username": "tester", "email": "johndoe@gmail.com", "password": "john199600"}
# )
# print(response.json())

# # Token Refresh
# response = requests.post(
#     "http://localhost:8000/token/refresh/", json={"refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc2MjQwNzQ1OSwiaWF0IjoxNzYyMzIxMDU5LCJqdGkiOiIzOWQ2MTM4N2ZiZDM0MGM5YTkwMzk5N2U1NzkwMjhhOCIsInVzZXJfaWQiOiIxIn0.qhL8DZ0cfUqiup9JlmSNaZukNXYZ9BY68XCQFkZ8hmY"}
# )
# print(response.json())

# Get User
# response = requests.get(
#     "http://localhost:8000/user/", headers={"Authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzYyMzIxNTAwLCJpYXQiOjE3NjIzMjEyMDAsImp0aSI6ImM1ZmU5Y2NkZDllMDQwYWQ5ZDllYjQwOTViNmM3YjIyIiwidXNlcl9pZCI6IjEifQ.PoA6jBiuEwvv52Lot4l2MfNyaIOkgkkAZJuDk_cFze4"}
# )
# print(response.json())
