from check_handshake_json import checkJsonFile
import json

# Dictionary for testing
# data = {
#     "group_name": "Data Dogs",
#     "classification": "testing",
#     "sources": [
#         {
#             "metrics": [
#                 {
#                     "asc": False,
#                     "data_type": "integer",
#                     "name": "WeueKSwmjcGsYVThpwuf",
#                     "units": "students",
#                 }
#             ],
#             "name": "Spedometer",
#         }
#     ],
# }

with open("sample.json") as f:
    data = json.load(f)


def test_verifyRequired():
    pass


def test_optionalFields():
    pass


def test_requiredFields():
    pass
