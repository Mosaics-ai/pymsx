# 🧰  pymoai - MontOps moai client for Python

[![PyPI](https://img.shields.io/pypi/v/pymoai?style=flat-square)](https://pypi.org/project/pymoai/)
[![Interrogate](https://raw.githubusercontent.com/MontOpsInc/pymoai/main/assets/interrogate_badge.svg)](https://github.com/MontOpsInc/pymoai)

This repository contains the source code for MontOps AI's official python client. This client is currently in pre-alpha version, so feedback is always welcome!

You are welcome to file an issue here for general use cases. You can also contact MontOps Support [here](help.montops.ai).

## Requirements

Python 3.8 or above is required.

## Documentation

For the latest documentation, see

- [MontOps AI](https://www.montops.ai)

## Quickstart

Install the library with `pip install pymoai`

Note: Don't hard-code authentication secrets into your Python. Use environment variables

email/Password Authentication:

```bash
export MOAI_USERNAME=*************
export MOAI_PASSWORD=*************
```

If you already have a token, use that instead:

```bash
export MOAI_TOKEN=*****************************************
```

Example usage:
```python
import os
import pandas as pd
from pymoai.client import MoaiClient

# If no credentials are supplied, then environment variables are required.
email = "tech@montops.ai"
password = "$montops123"

# ...or try using an active token.
# This may fail, see exception handling below.
token = None

# First create client with active token or credentials
moai = MoaiClient(
    # ...using email/password
    email=email,
    password=password,
    # ...or if using token, token will take priority
    token=token
)

# Check the health of your server
health = moai.health().dict()

print("Health: ", health)

assert health is not None and health['status'] == 'live'

# Add a dataset to your moai system

# From a DataFrame
path = "/path/to/dataset/data.csv"
df = pd.DataFrame(path)
result = moai.datasets.add(df=df)

# Or pass in a string path to read from fs directly
result = moai.datasets.add(path=path)

if result.ok:
    print("DataFrame uploaded: ", result.details)
else
    print("Upload failed: ", result.error)
```

Exception handling:
```python
from pymoai.client import MoaiClient
from pymoai.exceptions import ApiResponseError, InvalidTokenError

try:
    try:
        # An InvalidToken error is raised if the token is expired or incorrect
        moai = MoaiClient(
            token=token
        )
    except InvalidTokenError:
        print(f"Token invalid, logging in instead.")
        # Catch all other errors using ApiResponseErrors
        moai = MoaiClient(
            email=email,
            password=password
        )
except ApiResponseError as e:
    print(f"Could not create moai client: {e.error}")
    return
```

## Contributing

We will allow contributing soon!

## License

[Apache License 2.0](LICENSE)
