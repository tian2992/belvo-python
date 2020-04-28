# Sessions

## Connecting to Belvo API

In order to use Belvo API, you will have to login into a new session by using
a _secret key_.

Secret keys are generated from the Belvo API dashboard. For more information, please visit 
[our Developers portal](https://developers.belvo.co/docs/get-your-belvo-api-keys)

### Method

```python
def __init__(secret_key_id: str, secret_key_password: str, url: str = None) -> None:
    ...
```

You **must** provide `secret_key_id` and `secret_key_password`. 

The `url` tells the client to which Belvo API host should attempt to connect, 
this allows you to switch from a sandbox to a production environment.

You can also set which Belvo API host to use, by setting the `BELVO_API_URL`
environment variable.

When creating a new instance of `Client`, it will automatically perform a login
and create a `JWTSession` (if the credentials are valid).
 

### Example
```python
# Creating a client instance to connect to Belvo API
from belvo.client import Client

my_client = Client(
    "your-secret-key-id", 
    "your-secret-key-password", 
    "https://api.belvo.co"
)


# Creating a client that takes url from the environment.
# We assume that you have set BELVO_API_URL before 
# (e.g. export BELVO_API_URL=https://sandbox.belvo.co
my_client = Client(
    "your-secret-key-id", 
    "your-secret-key-password"
)
```

## Nested resources

All resources in the Belvo API are nested attributes in your client instance,
these resources are available **only** if you provide valid credentials.


### Available resources
* Institutions
* Links
* Accounts
* Transactions
* Owners
* Invoices
* TaxReturns
* TaxStatus
* Statements