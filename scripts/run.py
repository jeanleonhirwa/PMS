import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from main.app import App

if __name__ == "__main__":
    app = App()
    app.mainloop()