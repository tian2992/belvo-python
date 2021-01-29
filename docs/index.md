# Introduction

Bank connectivity simplified.

Belvo's Python SDK enables you to make use of Belvo API to connect to all major 
banks in Mexico.
---

## Quickstart
Requirements: Python 3.6+

Install using `pip`:
```
$ pip install belvo-python
```
---

## Example
```python

from pprint import pprint

from belvo.client import Client

# Login to Belvo API
client = Client("my-secret-key-id", "my-secret-key", "https://api.belvo.com")

# Register a link 
link = client.Links.create(
    institution="banamex",
    username="johndoe",
    password="supersecret"
)

# Get all accounts
client.Accounts.create(link["id"])

# Pretty print all checking accounts
for account in client.Accounts.list(type="checking"):
    pprint(account)
```