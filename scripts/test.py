import unittest
import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

if __name__ == "__main__":
    # Discover and run the tests
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir="src/tests")
    runner = unittest.TextTestRunner()
    runner.run(suite)