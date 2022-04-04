import pytest
import main

def test_file1_method1():
	x=5
	y=6
	assert x+1 == y,"test failed"
	response = main.lambda_handler({}, {})
	assert "all is good siuuu" == response, "Validate output"