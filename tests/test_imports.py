# tests/test_imports.py
#!/usr/bin/env python3

def test_imports():
    """Test that all required imports work"""
    try:
        import pytest
        print("✓ pytest imported successfully")
    except ImportError as e:
        print(f"✗ pytest import failed: {e}")
        raise

    try:
        from playwright.sync_api import Page, expect
        print("✓ playwright.sync_api imported successfully")
    except ImportError as e:
        print(f"✗ playwright.sync_api import failed: {e}")
        raise

    try:
        import browserstack_sdk
        print("✓ browserstack_sdk imported successfully")
    except ImportError as e:
        print(f"✗ browserstack_sdk import failed: {e}")
        raise

    print("All imports successful!")

if __name__ == "__main__":
    test_imports()