# 🧰  pymsx - Mosaics AI MSX Client for Python

[![PyPI](https://img.shields.io/pypi/v/pymsx?style=flat-square)](https://pypi.org/project/pymsx/)
[![Interrogate](assets/interrogate_badge.svg)](https://github.com/Mosaics-AI/pymsx)

This repository contains the source code for Mosaics AI's official python client. This client is currently in pre-alpha version, so feedback is always welcome!

You are welcome to file an issue here for general use cases. You can also contact Mosaics Support [here](help.mosaics.ai).

## Requirements

Python 3.8 or above is required.

## Documentation

For the latest documentation, see

- [Mosaics AI](https://www.mosaics.ai)

## Quickstart

Install the library with `pip install pymsx`

Note: Don't hard-code authentication secrets into your Python. Use environment variables

email/Password Authentication:

```bash
export MSX_USERNAME=*************
export MSX_PASSWORD=*************
```

If you already have a token, use that instead:

```bash
export MSX_TOKEN=*****************************************
```

Example usage:
```python
import os
import pandas as pd
from pymsx.client import MsxClient

# If no credentials are supplied, then environment variables are required.
email = "help@mosaics.ai"
password = "$mosaics123"

# ...or try using an active token.
# This may fail, see exception handling below.
token = None

# First create client with active token or credentials
msx = MsxClient(
    # ...using email/password
    email=email,
    password=password,
    # ...or if using token, token will take priority
    token=token
)

# Check the health of your server
health = msx.health().dict()

print("Health: ", health)

assert health is not None and health['status'] == 'live'

# Add a dataset to your msx system

# From a DataFrame
path = "/path/to/dataset/data.csv"
df = pd.DataFrame(path)
result = msx.datasets.add(df=df)

# Or pass in a string path to read from fs directly
result = msx.datasets.add(path=path)

if result.ok:
    print("DataFrame uploaded: ", result.details)
else
    print("Upload failed: ", result.error)
```

Exception handling:
```python
from pymsx.client import MsxClient
from pymsx.exceptions import ApiResponseError, InvalidTokenError

try:
    try:
        # An InvalidToken error is raised if the token is expired or incorrect
        msx = MsxClient(
            token=token
        )
    except InvalidTokenError:
        print(f"Token invalid, logging in instead.")
        # Catch all other errors using ApiResponseErrors
        msx = MsxClient(
            email=email,
            password=password
        )
except ApiResponseError as e:
    print(f"Could not create msx client: {e.error}")
    return
```

## Contributing

We will allow contributing soon!

## License

[Apache License 2.0](LICENSE)
