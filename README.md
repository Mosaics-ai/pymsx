# 🧰  pymsx - Mosaics AI MSX Client for Python

[![PyPI](https://img.shields.io/pypi/v/pymsx?style=flat-square)](https://pypi.org/project/pymsx/)
[![Downloads](https://pepy.tech/badge/pymsx)](https://pepy.tech/project/pymsx)
[![Documentation](assets/interrogate_badge.svg)](https://github.com/Mosaics-ai/pymsx)

This repository contains the source code for Mosaics AI's official python client. This client is currently in pre-alpha version, so feedback is always welcome!

You are welcome to file an issue here for general use cases. You can also contact Databricks Support [here](help.mosaics.ai).

## Requirements

Python 3.8 or above is required.

## Documentation

For the latest documentation, see

- [Mosaics AI](https://www.mosaics.ai)

## Quickstart

Install the library with `pip install pymsx`

Note: Don't hard-code authentication secrets into your Python. Use environment variables

Username/Password Authentication:

```bash
export MSX_ORG_ID=***************
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
from pymsx import MsxClient

org_id = os.getenv("MSX_ORG_ID")
username = os.getenv("MSX_USERNAME")
password = os.getenv("MSX_PASSWORD")

# or if using token
token = os.getenv("MSX_TOKEN")

msx = MsxClient(
    # required
    org_id=org_id,

    # if using username/password
    username=username,
    password=password,
    # or if using token, token will take priority
    token=token
)

# add a dataset to your msx system

# from a DataFrame
path = "/path/to/dataset/data.csv"
df = pd.DataFrame(path)
result = msx.datasets.add(df=df)

# or pass in a string path to read from fs directly
result = msx.datasets.add(path=path)

if result.ok():
    print("DataFrame uploaded: ", result.details())
else
    print("Upload failed: ", result.error())

# not necessary, but allows some cleanup
msx.disconnect()
```

In the above example:
- `org_id` is your Mosaics AI organization identifier.

## Contributing

We will allow contributing soon!

## License

[Apache License 2.0](LICENSE)
