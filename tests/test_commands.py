"""Test pymoai

Test api.commands functionality.
"""
email = "tech@montops.ai"
password = "$montops123"


def test_stdio_response():
    """Test listing metastore data"""
    from pymoai.client import MoaiClient

    moai = MoaiClient(email=email, password=password)

    assert moai.org_id is not None
    assert moai.token is not None
    assert moai.validated is True

    res = moai.commands.run("metastore", ["list", "-b", "default"])

    print("Command response: ", res)

    assert res is not None
    assert isinstance(res, dict)
    assert res["stdout"] is not None
    assert res["stderr"] is not None
