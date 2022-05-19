import pytest
import main

def exists_failed_test():
    with pytest.raises(Exception) as e:
        exists("C0123")
