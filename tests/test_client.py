"""Test pymoai

Test client functionality.
"""
import pytest

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
    from pymoai.client import MoaiClient

    email = "tech@montops.ai"
    password = "$montops123"

    moai = MoaiClient(email=email, password=password)

    print("Token: ", moai.token)

    assert moai.token is not None and len(moai.token) > 0
    assert moai.org_id is not None
    assert moai.validated is True


def test_connect_with_env(monkeypatch):
    """Test client connection with env variables."""
    with monkeypatch.context() as m:
        email = "tech@montops.ai"
        password = "$montops123"

        m.setenv("MOAI_EMAIL", email)
        m.setenv("MOAI_PASSWORD", password)

        from pymoai.client import MoaiClient

        moai = MoaiClient()

        print("Token: ", moai.token)

        assert moai.token is not None and len(moai.token) > 0
        assert moai.org_id is not None
        assert moai.validated is True


def test_incorrect_token():
    """Test incorrect token."""
    from pymoai.client import MoaiClient
    from pymoai.exceptions import InvalidTokenError

    with pytest.raises(InvalidTokenError):
        _ = MoaiClient(token=invalid_token)


def test_health_with_token():
    """Test client health check."""
    from pymoai.client import MoaiClient

    email = "tech@montops.ai"
    password = "$montops123"

    moai = MoaiClient(email=email, password=password)

    assert moai.org_id is not None
    assert moai.token is not None
    assert moai.validated is True

    health = moai.health()

    print("Health: ", health)

    assert health is not None
    assert health == "ok"
