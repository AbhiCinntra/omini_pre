from django.test import TestCase

# Create your tests here.
import os

# Get the absolute path of the currently running script
current_script_path = os.path.abspath(__file__)

print("current_script_path", os.path.dirname(__file__))

import sys
from pathlib import Path
project_base_dir = Path(__file__).resolve().parent.parent
setting_final_path = os.path.join(project_base_dir, 'bridge')
print("final_path", setting_final_path)
sys.path.append(setting_final_path)
import settings

print(settings.DATABASES['default']['HOST'])


