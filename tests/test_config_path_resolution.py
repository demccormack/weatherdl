import os
import tempfile
from unittest.mock import patch

import pytest

from application_config import ApplicationConfig


def test_config_can_be_found_from_different_directories():
    """Test that config.json can be found regardless of current working directory."""
    # Get the path resolution logic from main.py
    test_dir = os.path.dirname(__file__)
    repo_root = os.path.dirname(test_dir)
    main_py_path = os.path.join(repo_root, "src", "main.py")
    main_py_abs_path = os.path.abspath(main_py_path)
    
    # Simulate what main.py does to find config.json
    script_dir = os.path.dirname(os.path.dirname(main_py_abs_path))
    config_path = os.path.join(script_dir, "config.json")
    
    original_cwd = os.getcwd()
    
    try:
        # Test from repository root
        os.chdir(script_dir)
        config = ApplicationConfig(config_path)
        assert config.config is not None
        assert "time_zone" in config.config
        
        # Test from temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            os.chdir(temp_dir)
            config = ApplicationConfig(config_path)
            assert config.config is not None
            assert "time_zone" in config.config
            
        # Test from user home directory
        os.chdir(os.path.expanduser("~"))
        config = ApplicationConfig(config_path)
        assert config.config is not None
        assert "time_zone" in config.config
        
    finally:
        os.chdir(original_cwd)


def test_image_directory_is_relative_to_home():
    """Test that images are still written relative to user home directory."""
    # Get the path resolution logic from main.py
    test_dir = os.path.dirname(__file__)
    repo_root = os.path.dirname(test_dir)
    main_py_path = os.path.join(repo_root, "src", "main.py")
    main_py_abs_path = os.path.abspath(main_py_path)
    script_dir = os.path.dirname(os.path.dirname(main_py_abs_path))
    config_path = os.path.join(script_dir, "config.json")
    
    config = ApplicationConfig(config_path)
    
    # Verify that the image directory is under the user's home directory
    home = os.path.expanduser("~")
    assert config.img_dir.startswith(home), f"Image directory {config.img_dir} should be under home directory {home}"