"""Test pymoai

Test api.dataset functionality.
"""
import os

email = "tech@montops.ai"
password = "$montops123"


def test_upload():
    """Test multipart upload"""
    from pymoai.client import MoaiClient

    csv_file = os.path.join(os.path.dirname(__file__), "fixtures", "nlp_train.csv")

    print("File path: ", csv_file)

    moai = MoaiClient(email=email, password=password)

    assert moai.org_id is not None
    assert moai.token is not None
    assert moai.validated is True

    json_res = moai.datasets.add(
        csv_file,
        # pass through fields for moai triggers
        test_field1="test_value1",
        test_field2="test_value2",
    )

    print("Add dataset response: ", json_res)

    assert json_res is not None and len(json_res["path"]) > 0
    assert json_res["test_field1"] == "test_value1"
    assert json_res["test_field2"] == "test_value2"
