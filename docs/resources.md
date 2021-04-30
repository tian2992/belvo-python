# Resources
With the Python SDK you will be able to consume the following API resources:

## Institutions
Bank entities that are supported by Belvo API.

### List
Retrieve all bank integrations available.

**Method:**
```python
def list() -> Generator:
    ...
```

**Example:**
```python
# Retrieve all institutions
institutions = client.Institutions.list()

```
**:warning: Warning:**

The `.list()` method yields a `Generator`, you will have to iterate  over it or
cast it to `List` or `Tuple`.


## Links
Links an end-user identity with a bank entity.

### Registering a new Link

To register a `Link` you **must** provide: _institution, username and password_. 
Optionally you can also provide a _token_ (for MFA) and a _secret_ (that will
be used to safely encrypt and decrypt the password).

The `Link` will only be registered if the provided credentials are valid and will
be validated by authenticating against the specified bank.

**Method:** 

```python
def create(
    self,
    institution: str,
    username: str,
    password: str,
    *,
    username2: str = None,
    username3: str = None,
    password2: str = None,
    token: str = None,
    encryption_key: str = None,
    save_data: bool = True,
    raise_exception: bool = False,
    access_mode: AccessMode = None,
    username_type: str = None,
    certificate: str = None,
    private_key: str = None,
) -> Union[List[Dict], Dict]:
    ...
```

**Example:**
```python
# Link that doesn't require a MFA token
link = client.Links.create("banamex", "johndoe", "a-password")

# Link that requires a MFA token
link = client.Links.create("bancomer", "johndoe", "a-password", token="37038919")

# Link with custom encryption key
link = client.Links.create("santander", "johndoe", "a-password", encryption_key="your-secret")

# Creating a recurrent link
from belvo.enums import AccessMode
link = client.Links.create("banamex", "johndoe", "a-password", access_mode=AccessMode.RECURRENT)

# Creating a Link with a username_type
link = client.Links.create("banamex", "johndoe", "a-password", username_type="001")

# Creating a Link with a certificate and private_key
link = client.Links.create("sat_mx_fiscal", "johndoe", "a-password", certificate="/path/to/cert", private_key="/path/to/key")
```

**:warning: Warning:**

Please keep in mind that by using your own `encryption_key` when creating a `Link`, you
will need to send it in **ALL** subsequent requests. 

Belvo API doesn't store passwords in plain text, neither does store custom secrets. 
Keep your custom `encryption_key` safe. Don't lose it.

### Deleting links
A `Link` is persisted into our database when you register it, if you want you can 
delete it at any time and data related to the `Link` will be also deleted.

**Method:**
```python
def delete(link: str) -> bool:
    ...
```

**Example:**
```python
client.Links.delete("b91835f5-6f83-4d9b-a0ad-a5a249f18b7c")

```

**:warning: Warning:**

When deleting a `Link`, all _accounts_, _transactions_ and _owners_ data will be
deleted on cascade.

### List and filtering
In order to make easier to find a `Link` (or many of them), it is possible to 
filter the results.

If not filters are provided, you will get all `Links` that you have registered.

**Method:**
```python
def list(**kwargs) -> Generator:
    ...
```

**Example:**
```python
# Retrieve all links (no filter given)
links = client.Links.list()

# Retrieve links for a specific bank
links = client.Links.list(institution="banorte")

# Retrieve links for a list of banks
links = client.Links.list(institution__in="hsbc,banamex,santander")
```

**:warning: Warning:**

The `.list()` method yields a `Generator`, you will have to iterate  over it or
cast it to `List` or `Tuple`.

### Updating an existing Link

A `Link` is persisted into our database when you register it, if you want you can 
update it with new data, like a password change.

**Method:** 

```python
def update(
    self,
    link: str,
    *,
    password: str = None,
    password2: str = None,
    token: str = None,
    encryption_key: str = None,
    save_data: bool = True,
    raise_exception: bool = False,
    username_type: str = None,
    certificate: str = None,
    private_key: str = None,
) -> Union[List[Dict], Dict]:
```

**Example:**
```python
# Update a Link's password
link = client.Links.update("b91835f5-6f83-4d9b-a0ad-a5a249f18b7c", "a-password")
```

### Requesting link scoped tokens
A link token that contains `access` and `refresh` keys.
This link token is scoped to the link that created it and valid for the actions done with this link only.

**Method:**
```python
def token(link: str, scopes: str) -> Union[List[Dict], Dict]:
    ...
```

**Example:**
```python
link_token = client.Links.token(link="b91835f5-6f83-4d9b-a0ad-a5a249f18b7c", scopes="read_links")
```

## Accounts
Bank accounts available for a link.

### Fetching accounts
To fetch accounts you will make use of the `.create()` method, the process will
retrieve all account data available from the bank institution. You **must** 
provide a `Link`.

If the account already exists in our records, only its balance and `collected_at` 
will be updated.

**Method:** 

```python
def create(
    self, link: str, *, token: str = None, encryption_key: str = None, **kwargs: str
) -> Union[List[Dict], Dict]:
    ...
```

**Example:**
```python
# Fetch accounts for a Link
accounts = client.Accounts.create("b91835f5-6f83-4d9b-a0ad-a5a249f18b7c")

# Fetch accounts for a Link that was created with a custom encryption key
accounts = client.Accounts.create(
    "b91835f5-6f83-4d9b-a0ad-a5a249f18b7c",
    encryption_key="your-encryption-key"
)

# Fetch accounts for a Link with and timeout after 15 seconds
accounts = client.Accounts.create(
    "b91835f5-6f83-4d9b-a0ad-a5a249f18b7c", 
    timeout=15
)
```

### Deleting accounts
An `Account` is persisted into our database after you fetch it, if you want you 
can delete it at any time.

**Method:**
```python
def delete(account: str) -> bool:
    ...
```

**Example:**
```python
client.Accounts.delete("161a5e4d-67f5-4760-ae4f-c1fe85cb20ca")

```

**:warning: Warning:**

When deleting an `Account`, all transactions_ and _owners_ data will be deleted 
on cascade.

### List and filtering
In order to make easier to find a `Account` (or many of them), it is possible to 
filter the results.

If not filters are provided, you will get all `Accounts` that you have registered.

**Method:**
```python
def list(**kwargs) -> Generator:
    ...
```

**Example:**
```python
# Retrieve all accounts (no filter given)
accounts = client.Accounts.list()

# Retrieve accounts for a specific bank
accounts = client.Accounts.list(institution="banorte")


# Retrieve all checking accounts with an available balance >= 100
accounts = client.Accounts.list(type__in="checking", balance_available__gte=100)
```

**:warning: Warning:**

The `.list()` method yields a `Generator`, you will have to iterate  over it or
cast it to `List` or `Tuple`.

## Transactions
Bank transactions made in a bank account. 

### Fetching transactions
To fetch transactions you will make use of the `.create()` method, the process will
retrieve all transaction data available from the bank institution. You **must** 
provide a `Link` and a date range defined by `date_from` and `date_to`. 

Optionally, if `Account` is given it will only fetch transaction matching 
the account.

If the account retrieved in the transaction doesn't exist, it will be created
with the transaction.

**Method:** 

```python
def create(
    self,
    link: str,
    date_from: str,
    *,
    date_to: str = None,
    account: str = None,
    token: str = None,
    encryption_key: str = None,
    **kwargs: str
) -> Union[List[Dict], Dict]:
    ...
```

**Example:**
```python
# Fetch transactions for a Link
transactions = client.Transactions.create(
    "b91835f5-6f83-4d9b-a0ad-a5a249f18b7c",
    "2019-07-01",
    date_to="2019-07-31"
)

# Fetch transactions for a Link that was created with a custom encryption key
transactions = client.Transactions.create(
    "b91835f5-6f83-4d9b-a0ad-a5a249f18b7c",
    "2019-07-01",
    date_to="2019-07-31",
    encryption_key="your-encryption-key"
)

# Fetch transactions for a Link with timeout after 15 seconds
transactions = client.Transactions.create(
    "b91835f5-6f83-4d9b-a0ad-a5a249f18b7c",
    "2019-07-01",
    date_to="2019-07-31",    
    timeout=15
)
```

### Deleting transactions
A `Transaction` is persisted into our database after you fetch it, if you want you 
can delete it at any time.

**Method:**
```python
def delete(transaction: str) -> bool:
    ...
```

**Example:**
```python
client.Transactions.delete("b92935e6-fb9a-4c2f-9d7c-3e42165421d6")

```

### List and filtering
In order to make easier to find a `Transaction` (or many of them), it is possible to 
filter the results.

If no filters are provided, you will get all `transactions` that you have registered.

**Method:**
```python
def list(**filters) -> Generator:
    ...
```

**Example:**
```python
# Retrieve all transactions (no filter given)
transactions = client.transactions.list()

# Retrieve transactions for a specific bank
transactions = client.transactions.list(institution="banorte")

# Retrieve transactions for a specific account
transactions = client.transactions.list(
    account="161a5e4d-67f5-4760-ae4f-c1fe85cb20ca"
)
```

**:warning: Warning:**

The `.list()` method yields a `Generator`, you will have to iterate  over it or
cast it to `List` or `Tuple`.

## Balances
Account balances at a given time.

### Fetching balances
To fetch balances you will make use of the `.create()` method. You will get the 
account balance at the end of every day within the specified date range. You **must** 
provide a `Link` and a date range defined by `date_from` and `date_to`. 

Optionally, if `Account` is given it will only fetch transaction matching 
the account.

If the account retrieved in the transaction doesn't exist, it will be created
with the transaction.

**Method:** 

```python
def create(
    self,
    link: str,
    date_from: str,
    *,
    date_to: str = None,
    account: str = None,
    token: str = None,
    encryption_key: str = None,
    **kwargs: str
) -> Union[List[Dict], Dict]:
    ...
```

**Example:**
```python
# Fetch balances for a Link
balances = client.Balances.create(
    "b91835f5-6f83-4d9b-a0ad-a5a249f18b7c",
    "2019-07-01",
    date_to="2019-07-31"
)

# Fetch balances for a Link that was created with a custom encryption key
balances = client.Balances.create(
    "b91835f5-6f83-4d9b-a0ad-a5a249f18b7c",
    "2019-07-01",
    date_to="2019-07-31",
    encryption_key="your-encryption-key"
)

# Fetch balances for a Link with timeout after 15 seconds
balances = client.Balances.create(
    "b91835f5-6f83-4d9b-a0ad-a5a249f18b7c",
    "2019-07-01",
    date_to="2019-07-31",    
    timeout=15
)
```

### Deleting balances
A `Balance` is persisted into our database after you fetch it, if you want you 
can delete it at any time.

**Method:**
```python
def delete(balance: str) -> bool:
    ...
```

**Example:**
```python
client.Balances.delete("b92935e6-fb9a-4c2f-9d7c-3e42165421d6")

```

### List and filtering
In order to make easier to find a `Balance` (or many of them), it is possible to 
filter the results.

If no filters are provided, you will get all `balances` that you have registered.

**Method:**
```python
def list(**filters) -> Generator:
    ...
```

**Example:**
```python
# Retrieve all balances (no filter given)
balances = client.balances.list()

# Retrieve balances for a specific bank
balances = client.balances.list(institution="banorte")

# Retrieve balances for a specific account
balances = client.balances.list(
    account="161a5e4d-67f5-4760-ae4f-c1fe85cb20ca"
)
```

**:warning: Warning:**

The `.list()` method yields a `Generator`, you will have to iterate  over it or
cast it to `List` or `Tuple`.


## Incomes
Bank entities that are supported by Belvo API.

### Fetching incomes
Retrieve the monthly income summaries for a specific `Link`.

**Method:**
```python
def create(
    self,
    link: str,
    *,
    token: str = None,
    encryption_key: str = None,
    save_data: bool = True,
    raise_exception: bool = False,
    **kwargs: Dict,
) -> Union[List[Dict], Dict]
```

**Example:**
```python
# Fetch incomes for a Link
incomes = client.Incomes.create("b91835f5-6f83-4d9b-a0ad-a5a249f18b7c")

# Fetch incomes for a Link that was created with a custom encryption key
incomes = client.Incomes.create(
    "b91835f5-6f83-4d9b-a0ad-a5a249f18b7c",
    encryption_key="your-encryption-key"
)

# Fetch incomes for a Link with and timeout after 15 seconds
incomes = client.Incomes.create(
    "b91835f5-6f83-4d9b-a0ad-a5a249f18b7c",
    timeout=15
)
```


## Owners
Personal information available from an account owner.

### Fetching owners
To fetch owners you will make use of the `.create()` method, the process will
retrieve all owner data available from the bank institution. You **must** 
provide a `Link`.

**Method:** 

```python
def create(
    self, link: str, *, token: str = None, encryption_key: str = None, **kwargs: str
) -> Union[List[Dict], Dict]:
    ...
```

**Example:**
```python
# Fetch owners for a Link
owners = client.Owners.create("b91835f5-6f83-4d9b-a0ad-a5a249f18b7c")

# Fetch owners for a Link that was created with a custom encryption key
owners = client.Owners.create(
    "b91835f5-6f83-4d9b-a0ad-a5a249f18b7c",
    encryption_key="your-encryption-key"
)

# Fetch owners for a Link with and timeout after 15 seconds
owners = client.Owners.create(
    "b91835f5-6f83-4d9b-a0ad-a5a249f18b7c",
    timeout=15
)
```

### Deleting owners
A `owner` is persisted into our database after you fetch it, if you want you 
can delete it at any time.

**Method:**
```python
def delete(owner: str) -> bool:
    ...
```

**Example:**
```python
client.Owners.delete("e29e8def-1959-4cb8-892d-d3bf65a5d9f3")

```

### List and filtering
In order to make easier to find a `Owner` (or many of them), it is possible to 
filter the results.

If not filters are provided, you will get all `owners` that you have registered.

**Method:**
```python
def list(**kwargs) -> Generator:
    ...
```

**Example:**
```python
# Retrieve all owners (no filter given)
owners = client.owners.list()

# Retrieve owners for a specific bank
owners = client.owners.list(institution="banorte")

# Retrieve owners for a specific account
owners = client.owners.list(
    account="161a5e4d-67f5-4760-ae4f-c1fe85cb20ca"
)
```

**:warning: Warning:**

The `.list()` method yields a `Generator`, you will have to iterate  over it or
cast it to `List` or `Tuple`.

## Invoices
List of invoices issued for a given account

### Fetching invoices
To fetch invoices you will make use of the `.create()` method, the process will
retrieve all invoices available from the institution. You **must** 
provide a `Link`, a date range defined by `date_from` and `date_to` and invoice 
`type`. 

**Method:** 

```python
def create(
    self,
    link: str,
    date_from: str,
    date_to: str,
    type_: str,
    *,
    attach_xml: bool = False,
    encryption_key: str = None,
    save_data: bool = True,
    raise_exception: bool = False,
    **kwargs: Dict,
) -> Union[List[Dict], Dict]:
    ...
```

**Example:**
```python
# Fetch invoices for a Link
invoices = client.Invoices.create(
    "b91835f5-6f83-4d9b-a0ad-a5a249f18b7c",
    "2019-07-01",
    "2019-07-31",
    "INFLOW"
)

# Fetch invoices for a Link that was created with a custom encryption key
invoices = client.Invoices.create(
    "b91835f5-6f83-4d9b-a0ad-a5a249f18b7c",
    "2019-07-01",
    "2019-07-31",
    "INFLOW",
    encryption_key="your-encryption-key"
)
```

### Deleting invoices
A `Invoice` is persisted into our database after you fetch it, if you want you 
can delete it at any time.

**Method:**
```python
def delete(invoice: str) -> bool:
    ...
```

**Example:**
```python
client.Invoices.delete("b92935e6-fb9a-4c2f-9d7c-3e42165421d6")

```

### List
**Method:**
```python
def list(**filters) -> Generator:
    ...
```

**Example:**
```python
# Retrieve all invoices
invoices = client.Invoices.list()
```

**:warning: Warning:**

The `.list()` method yields a `Generator`, you will have to iterate  over it or
cast it to `List` or `Tuple`.

## Tax Returns
List of tax returns for a given account

### Fetching tax returns
To fetch tax returns you will make use of the `.create()` method, the process will
retrieve all tax returns available from the institution. You **must** 
provide a `Link`, a year range defined by `year_from` and `year_to`. 

**Method:** 

```python
def create(
    self,
    link: str,
    year_from: str,
    year_to: str,
    *,
    attach_pdf: bool = False,
    encryption_key: str = None,
    save_data: bool = True,
    **kwargs: Dict,
) -> Union[List[Dict], Dict]:
    ...
```

**Example:**
```python
# Fetch tax returns for a Link
tax_returns = client.TaxReturns.create(
    "b91835f5-6f83-4d9b-a0ad-a5a249f18b7c",
    "2019",
    "2019"
)

# Fetch tax returns for a Link that was created with a custom encryption key
tax_returns = client.TaxReturns.create(
    "b91835f5-6f83-4d9b-a0ad-a5a249f18b7c",
    "2019",
    "2019",
    encryption_key="your-encryption-key"
)
```

### Deleting tax returns
A `TaxReturn` is persisted into our database after you fetch it, if you want you 
can delete it at any time.

**Method:**
```python
def delete(tax_return: str) -> bool:
    ...
```

**Example:**
```python
client.TaxReturns.delete("b92935e6-fb9a-4c2f-9d7c-3e42165421d6")

```

### List
**Method:**
```python
def list(**filters) -> Generator:
    ...
```

**Example:**
```python
# Retrieve all tax returns
tax_returns = client.TaxReturns.list()
```

**:warning: Warning:**

The `.list()` method yields a `Generator`, you will have to iterate  over it or
cast it to `List` or `Tuple`.

## Tax Compliance Status
Tax compliance status for a given `Link`

### Fetching tax compliance status
To fetch tax compliance status you will make use of the `.create()` method. The process will
retrieve the tax compliance status from the institution. You **must** 
provide a `Link`. 

**Method:** 

```python
def create(
    self,
    link: str,
    *,
    attach_pdf: bool = False,
    encryption_key: str = None,
    save_data: bool = True,
    raise_exception: bool = False,
    **kwargs: Dict,
) -> Union[List[Dict], Dict]:
    ...
```

**Example:**
```python
# Fetch tax compliance status for a Link
tax_copliance_status = client.TaxComplianceStatus.create(
    "b91835f5-6f83-4d9b-a0ad-a5a249f18b7c"
)

# Fetch tax compliance status for a Link that was created with a custom encryption key and retrieve its pdf
tax_compliance_status = client.TaxComplianceStatus.create(
    "b91835f5-6f83-4d9b-a0ad-a5a249f18b7c",
    encryption_key="your-encryption-key",
    attach_pdf=True
)
```

### Deleting tax compliance status
A `TaxComplianceStatus` is persisted into our database after you fetch it, if you want you 
can delete it at any time.

**Method:**
```python
def delete(tax_status: str) -> bool:
    ...
```

**Example:**
```python
client.TaxComplianceStatus.delete("b92935e6-fb9a-4c2f-9d7c-3e42165421d6")

```

### List
**Method:**
```python
def list(**filters) -> Generator:
    ...
```

**Example:**
```python
# Retrieve all tax compliance status
tax_compliance_status = client.TaxComplianceStatus.list()
```

**:warning: Warning:**

The `.list()` method yields a `Generator`, you will have to iterate  over it or
cast it to `List` or `Tuple`.


## Tax Status
Tax situation for a given `Link`

### Fetching tax status
To fetch tax status you will make use of the `.create()` method, the process will
retrieve the tax status from the institution. You **must** 
provide a `Link`. 

**Method:** 

```python
def create(
    self,
    link: str,
    *,
    attach_pdf: bool = False,
    encryption_key: str = None,
    save_data: bool = True,
    raise_exception: bool = False,
    **kwargs: Dict,
) -> Union[List[Dict], Dict]:
    ...
```

**Example:**
```python
# Fetch tax status for a Link
tax_status = client.TaxStatus.create(
    "b91835f5-6f83-4d9b-a0ad-a5a249f18b7c"
)

# Fetch tax status for a Link that was created with a custom encryption key and retrieve it's pdf
tax_status = client.TaxReturns.create(
    "b91835f5-6f83-4d9b-a0ad-a5a249f18b7c",
    encryption_key="your-encryption-key",
    attach_pdf=True
)
```

### Deleting tax status
A `TaxStatus` is persisted into our database after you fetch it, if you want you 
can delete it at any time.

**Method:**
```python
def delete(tax_status: str) -> bool:
    ...
```

**Example:**
```python
client.TaxStatus.delete("b92935e6-fb9a-4c2f-9d7c-3e42165421d6")

```

### List
**Method:**
```python
def list(**filters) -> Generator:
    ...
```

**Example:**
```python
# Retrieve all tax status
tax_status = client.TaxStatus.list()
```

**:warning: Warning:**

The `.list()` method yields a `Generator`, you will have to iterate  over it or
cast it to `List` or `Tuple`.

## Statements
List of monthly statements for a given account

### Fetching statements
To fetch statements you will make use of the `.create()` method, the process will
retrieve all monthly statements available from the institution. You **must** 
provide a `Link`, an `Account` and a month defined by `year` and `month`. 

**Method:** 

```python
def create(
    self,
    link: str,
    account: str,
    year: str,
    month: str,
    *,
    attach_pdf: bool = False,
    encryption_key: str = None,
    save_data: bool = True,
    raise_exception: bool = False,
    **kwargs: Dict,
) -> Union[List[Dict], Dict]:
```

**Example:**
```python
# Fetch statements for a Link
statements = client.Statements.create(
    "b91835f5-6f83-4d9b-a0ad-a5a249f18b7c",
    "161a5e4d-67f5-4760-ae4f-c1fe85cb20ca",
    "2019",
    "12"
)

# Fetch statements for a Link that was created with a custom encryption key
statements = client.Statements.create(
    "b91835f5-6f83-4d9b-a0ad-a5a249f18b7c",
    "161a5e4d-67f5-4760-ae4f-c1fe85cb20ca",
    "2019",
    "12",
    encryption_key="your-encryption-key"
)
```

### Resume fetch statements
Most institutions use 2FA to verify client's identity. The `.resume()` method 
is needed in those cases to provide the required `token` during the login.
`session`, `link` and `account` parameters will be needed to resume the process.

**Method:** 

```python
def resume(
    self,
    session: str,
    token: str,
    *,
    link: str = None,
    account: str = None,
    raise_exception: bool = False,
    **kwargs,
) -> Union[List[Dict], Dict]:
```

### Deleting statements
A `Statement` is persisted into our database after you fetch it, if you want you 
can delete it at any time.

**Method:**
```python
def delete(statement: str) -> bool:
    ...
```

**Example:**
```python
client.Statements.delete("b92935e6-fb9a-4c2f-9d7c-3e42165421d6")

```

### List
**Method:**
```python
def list(**filters) -> Generator:
    ...
```

**Example:**
```python
# Retrieve all statements
statements = client.Statements.list()
```

**:warning: Warning:**

The `.list()` method yields a `Generator`, you will have to iterate  over it or
cast it to `List` or `Tuple`.

## WidgetToken
A widget token that contains `access` and `refresh` keys. Use `access` to connect the Belvo Widget to your app. 

### Creating a new token
To create a new widget token you need to use the `.create()` method, the process will
request a new token to our API. This token has a limited scope and a short time to live. 

**Method:** 

```python
def create(
    self,
    *,
    raise_exception: bool = False
) -> Union[List[Dict], Dict]:
```
