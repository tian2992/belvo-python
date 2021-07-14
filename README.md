<h1 align="center">Belvo Python SDK</h1>
<p align="center">
    <a href="https://pypi.org/project/belvo-python/"><img alt="PyPI" src="https://img.shields.io/pypi/v/belvo-python?style=for-the-badge"></a>
    <a href="https://pypistats.org/packages/belvo-python"><img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dm/belvo-python?style=for-the-badge"></a>
    <a href="https://travis-ci.com/belvo-finance/belvo-python"><img alt="Travis (.com)" src="https://img.shields.io/travis/com/belvo-finance/belvo-python/master?style=for-the-badge"></a>
    <a href="https://coveralls.io/github/belvo-finance/belvo-python"><img alt="Coveralls github" src="https://img.shields.io/coveralls/github/belvo-finance/belvo-python?style=for-the-badge"></a>
    <a href="https://github.com/psf/black"><img alt="Coveralls github" src="https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge"></a>
</p>

## 📕 Documentation
How to use `belvo-python`: https://belvo-finance.github.io/belvo-python/

If you want to check the full documentation about Belvo API: https://docs.belvo.com

Or if you want to more information about:
* [Getting Belvo API keys](https://developers.belvo.com/docs/get-your-belvo-api-keys)
* [Using Connect Widget](https://developers.belvo.com/docs/connect-widget)
* [Testing in sandbox](https://developers.belvo.com/docs/test-in-sandbox)
* [Using webhooks and recurrent links](https://developers.belvo.com/docs/webhooks)


## 📋 Requirements
* Python 3.6+

## 🚀 Getting started

Install using `pip`:
```
$ pip install belvo-python
```

## Usage (create link via widget)

When your user successfully links their account using the [Connect Widget](https://developers.belvo.com/docs/connect-widget), your implemented callback funciton will return the `link_id` required to make further API to retrieve information.

```python

from pprint import pprint

from belvo.client import Client
from belvo.enums import AccessMode

# Login to Belvo API
client = Client("your-secret-key-id", "your-secret-key", "sandbox")

# Get the link_id from the result of your widget callback function
link_id = result_from_callback_function.id

# Get all accounts
client.Accounts.create(link=link_id)

# Pretty print all checking accounts
for account in client.Accounts.list(type="checking"):
    pprint(account)
```


## Usage (create link via SDK)

You can also manually create the link using the SDK. However, for security purposes, we highly recommend, that you use the [Connect Widget](https://developers.belvo.com/docs/connect-widget) to create the link and follow the **Usage (create link via widget)** example.


```python

from pprint import pprint

from belvo.client import Client
from belvo.enums import AccessMode

# Login to Belvo API
client = Client("your-secret-key-id", "your-secret-key", "sandbox")

# Register a link 
link = client.Links.create(
    institution="banamex",
    username="johndoe",
    password="supersecret",
    access_mode=AccessMode.SINGLE
)

# Get all accounts
client.Accounts.create(link=link["id"])

# Pretty print all checking accounts
for account in client.Accounts.list(type="checking"):
    pprint(account)
```

## Errors and exceptions

By default, when you use our SDK, we automatically return the [error](https://developers.belvo.com/docs/integration-overview#error-handling). However, if you prefer to receive the exception, you need to set the `raise_exception` optional parameter to `True`.



```python
from pprint import pprint
from belvo.client import Client
from belvo.enums import AccessMode
from belvo.exceptions import RequestError

# Login to Belvo API
client = Client("my-secret-key-id", "my-secret-key", "sandbox")

try:
    # Register a link
    link = client.Links.create(
        access_mode=AccessMode.SINGLE,
        institution="banamex_mx_retail",
        username="<username>",
        password="<pass>",
        raise_exception=True, # Set this optional paramter
    )
except RequestError as e:
    # do something with the error
    pprint(e)
else:
    # do something with the link
    pprint(link)

```

## 🐍 Development

To release a new version of the SDK to PyPI:
- Use `make new-version major|minor|patch` to bump a new version.
- Create a new pull request for the new version.
- Once the new version is merged in `master`, create a `tag` matching the new version.

## 👥 Contributing
**Anyone** can do something to make `belvo-python` better, so contributors are always welcome!
If you wish to submit a pull request, please be sure check the items on this list:
- [ ] Tests related to the changed code were executed
- [ ] The source code has been coded following the OWASP security best practices (https://owasp.org/www-pdf-archive/OWASP_SCP_Quick_Reference_Guide_v2.pdf).
- [ ] Commit message properly labeled
- [ ] There is a ticket associated to each PR. 

For more details about contributing to this project, please take a look to our [guidelines](CONTRIBUTING.md). 
