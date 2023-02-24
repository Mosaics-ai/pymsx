"""Test pymsx

Test api.commands functionality.
"""
email = "help@mosaics.ai"
password = "$mosaics123"


def test_stdio_response():
    """Test listing metastore data"""
    from pymsx.client import MsxClient

    msx = MsxClient(email=email, password=password)

    assert msx.org_id is not None
    assert msx.token is not None
    assert msx.validated is True

    res = msx.commands.run("metastore", ["list", "-b", "default"])

    print("Command response: ", res)

    assert res is not None
    assert isinstance(res, dict)
    assert res["stdout"] is not None
    assert res["stderr"] is not None
