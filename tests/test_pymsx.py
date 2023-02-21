"""Test pymsx

Test package level functionality.
"""
import pytest

email = "help@mosaics.ai"
password = "$mosaics123"

invalid_token = (
    "eyJhbGciOiJSUzI1NiIsImtpZCI6ImFlYjMxMjdiMjRjZTg2MDJjODEyNDUxZThmZTczZDU4"
    "MjkyMDg4N2MiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb"
    "2dsZS5jb20vbXN4LWRlbW8tNWQ1YWYiLCJhdWQiOiJtc3gtZGVtby01ZDVhZiIsImF1dGhfd"
    "GltZSI6MTY3Njg3MTc4MiwidXNlcl9pZCI6Ill6cDZyVFFGSEFkY256VWRjdFdnYTFuMU4zb"
    "zIiLCJzdWIiOiJZenA2clRRRkhBZGNuelVkY3RXZ2ExbjFOM28yIiwiaWF0IjoxNjc2ODcxN"
    "zgyLCJleHAiOjE2NzY4NzUzODIsImVtYWlsIjoicGF0dGVyc29uLmdlb3JnZUBnbWFpbC5jb"
    "20iLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZ"
    "W1haWwiOlsicGF0dGVyc29uLmdlb3JnZUBnbWFpbC5jb20iXX0sInNpZ25faW5fcHJvdmlkZ"
    "XIiOiJwYXNzd29yZCJ9fQ.dbxU4MWwtAa2Z9_nac8Skw8F5dvV2Vdvqnzy-vX3HL9ddI1IUw"
    "ItcFomi1-DeR0ZesCYlsSptoJ-n_6NsDkoBiVhvboW-8mTldqsA-p4ravUhhAkIyGm2iuzCq"
    "XoVmm7SAEe4Yrmwy-otb9eL0iSqCLdxyglMu1oaIHttCfIoUvI7cgqueNSy7-qmCoSLSPmf8"
    "k5WbeFshqvDxvlNyMejqwViQcyK4qMwa6oKzCL8MgAhbXbxdg66j4pwwIYOxghD0rLPSyfmD"
    "eM_xVtcwqZDZk-dBaLH_GRgMWZfC6kSKPZs9M8McnWXEbVvpmW-S7f6tnmzpR8_E_2kdPdEP"
    "qdeA"
)


def test_connect_with_credentials():
    """Test client connection with creds."""
    from pymsx.client import MsxClient

    msx = MsxClient(email=email, password=password)

    print("Token: ", msx.token)

    assert msx.token is not None and len(msx.token) > 0
    assert msx.org_id is not None
    assert msx.validated is True


def test_connect_with_env(monkeypatch):
    """Test client connection with env variables."""
    with monkeypatch.context() as m:
        """Test client connection use env vars."""
        m.setenv("MSX_EMAIL", email)
        m.setenv("MSX_PASSWORD", password)

        from pymsx.client import MsxClient

        msx = MsxClient()

        print("Token: ", msx.token)

        assert msx.token is not None and len(msx.token) > 0
        assert msx.org_id is not None
        assert msx.validated is True


def test_incorrect_token():
    """Test incorrect token."""
    from pymsx.client import MsxClient
    from pymsx.exceptions import InvalidTokenError

    with pytest.raises(InvalidTokenError):
        _ = MsxClient(token=invalid_token)


def test_health_with_token():
    """Test client health check."""
    from pymsx.client import MsxClient

    msx = MsxClient(email=email, password=password)

    assert msx.org_id is not None
    assert msx.token is not None
    assert msx.validated is True

    health = msx.health()

    health = health.dict()

    print("Health: ", health)

    assert health is not None
    assert health["status"] == "live"


def test_upload():
    """Test multipart upload"""
    from pymsx.client import MsxClient

    csv_file = (
        "/Users/munnyserver/kairosos/mosaics.ai/pymsx/tests/fixtures/nlp_train.csv"
    )

    print("File path: ", csv_file)

    msx = MsxClient(email=email, password=password)

    assert msx.org_id is not None
    assert msx.token is not None
    assert msx.validated is True

    json_res = msx.datasets.add(
        csv_file,
        # pass through fields for msx triggers
        test_field1="test_value1",
        test_field2="test_value2",
    )

    print("Res json: ", json_res)

    assert json_res is not None and len(json_res["path"]) > 0
    assert json_res["test_field1"] == "test_value1"
    assert json_res["test_field2"] == "test_value2"
