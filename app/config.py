import os

def is_test_mode() -> bool:
    return os.getenv("MAILGENT_TEST_MODE") == "1"
