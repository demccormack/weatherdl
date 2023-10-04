from utils import unused_file_name_like


def test_it_returns_name_if_unused():
    assert unused_file_name_like("test.pptx", []) == "test.pptx"


def test_it_adds_a_suffix_if_name_already_taken():
    assert (
        unused_file_name_like("test.pptx", ["test.pptx", "test (1).pptx"])
        == "test (2).pptx"
    )
