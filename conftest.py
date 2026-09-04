import os
import sys

# Make the role root importable so tests can `import filter_plugins.custom`.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
