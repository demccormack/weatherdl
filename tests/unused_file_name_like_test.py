from .context import presentation


def test_it_returns_name_if_unused():
    assert presentation.unused_file_name_like('test.pptx', []) == 'test.pptx'
