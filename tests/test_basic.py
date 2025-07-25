# tests/test_basic.py
import pytest
import os
import sys

# Add project root to path
project_root = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, project_root)

def test_imports():
    """Test that core modules can be imported"""
    try:
        from src.search_agent import SearchAgent
        from src.recommendation_agent import RecommendationAgent  
        from src.gbr_system import GBRSystem
        assert True
    except ImportError as e:
        pytest.fail(f"Import failed: {e}")

def test_config_files_exist():
    """Test that required config files exist"""
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'user_profiles.json')
    assert os.path.exists(config_path), "user_profiles.json not found"

def test_app_file_exists():
    """Test that app.py exists"""
    app_path = os.path.join(os.path.dirname(__file__), '..', 'app.py')
    assert os.path.exists(app_path), "app.py not found"

def test_requirements_file_exists():
    """Test that requirements.txt exists"""
    req_path = os.path.join(os.path.dirname(__file__), '..', 'requirements.txt')
    assert os.path.exists(req_path), "requirements.txt not found"