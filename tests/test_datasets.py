"""Test pymsx

Test api.dataset functionality.
"""
import os

email = "help@mosaics.ai"
password = "$mosaics123"


def test_upload():
    """Test multipart upload"""
    from pymsx.client import MsxClient

    csv_file = os.path.join(os.path.dirname(__file__), "fixtures", "nlp_train.csv")

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
