import pytest
import main

@pytest.mark.parametrize(
    "input",[
        (400),
        (500),
        (501)
    ]
)
def test_validate_dynamodb_response_failure(input):
    with pytest.raises(Exception) as e:
        main.validate_dynamodb_response(input)