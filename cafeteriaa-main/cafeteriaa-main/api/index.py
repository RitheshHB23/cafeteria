import sys
from pathlib import Path

# Add the parent directory to sys.path so that 'server' can be imported
sys.path.append(str(Path(__file__).parent.parent))

from server import app
